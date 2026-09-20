# 📄 Dosya Yolu: E:\JHoster\app\agent\services\project_service.py
# 📌 Amac: JHoster proje olusturma ve listeleme is kurallarini yonetir
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Aktif runtime version secimi ile www altinda guvenli project kaydi olusturur
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    PROJECT_DEFAULT_RUNTIME_FAMILY,
    PROJECT_ERROR_ACTIVE_RUNTIME_NOT_FOUND,
    PROJECT_ERROR_ALREADY_EXISTS,
    PROJECT_ERROR_INVALID_CODE,
    PROJECT_ERROR_NOT_FOUND,
    PROJECT_ERROR_PATH_BLOCKED,
    PROJECT_ERROR_COMMUNITY_SITE_LIMIT,
    PROJECT_MESSAGE_CREATED,
    PROJECT_MESSAGE_DRY_RUN,
    PROJECT_STATUS_ACTIVE,
    PROJECT_STATUS_PLANNED,
)
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from services.hosts_auto_service import HostsAutoService
from services.plan_gate_service import PlanGateService
from tools.project_path_tool import ProjectPathTool


class ProjectService:
    def __init__(
        self,
        project_registry_repository: ProjectRegistryRepository,
        runtime_version_repository: RuntimeVersionRepository,
        project_path_tool: ProjectPathTool,
        plan_gate_service: PlanGateService,
        hosts_auto_service: HostsAutoService | None = None,
    ) -> None:
        self.project_registry_repository = project_registry_repository
        self.runtime_version_repository = runtime_version_repository
        self.project_path_tool = project_path_tool
        self.plan_gate_service = plan_gate_service
        self.hosts_auto_service = hosts_auto_service

    def list_projects(self) -> dict[str, Any]:
        projects = self.project_registry_repository.list_projects()

        return {
            "success": True,
            "count": len(projects),
            "projects": projects,
        }

    def get_project(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        project_item = self.project_registry_repository.get_project(normalized_code)

        if project_item is None:
            return {
                "success": False,
                "error": PROJECT_ERROR_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "project": project_item,
        }

    def create_project(
        self,
        project_code: str,
        project_name: str,
        runtime_family: str,
        dry_run: bool,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        normalized_runtime_family = str(runtime_family or PROJECT_DEFAULT_RUNTIME_FAMILY).strip()

        if not self.project_path_tool.is_valid_project_code(normalized_code):
            return {
                "success": False,
                "error": PROJECT_ERROR_INVALID_CODE,
                "project_code": normalized_code,
            }

        existing_project = self.project_registry_repository.get_project(normalized_code)
        if existing_project is not None and not dry_run:
            return {
                "success": False,
                "error": PROJECT_ERROR_ALREADY_EXISTS,
                "project": existing_project,
            }

        plan_gate = self.plan_gate_service.can_create_project()
        if not dry_run and existing_project is None and not plan_gate.get("allowed", False):
            return {
                "success": False,
                "status": "blocked",
                "error": PROJECT_ERROR_COMMUNITY_SITE_LIMIT,
                "message": plan_gate.get("message"),
                "project_code": normalized_code,
                "plan_gate": plan_gate,
            }

        active_runtime = self.runtime_version_repository.get_active_version(normalized_runtime_family)
        if active_runtime is None:
            return {
                "success": False,
                "error": PROJECT_ERROR_ACTIVE_RUNTIME_NOT_FOUND,
                "runtime_family": normalized_runtime_family,
            }

        plan = self.project_path_tool.build_project_plan(normalized_code)
        project_payload = self._build_project_payload(
            normalized_code,
            project_name,
            normalized_runtime_family,
            active_runtime,
            plan,
        )

        if not plan.get("safe", False):
            return {
                "success": False,
                "error": PROJECT_ERROR_PATH_BLOCKED,
                "project": project_payload,
                "plan_gate": plan_gate,
            }

        if dry_run:
            return {
                "success": True,
                "status": PROJECT_STATUS_PLANNED,
                "message": PROJECT_MESSAGE_DRY_RUN,
                "project": project_payload,
                "plan_gate": plan_gate,
            }

        create_result = self.project_path_tool.create_project_files(
            normalized_code,
            project_name,
            normalized_runtime_family,
            active_runtime,
        )
        if not create_result.get("success", False):
            return {
                "success": False,
                "error": PROJECT_ERROR_PATH_BLOCKED,
                "create_result": create_result,
            }

        stored_project = self.project_registry_repository.upsert_project(project_payload)

        hosts_auto_result = self._sync_hosts_after_create(stored_project)

        return {
            "success": True,
            "status": PROJECT_STATUS_ACTIVE,
            "message": PROJECT_MESSAGE_CREATED,
            "project": stored_project,
            "create_result": create_result,
            "hosts_auto": hosts_auto_result,
            "plan_gate": plan_gate,
        }

    def _sync_hosts_after_create(self, stored_project: dict[str, Any]) -> dict[str, Any]:
        if self.hosts_auto_service is None:
            return {
                "success": False,
                "status": "skipped",
                "message": "hosts auto service is not configured",
            }

        return self.hosts_auto_service.sync_project(
            project_payload=stored_project,
            ip_value=None,
            real_write=True,
            dry_run=False,
        )

    def _build_project_payload(
        self,
        project_code: str,
        project_name: str,
        runtime_family: str,
        active_runtime: dict[str, Any],
        plan: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "code": project_code,
            "name": str(project_name).strip() or project_code,
            "runtime_family": runtime_family,
            "runtime_component_code": active_runtime.get("component_code"),
            "runtime_version": active_runtime.get("version"),
            "project_path": plan.get("project_path"),
            "document_root": plan.get("document_root"),
            "created_from": "project_service",
            "planned_at": datetime.now(timezone.utc).isoformat(),
        }
