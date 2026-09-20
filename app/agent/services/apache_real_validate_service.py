# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_real_validate_service.py
# 📌 Amac: Apache real validate adapter is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Publish kaydi, executable kaydi ve real validator tool arasindaki akisi koordine eder
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    APACHE_REAL_VALIDATE_ERROR_EXECUTABLE_NOT_FOUND,
    APACHE_REAL_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
    APACHE_REAL_VALIDATE_ERROR_TARGET_NOT_FOUND,
    APACHE_REAL_VALIDATE_STATUS_INVALID,
    APACHE_REAL_VALIDATE_STATUS_SKIPPED,
    APACHE_REAL_VALIDATE_STATUS_VALID,
)
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_real_validate_registry_repository import ApacheRealValidateRegistryRepository
from tools.apache_real_validator_tool import ApacheRealValidatorTool
from tools.project_path_tool import ProjectPathTool


class ApacheRealValidateService:
    def __init__(
        self,
        root_path: Path,
        apache_publish_registry_repository: ApachePublishRegistryRepository,
        apache_executable_registry_repository: ApacheExecutableRegistryRepository,
        apache_real_validate_registry_repository: ApacheRealValidateRegistryRepository,
        project_path_tool: ProjectPathTool,
        apache_real_validator_tool: ApacheRealValidatorTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.apache_publish_registry_repository = apache_publish_registry_repository
        self.apache_executable_registry_repository = apache_executable_registry_repository
        self.apache_real_validate_registry_repository = apache_real_validate_registry_repository
        self.project_path_tool = project_path_tool
        self.apache_real_validator_tool = apache_real_validator_tool

    def list_real_validation_records(self) -> dict[str, Any]:
        validation_records = self.apache_real_validate_registry_repository.list_real_validation_records()

        return {
            "success": True,
            "count": len(validation_records),
            "real_validation_records": validation_records,
        }

    def get_latest_real_validation(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        validation_item = self.apache_real_validate_registry_repository.get_latest_real_validation(normalized_code)

        if validation_item is None:
            return {
                "success": False,
                "error": APACHE_REAL_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "real_validation_record": validation_item,
        }

    def plan_real_validation(self, project_code: str) -> dict[str, Any]:
        return self.validate_with_real_adapter(
            project_code=project_code,
            dry_run=True,
            allow_real_execution=False,
        )

    def validate_with_real_adapter(
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
                "error": APACHE_REAL_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        executable_record = self.apache_executable_registry_repository.get_latest_detection()
        if executable_record is None:
            return {
                "success": False,
                "error": APACHE_REAL_VALIDATE_ERROR_EXECUTABLE_NOT_FOUND,
                "project_code": normalized_code,
            }

        target_config_file = self._resolve_target_config_file(published_item)
        if not target_config_file.is_file():
            return {
                "success": False,
                "error": APACHE_REAL_VALIDATE_ERROR_TARGET_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(target_config_file),
            }

        validation_result = self.apache_real_validator_tool.validate_with_real_adapter(
            project_code=normalized_code,
            published_config_file=target_config_file,
            executable_record=executable_record,
            dry_run=dry_run,
            allow_real_execution=allow_real_execution,
        )

        if validation_result.get("status") in [
            APACHE_REAL_VALIDATE_STATUS_VALID,
            APACHE_REAL_VALIDATE_STATUS_INVALID,
            APACHE_REAL_VALIDATE_STATUS_SKIPPED,
        ]:
            stored_record = self.apache_real_validate_registry_repository.append_real_validation_record(
                self._build_real_validation_record(
                    published_item=published_item,
                    executable_record=executable_record,
                    validation_result=validation_result,
                )
            )
            validation_result["real_validation_record"] = stored_record

        return validation_result

    def _resolve_target_config_file(self, published_item: dict[str, Any]) -> Path:
        raw_target_file = str(published_item.get("target_file", "")).strip()
        normalized_target_file = raw_target_file.replace("\\", "/")
        target_file_path = Path(normalized_target_file)

        if target_file_path.is_absolute():
            return target_file_path.resolve()

        return (self.root_path / target_file_path).resolve()

    def _build_real_validation_record(
        self,
        published_item: dict[str, Any],
        executable_record: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = validation_result.get("plan", {})
        execution_result = validation_result.get("execution_result", {})

        return {
            "project_code": published_item.get("project_code"),
            "project_name": published_item.get("project_name"),
            "domain": published_item.get("domain"),
            "port": published_item.get("port"),
            "published_config_file": plan.get("published_config_file"),
            "main_config_file": plan.get("main_config_file"),
            "apache_executable_file": plan.get("apache_executable_file"),
            "apache_executable_source": executable_record.get("source"),
            "validation_mode": plan.get("validation_mode"),
            "command_label": plan.get("command_label"),
            "shell_execution": plan.get("shell_execution"),
            "real_apache_execution_requested": plan.get("real_apache_execution_requested"),
            "real_apache_execution": execution_result.get("real_apache_execution", plan.get("real_apache_execution")),
            "return_code": execution_result.get("return_code"),
            "status": validation_result.get("status"),
            "validated_from": "apache_real_validate_service",
            "validated_at": validation_result.get("validated_at"),
        }
