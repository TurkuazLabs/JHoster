# 📄 Dosya Yolu: E:\JHoster\app\agent\services\nginx_reload_service.py
# 📌 Amac: JHoster Nginx reload is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Validate kaydindan hedef config bulur, reload planlar ve registry kaydini olusturur
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    NGINX_RELOAD_ERROR_TARGET_NOT_FOUND,
    NGINX_RELOAD_ERROR_VALIDATION_NOT_FOUND,
    NGINX_RELOAD_ERROR_VALIDATION_NOT_VALID,
    NGINX_RELOAD_STATUS_RELOADED,
    NGINX_VALIDATE_STATUS_VALID,
)
from repositories.nginx_reload_registry_repository import NginxReloadRegistryRepository
from repositories.nginx_validate_registry_repository import NginxValidateRegistryRepository
from tools.nginx_reload_tool import NginxReloadTool
from tools.project_path_tool import ProjectPathTool


class NginxReloadService:
    def __init__(
        self,
        root_path: Path,
        nginx_validate_registry_repository: NginxValidateRegistryRepository,
        nginx_reload_registry_repository: NginxReloadRegistryRepository,
        project_path_tool: ProjectPathTool,
        nginx_reload_tool: NginxReloadTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.nginx_validate_registry_repository = nginx_validate_registry_repository
        self.nginx_reload_registry_repository = nginx_reload_registry_repository
        self.project_path_tool = project_path_tool
        self.nginx_reload_tool = nginx_reload_tool

    def list_reload_records(self) -> dict[str, Any]:
        reload_records = self.nginx_reload_registry_repository.list_reload_records()

        return {
            "success": True,
            "count": len(reload_records),
            "reload_records": reload_records,
        }

    def get_latest_reload(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        reload_item = self.nginx_reload_registry_repository.get_latest_reload(normalized_code)

        if reload_item is None:
            return {
                "success": False,
                "error": NGINX_RELOAD_ERROR_VALIDATION_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "reload_record": reload_item,
        }

    def plan_project_reload(self, project_code: str) -> dict[str, Any]:
        return self.reload_project_config(project_code=project_code, dry_run=True)

    def reload_project_config(self, project_code: str, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        validation_item = self.nginx_validate_registry_repository.get_latest_validation(normalized_code)

        if validation_item is None:
            return {
                "success": False,
                "error": NGINX_RELOAD_ERROR_VALIDATION_NOT_FOUND,
                "project_code": normalized_code,
            }

        if validation_item.get("status") != NGINX_VALIDATE_STATUS_VALID:
            return {
                "success": False,
                "error": NGINX_RELOAD_ERROR_VALIDATION_NOT_VALID,
                "project_code": normalized_code,
                "validation_status": validation_item.get("status"),
            }

        target_config_file = self._resolve_target_config_file(validation_item)
        if not target_config_file.is_file():
            return {
                "success": False,
                "error": NGINX_RELOAD_ERROR_TARGET_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(target_config_file),
            }

        reload_result = self.nginx_reload_tool.reload_config(
            project_code=normalized_code,
            validated_config_file=target_config_file,
            dry_run=dry_run,
        )

        if reload_result.get("status") == NGINX_RELOAD_STATUS_RELOADED:
            stored_record = self.nginx_reload_registry_repository.append_reload_record(
                self._build_reload_record(validation_item, reload_result)
            )
            reload_result["reload_record"] = stored_record

        return reload_result

    def _resolve_target_config_file(self, validation_item: dict[str, Any]) -> Path:
        raw_target_file = str(validation_item.get("target_file", "")).strip()
        normalized_target_file = raw_target_file.replace("\\", "/")
        target_file_path = Path(normalized_target_file)

        if target_file_path.is_absolute():
            return target_file_path.resolve()

        return (self.root_path / target_file_path).resolve()

    def _build_reload_record(
        self,
        validation_item: dict[str, Any],
        reload_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = reload_result.get("plan", {})

        return {
            "project_code": validation_item.get("project_code"),
            "project_name": validation_item.get("project_name"),
            "domain": validation_item.get("domain"),
            "port": validation_item.get("port"),
            "target_file": plan.get("target_file"),
            "reload_mode": plan.get("reload_mode"),
            "command_label": plan.get("command_label"),
            "shell_execution": plan.get("shell_execution"),
            "status": reload_result.get("status"),
            "reload_result": reload_result.get("reload_result"),
            "reloaded_from": "nginx_reload_service",
            "reloaded_at": reload_result.get("reloaded_at"),
        }
