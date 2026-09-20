# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_real_reload_service.py
# 📌 Amac: Apache real reload adapter is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Real validate kaydi, executable kaydi, publish kaydi ve real reload tool arasindaki akisi koordine eder
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    APACHE_REAL_RELOAD_ERROR_EXECUTABLE_NOT_FOUND,
    APACHE_REAL_RELOAD_ERROR_PUBLISH_NOT_FOUND,
    APACHE_REAL_RELOAD_ERROR_TARGET_NOT_FOUND,
    APACHE_REAL_RELOAD_ERROR_VALIDATION_NOT_FOUND,
    APACHE_REAL_RELOAD_STATUS_REJECTED,
    APACHE_REAL_RELOAD_STATUS_RELOADED,
    APACHE_REAL_RELOAD_STATUS_SKIPPED,
)
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_real_reload_registry_repository import ApacheRealReloadRegistryRepository
from repositories.apache_real_validate_registry_repository import ApacheRealValidateRegistryRepository
from tools.apache_real_reloader_tool import ApacheRealReloaderTool
from tools.project_path_tool import ProjectPathTool


class ApacheRealReloadService:
    def __init__(
        self,
        root_path: Path,
        apache_publish_registry_repository: ApachePublishRegistryRepository,
        apache_executable_registry_repository: ApacheExecutableRegistryRepository,
        apache_real_validate_registry_repository: ApacheRealValidateRegistryRepository,
        apache_real_reload_registry_repository: ApacheRealReloadRegistryRepository,
        project_path_tool: ProjectPathTool,
        apache_real_reloader_tool: ApacheRealReloaderTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.apache_publish_registry_repository = apache_publish_registry_repository
        self.apache_executable_registry_repository = apache_executable_registry_repository
        self.apache_real_validate_registry_repository = apache_real_validate_registry_repository
        self.apache_real_reload_registry_repository = apache_real_reload_registry_repository
        self.project_path_tool = project_path_tool
        self.apache_real_reloader_tool = apache_real_reloader_tool

    def list_real_reload_records(self) -> dict[str, Any]:
        reload_records = self.apache_real_reload_registry_repository.list_real_reload_records()

        return {
            "success": True,
            "count": len(reload_records),
            "real_reload_records": reload_records,
        }

    def get_latest_real_reload(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        reload_item = self.apache_real_reload_registry_repository.get_latest_real_reload(normalized_code)

        if reload_item is None:
            return {
                "success": False,
                "error": APACHE_REAL_RELOAD_ERROR_VALIDATION_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "real_reload_record": reload_item,
        }

    def plan_real_reload(self, project_code: str) -> dict[str, Any]:
        return self.reload_with_real_adapter(
            project_code=project_code,
            dry_run=True,
            allow_real_execution=False,
        )

    def reload_with_real_adapter(
        self,
        project_code: str,
        dry_run: bool,
        allow_real_execution: bool,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        published_item = self.apache_publish_registry_repository.get_latest_publish(normalized_code)

        if published_item is None:
            return {
                "success": False,
                "error": APACHE_REAL_RELOAD_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        executable_record = self.apache_executable_registry_repository.get_latest_detection()
        if executable_record is None:
            return {
                "success": False,
                "error": APACHE_REAL_RELOAD_ERROR_EXECUTABLE_NOT_FOUND,
                "project_code": normalized_code,
            }

        validation_record = self.apache_real_validate_registry_repository.get_latest_real_validation(normalized_code)
        if validation_record is None:
            return {
                "success": False,
                "error": APACHE_REAL_RELOAD_ERROR_VALIDATION_NOT_FOUND,
                "project_code": normalized_code,
            }

        target_config_file = self._resolve_target_config_file(published_item)
        if not target_config_file.is_file():
            return {
                "success": False,
                "error": APACHE_REAL_RELOAD_ERROR_TARGET_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(target_config_file),
            }

        reload_result = self.apache_real_reloader_tool.reload_with_real_adapter(
            project_code=normalized_code,
            published_config_file=target_config_file,
            executable_record=executable_record,
            validation_record=validation_record,
            dry_run=dry_run,
            allow_real_execution=allow_real_execution,
        )

        if reload_result.get("status") in [
            APACHE_REAL_RELOAD_STATUS_RELOADED,
            APACHE_REAL_RELOAD_STATUS_SKIPPED,
            APACHE_REAL_RELOAD_STATUS_REJECTED,
        ]:
            stored_record = self.apache_real_reload_registry_repository.append_real_reload_record(
                self._build_real_reload_record(
                    published_item=published_item,
                    executable_record=executable_record,
                    validation_record=validation_record,
                    reload_result=reload_result,
                )
            )
            reload_result["real_reload_record"] = stored_record

        return reload_result

    def _resolve_target_config_file(self, published_item: dict[str, Any]) -> Path:
        raw_target_file = str(published_item.get("target_file", "")).strip()
        normalized_target_file = raw_target_file.replace("\\", "/")
        target_file_path = Path(normalized_target_file)

        if target_file_path.is_absolute():
            return target_file_path.resolve()

        return (self.root_path / target_file_path).resolve()

    def _build_real_reload_record(
        self,
        published_item: dict[str, Any],
        executable_record: dict[str, Any],
        validation_record: dict[str, Any],
        reload_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = reload_result.get("plan", {})
        reload_execution_result = reload_result.get("reload_result", {})

        return {
            "project_code": published_item.get("project_code"),
            "project_name": published_item.get("project_name"),
            "domain": published_item.get("domain"),
            "port": published_item.get("port"),
            "published_config_file": plan.get("published_config_file"),
            "main_config_file": plan.get("main_config_file"),
            "apache_executable_file": plan.get("apache_executable_file"),
            "apache_executable_source": executable_record.get("source"),
            "validation_status": validation_record.get("status"),
            "validation_return_code": validation_record.get("return_code"),
            "reload_mode": plan.get("reload_mode"),
            "command_label": plan.get("command_label"),
            "shell_execution": plan.get("shell_execution"),
            "real_apache_execution_requested": plan.get("real_apache_execution_requested"),
            "real_apache_execution": reload_execution_result.get("real_apache_execution", plan.get("real_apache_execution")),
            "return_code": reload_execution_result.get("return_code"),
            "status": reload_result.get("status"),
            "reload_result": reload_execution_result,
            "reloaded_from": "apache_real_reload_service",
            "reloaded_at": reload_result.get("reloaded_at"),
        }
