# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_vhost_service.py
# 📌 Amac: JHoster Apache virtual host is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Project kaydindan guvenli Apache vhost planlama ve config uretme akisini yonetir
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    APACHE_VHOST_ERROR_INVALID_DOMAIN,
    APACHE_VHOST_ERROR_PATH_BLOCKED,
    APACHE_VHOST_ERROR_PROJECT_NOT_FOUND,
    APACHE_VHOST_MESSAGE_DRY_RUN,
    APACHE_VHOST_MESSAGE_GENERATED,
    APACHE_VHOST_STATUS_GENERATED,
    APACHE_VHOST_STATUS_PLANNED,
)
from repositories.apache_vhost_registry_repository import ApacheVhostRegistryRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from tools.apache_vhost_config_tool import ApacheVhostConfigTool
from tools.project_path_tool import ProjectPathTool


class ApacheVhostService:
    def __init__(
        self,
        project_registry_repository: ProjectRegistryRepository,
        apache_vhost_registry_repository: ApacheVhostRegistryRepository,
        project_path_tool: ProjectPathTool,
        apache_vhost_config_tool: ApacheVhostConfigTool,
    ) -> None:
        self.project_registry_repository = project_registry_repository
        self.apache_vhost_registry_repository = apache_vhost_registry_repository
        self.project_path_tool = project_path_tool
        self.apache_vhost_config_tool = apache_vhost_config_tool

    def list_virtual_hosts(self) -> dict[str, Any]:
        virtual_hosts = self.apache_vhost_registry_repository.list_virtual_hosts()

        return {
            "success": True,
            "count": len(virtual_hosts),
            "apache_virtual_hosts": virtual_hosts,
        }

    def get_virtual_host(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        virtual_host_item = self.apache_vhost_registry_repository.get_virtual_host(normalized_code)

        if virtual_host_item is None:
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "apache_virtual_host": virtual_host_item,
        }

    def plan_virtual_host(self, project_code: str, domain: str, port: int) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        project_item = self.project_registry_repository.get_project(normalized_code)

        if project_item is None:
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        plan = self.apache_vhost_config_tool.build_virtual_host_plan(project_item, domain, port)
        if not plan.get("valid_domain", False):
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_INVALID_DOMAIN,
                "plan": plan,
            }

        if not plan.get("safe", False):
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_PATH_BLOCKED,
                "plan": plan,
            }

        return {
            "success": True,
            "status": APACHE_VHOST_STATUS_PLANNED,
            "message": APACHE_VHOST_MESSAGE_DRY_RUN,
            "apache_virtual_host_plan": plan,
        }

    def generate_virtual_host(self, project_code: str, domain: str, port: int, dry_run: bool) -> dict[str, Any]:
        plan_response = self.plan_virtual_host(project_code, domain, port)
        if not plan_response.get("success", False):
            return plan_response

        plan = plan_response.get("apache_virtual_host_plan", {})
        if dry_run:
            return plan_response

        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        project_item = self.project_registry_repository.get_project(normalized_code)
        if project_item is None:
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_PROJECT_NOT_FOUND,
                "project_code": normalized_code,
            }

        generate_result = self.apache_vhost_config_tool.generate_config_file(project_item, domain, port)
        if not generate_result.get("success", False):
            return {
                "success": False,
                "error": APACHE_VHOST_ERROR_PATH_BLOCKED,
                "generate_result": generate_result,
            }

        virtual_host_payload = self._build_virtual_host_payload(project_item, generate_result.get("plan", plan))
        stored_virtual_host = self.apache_vhost_registry_repository.upsert_virtual_host(virtual_host_payload)

        return {
            "success": True,
            "status": APACHE_VHOST_STATUS_GENERATED,
            "message": APACHE_VHOST_MESSAGE_GENERATED,
            "apache_virtual_host": stored_virtual_host,
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
            "web_server": "apache",
            "config_syntax": "apache_vhost",
            "runtime_family": project_item.get("runtime_family"),
            "runtime_version": project_item.get("runtime_version"),
            "runtime_adapter": project_item.get("runtime_adapter"),
            "generated_from": "apache_vhost_service",
            "generated_at": generated_at,
        }
