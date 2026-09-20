# 📄 Dosya Yolu: E:\JHoster\app\agent\services\quick_app_service.py
# 📌 Amac: Quick App template listeleme, stack secimli planlama ve scaffold olusturma is kurallarini yonetir
# 📌 Modul - FileType
# Version: 3.77.0
# Aciklama: Controller'dan gelen Quick App isteklerini runtime, provisioning plan, proje registry, scaffold tool ve hosts auto katmanlarina dagitir
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    QUICK_APP_ERROR_ALREADY_EXISTS,
    QUICK_APP_ERROR_ACTIVE_RUNTIME_NOT_FOUND,
    QUICK_APP_ERROR_INVALID_PROJECT_CODE,
    QUICK_APP_ERROR_PATH_BLOCKED,
    QUICK_APP_ERROR_COMMUNITY_SITE_LIMIT,
    QUICK_APP_ERROR_TEMPLATE_NOT_FOUND,
    QUICK_APP_MESSAGE_CREATED,
    QUICK_APP_MESSAGE_DRY_RUN,
    QUICK_APP_STATUS_CREATED,
    QUICK_APP_STATUS_PLANNED,
)
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.quick_app_registry_repository import QuickAppRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from tools.project_path_tool import ProjectPathTool
from services.hosts_auto_service import HostsAutoService
from services.plan_gate_service import PlanGateService
from services.stack_provisioning_service import StackProvisioningService
from tools.quick_app_template_tool import QuickAppTemplateTool


class QuickAppService:
    WEB_SERVER_APACHE = "apache"
    WEB_SERVER_NGINX = "nginx"
    SERVICE_MYSQL = "mysql"
    SERVICE_PHP = "php"
    SERVICE_MAILPIT = "mailpit"

    def __init__(
        self,
        quick_app_registry_repository: QuickAppRegistryRepository,
        project_registry_repository: ProjectRegistryRepository,
        runtime_version_repository: RuntimeVersionRepository,
        project_path_tool: ProjectPathTool,
        quick_app_template_tool: QuickAppTemplateTool,
        plan_gate_service: PlanGateService,
        hosts_auto_service: HostsAutoService | None = None,
        stack_provisioning_service: StackProvisioningService | None = None,
    ) -> None:
        self.quick_app_registry_repository = quick_app_registry_repository
        self.project_registry_repository = project_registry_repository
        self.runtime_version_repository = runtime_version_repository
        self.project_path_tool = project_path_tool
        self.quick_app_template_tool = quick_app_template_tool
        self.plan_gate_service = plan_gate_service
        self.hosts_auto_service = hosts_auto_service
        self.stack_provisioning_service = stack_provisioning_service

    def list_templates(self) -> dict[str, Any]:
        templates = self.quick_app_template_tool.list_templates()
        return {
            "success": True,
            "count": len(templates),
            "templates": templates,
        }

    def list_records(self) -> dict[str, Any]:
        records = self.quick_app_registry_repository.list_records()
        return {
            "success": True,
            "count": len(records),
            "records": records,
        }

    def get_latest_record(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        record = self.quick_app_registry_repository.get_latest_record(normalized_code)
        return {
            "success": record is not None,
            "project_code": normalized_code,
            "record": record,
        }

    def get_template(self, template_code: str) -> dict[str, Any]:
        normalized_template_code = str(template_code).strip().lower()
        template_item = self.quick_app_template_tool.get_template(normalized_template_code)
        if template_item is None:
            return {
                "success": False,
                "error": QUICK_APP_ERROR_TEMPLATE_NOT_FOUND,
                "template_code": normalized_template_code,
            }

        return {
            "success": True,
            "template": template_item,
        }

    def plan_app(
        self,
        project_code: str,
        project_name: str,
        template_code: str,
        domain: str,
        port: int,
        web_server: str = WEB_SERVER_APACHE,
        include_mysql: bool = True,
        include_php: bool = True,
        include_mailpit: bool = False,
    ) -> dict[str, Any]:
        return self._build_result(project_code, project_name, template_code, domain, port, True, web_server, include_mysql, include_php, include_mailpit)

    def create_app(
        self,
        project_code: str,
        project_name: str,
        template_code: str,
        domain: str,
        port: int,
        dry_run: bool,
        web_server: str = WEB_SERVER_APACHE,
        include_mysql: bool = True,
        include_php: bool = True,
        include_mailpit: bool = False,
    ) -> dict[str, Any]:
        return self._build_result(project_code, project_name, template_code, domain, port, dry_run, web_server, include_mysql, include_php, include_mailpit)

    def _build_result(
        self,
        project_code: str,
        project_name: str,
        template_code: str,
        domain: str,
        port: int,
        dry_run: bool,
        web_server: str = WEB_SERVER_APACHE,
        include_mysql: bool = True,
        include_php: bool = True,
        include_mailpit: bool = False,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        normalized_template_code = str(template_code).strip().lower()
        stack_plan = self._build_stack_plan(web_server, include_mysql, include_php, include_mailpit)

        if not self.project_path_tool.is_valid_project_code(normalized_code):
            return {
                "success": False,
                "error": QUICK_APP_ERROR_INVALID_PROJECT_CODE,
                "project_code": normalized_code,
            }

        template_item = self.quick_app_template_tool.get_template(normalized_template_code)
        if template_item is None:
            return {
                "success": False,
                "error": QUICK_APP_ERROR_TEMPLATE_NOT_FOUND,
                "template_code": normalized_template_code,
            }

        existing_project = self.project_registry_repository.get_project(normalized_code)
        if existing_project is not None and not dry_run:
            return {
                "success": False,
                "error": QUICK_APP_ERROR_ALREADY_EXISTS,
                "project": existing_project,
            }

        plan_gate = self.plan_gate_service.can_create_project()
        if not dry_run and existing_project is None and not plan_gate.get("allowed", False):
            return {
                "success": False,
                "status": "blocked",
                "error": QUICK_APP_ERROR_COMMUNITY_SITE_LIMIT,
                "message": plan_gate.get("message"),
                "project_code": normalized_code,
                "template_code": normalized_template_code,
                "plan_gate": plan_gate,
            }

        runtime_family = str(template_item.get("runtime_family", "")).strip()
        active_runtime = self.runtime_version_repository.get_active_version(runtime_family)
        provisioning_plan = self._build_provisioning_plan(
            project_code=normalized_code,
            domain=domain,
            port=port,
            runtime_family=runtime_family,
            stack_plan=stack_plan,
            active_runtime=active_runtime,
        )
        if active_runtime is None:
            if dry_run:
                plan = self.quick_app_template_tool.build_plan(normalized_code, project_name, normalized_template_code, domain, port, stack_plan)
                return {
                    "success": True,
                    "status": QUICK_APP_STATUS_PLANNED,
                    "message": QUICK_APP_MESSAGE_DRY_RUN,
                    "project_code": normalized_code,
                    "template_code": normalized_template_code,
                    "runtime_family": runtime_family,
                    "runtime_required": True,
                    "runtime_error": QUICK_APP_ERROR_ACTIVE_RUNTIME_NOT_FOUND,
                    "plan": plan,
                    "plan_gate": plan_gate,
                    "stack_plan": stack_plan,
                    "stack_label": stack_plan.get("label"),
                    "provisioning_plan": provisioning_plan,
                    "provisioning_status": provisioning_plan.get("status"),
                    "database_label": provisioning_plan.get("database_wizard", {}).get("label", ""),
                }
            return {
                "success": False,
                "error": QUICK_APP_ERROR_ACTIVE_RUNTIME_NOT_FOUND,
                "runtime_family": runtime_family,
                "provisioning_plan": provisioning_plan,
                "provisioning_status": provisioning_plan.get("status"),
                "database_label": provisioning_plan.get("database_wizard", {}).get("label", ""),
            }

        plan = self.quick_app_template_tool.build_plan(normalized_code, project_name, normalized_template_code, domain, port, stack_plan)
        if not plan.get("safe", False):
            return {
                "success": False,
                "error": QUICK_APP_ERROR_PATH_BLOCKED,
                "plan": plan,
            }

        project_payload = self._build_project_payload(plan, template_item, active_runtime, stack_plan)
        if dry_run:
            return {
                "success": True,
                "status": QUICK_APP_STATUS_PLANNED,
                "message": QUICK_APP_MESSAGE_DRY_RUN,
                "project_code": normalized_code,
                "template_code": normalized_template_code,
                "runtime_family": runtime_family,
                "active_runtime": active_runtime,
                "plan": plan,
                "project": project_payload,
                "plan_gate": plan_gate,
                "stack_plan": stack_plan,
                "stack_label": stack_plan.get("label"),
                "provisioning_plan": provisioning_plan,
                "provisioning_status": provisioning_plan.get("status"),
                "database_label": provisioning_plan.get("database_wizard", {}).get("label", ""),
            }

        create_result = self.quick_app_template_tool.create_scaffold(normalized_code, project_name, normalized_template_code, domain, port, stack_plan)
        if not create_result.get("success", False):
            return {
                "success": False,
                "error": QUICK_APP_ERROR_PATH_BLOCKED,
                "create_result": create_result,
            }

        stored_project = self.project_registry_repository.upsert_project(project_payload)
        stored_record = self.quick_app_registry_repository.append_record(
            {
                "status": QUICK_APP_STATUS_CREATED,
                "project_code": normalized_code,
                "template_code": normalized_template_code,
                "runtime_family": runtime_family,
                "runtime_component_code": active_runtime.get("component_code"),
                "stack_plan": stack_plan,
                "project_path": plan.get("project_path"),
                "document_root": plan.get("document_root"),
                "file_count": create_result.get("file_count", 0),
            }
        )

        hosts_auto_result = self._sync_hosts_after_create(stored_project)

        return {
            "success": True,
            "status": QUICK_APP_STATUS_CREATED,
            "message": QUICK_APP_MESSAGE_CREATED,
            "project_code": normalized_code,
            "template_code": normalized_template_code,
            "runtime_family": runtime_family,
            "project": stored_project,
            "record": stored_record,
            "create_result": create_result,
            "hosts_auto": hosts_auto_result,
            "plan_gate": plan_gate,
            "stack_plan": stack_plan,
            "stack_label": stack_plan.get("label"),
            "provisioning_plan": provisioning_plan,
            "provisioning_status": provisioning_plan.get("status"),
            "database_label": provisioning_plan.get("database_wizard", {}).get("label", ""),
        }

    def _build_provisioning_plan(
        self,
        project_code: str,
        domain: str,
        port: int,
        runtime_family: str,
        stack_plan: dict[str, Any],
        active_runtime: dict[str, Any] | None,
    ) -> dict[str, Any]:
        if self.stack_provisioning_service is None:
            return {
                "success": True,
                "status": "skipped",
                "message": "stack provisioning service is not configured",
            }

        return self.stack_provisioning_service.build_plan(
            project_code=project_code,
            domain=domain,
            port=port,
            runtime_family=runtime_family,
            stack_plan=stack_plan,
            active_runtime=active_runtime,
        )

    def _build_stack_plan(self, web_server: str, include_mysql: bool, include_php: bool, include_mailpit: bool) -> dict[str, Any]:
        normalized_web_server = str(web_server).strip().lower()
        if normalized_web_server not in {self.WEB_SERVER_APACHE, self.WEB_SERVER_NGINX}:
            normalized_web_server = self.WEB_SERVER_APACHE

        services: list[str] = [normalized_web_server]
        if include_mysql:
            services.append(self.SERVICE_MYSQL)
        if include_php:
            services.append(self.SERVICE_PHP)
        if include_mailpit:
            services.append(self.SERVICE_MAILPIT)

        label_parts = [normalized_web_server.title()]
        if include_mysql:
            label_parts.append("MySQL")
        if include_php:
            label_parts.append("PHP")
        if include_mailpit:
            label_parts.append("Mailpit")

        return {
            "web_server": normalized_web_server,
            "include_mysql": bool(include_mysql),
            "include_php": bool(include_php),
            "include_mailpit": bool(include_mailpit),
            "mysql": bool(include_mysql),
            "php": bool(include_php),
            "mailpit": bool(include_mailpit),
            "services": services,
            "label": " + ".join(label_parts),
            "mode": "selected_stack",
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
        plan: dict[str, Any],
        template_item: dict[str, Any],
        active_runtime: dict[str, Any],
        stack_plan: dict[str, Any],
    ) -> dict[str, Any]:
        created_at = datetime.now(timezone.utc).isoformat()
        return {
            "code": plan.get("project_code"),
            "name": plan.get("project_name"),
            "runtime_family": template_item.get("runtime_family"),
            "runtime_component_code": active_runtime.get("component_code"),
            "runtime_version": active_runtime.get("version"),
            "runtime_adapter": active_runtime.get("runtime_adapter"),
            "stack_plan": stack_plan,
            "web_server": stack_plan.get("web_server"),
            "selected_services": stack_plan.get("services"),
            "project_path": plan.get("project_path"),
            "document_root": plan.get("document_root"),
            "domain": plan.get("domain"),
            "port": plan.get("port"),
            "template_code": template_item.get("code"),
            "created_from": "quick_app_service",
            "created_at": created_at,
        }
