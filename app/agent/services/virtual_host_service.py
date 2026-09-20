# 📄 Dosya Yolu: E:\JHoster\app\agent\services\virtual_host_service.py
# 📌 Amac: JHoster virtual host is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Project kaydindan guvenli virtual host planlama ve config uretme akisini yonetir
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    VIRTUAL_HOST_ERROR_INVALID_DOMAIN,
    VIRTUAL_HOST_ERROR_PATH_BLOCKED,
    VIRTUAL_HOST_ERROR_PROJECT_NOT_FOUND,
    VIRTUAL_HOST_MESSAGE_DRY_RUN,
    VIRTUAL_HOST_MESSAGE_GENERATED,
    VIRTUAL_HOST_STATUS_GENERATED,
    VIRTUAL_HOST_STATUS_PLANNED,
)
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from tools.project_path_tool import ProjectPathTool
from tools.virtual_host_config_tool import VirtualHostConfigTool


class VirtualHostService:
    def __init__(
        self,
        project_registry_repository: ProjectRegistryRepository,
        virtual_host_registry_repository: VirtualHostRegistryRepository,
        project_path_tool: ProjectPathTool,
        virtual_host_config_tool: VirtualHostConfigTool,
    ) -> None:
        self.project_registry_repository = project_registry_repository
        self.virtual_host_registry_repository = virtual_host_registry_repository
        self.project_path_tool = project_path_tool
        self.virtual_host_config_tool = virtual_host_config_tool

    def list_virtual_hosts(self) -> dict[str, Any]:
        virtual_hosts = self.virtual_host_registry_repository.list_virtual_hosts()

        return {
            "success": True,
            "count": len(virtual_hosts),
            "virtual_hosts": virtual_hosts,
        }

    def get_virtual_host(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        virtual_host_item = self.virtual_host_registry_repository.get_virtual_host(normalized_code)

        if virtual_host_item is None:
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "virtual_host": virtual_host_item,
        }

    def plan_virtual_host(self, project_code: str, domain: str, port: int) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        project_item = self.project_registry_repository.get_project(normalized_code)

        if project_item is None:
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        plan = self.virtual_host_config_tool.build_virtual_host_plan(project_item, domain, port)
        if not plan.get("valid_domain", False):
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_INVALID_DOMAIN,
                "plan": plan,
            }

        if not plan.get("safe", False):
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_PATH_BLOCKED,
                "plan": plan,
            }

        return {
            "success": True,
            "status": VIRTUAL_HOST_STATUS_PLANNED,
            "message": VIRTUAL_HOST_MESSAGE_DRY_RUN,
            "virtual_host_plan": plan,
        }

    def generate_virtual_host(self, project_code: str, domain: str, port: int, dry_run: bool) -> dict[str, Any]:
        plan_response = self.plan_virtual_host(project_code, domain, port)
        if not plan_response.get("success", False):
            return plan_response

        plan = plan_response.get("virtual_host_plan", {})
        if dry_run:
            return plan_response

        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        project_item = self.project_registry_repository.get_project(normalized_code)
        if project_item is None:
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        generate_result = self.virtual_host_config_tool.generate_config_file(project_item, domain, port)
        if not generate_result.get("success", False):
            return {
                "success": False,
                "error": VIRTUAL_HOST_ERROR_PATH_BLOCKED,
                "generate_result": generate_result,
            }

        virtual_host_payload = self._build_virtual_host_payload(project_item, generate_result.get("plan", plan))
        stored_virtual_host = self.virtual_host_registry_repository.upsert_virtual_host(virtual_host_payload)

        return {
            "success": True,
            "status": VIRTUAL_HOST_STATUS_GENERATED,
            "message": VIRTUAL_HOST_MESSAGE_GENERATED,
            "virtual_host": stored_virtual_host,
            "generate_result": generate_result,
        }

    def _build_virtual_host_payload(self, project_item: dict[str, Any], plan: dict[str, Any]) -> dict[str, Any]:
        generated_at = datetime.now(timezone.utc).isoformat()

        return {
            "project_code": project_item.get("code"),
            "project_name": project_item.get("name"),
            "domain": plan.get("domain"),
            "port": plan.get("port"),
            "document_root": plan.get("document_root"),
            "config_file": plan.get("config_file"),
            "runtime_family": project_item.get("runtime_family"),
            "runtime_version": project_item.get("runtime_version"),
            "runtime_adapter": project_item.get("runtime_adapter"),
            "generated_from": "virtual_host_service",
            "generated_at": generated_at,
        }
