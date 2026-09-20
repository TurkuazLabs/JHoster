# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_validate_service.py
# 📌 Amac: JHoster Apache config validate is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Publish kaydindan hedef Apache config bulur, validate planlar ve registry kaydini olusturur
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    APACHE_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
    APACHE_VALIDATE_ERROR_TARGET_NOT_FOUND,
    APACHE_VALIDATE_STATUS_INVALID,
    APACHE_VALIDATE_STATUS_VALID,
)
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_validate_registry_repository import ApacheValidateRegistryRepository
from tools.apache_config_validator_tool import ApacheConfigValidatorTool
from tools.project_path_tool import ProjectPathTool


class ApacheValidateService:
    def __init__(
        self,
        root_path: Path,
        apache_publish_registry_repository: ApachePublishRegistryRepository,
        apache_validate_registry_repository: ApacheValidateRegistryRepository,
        project_path_tool: ProjectPathTool,
        apache_config_validator_tool: ApacheConfigValidatorTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.apache_publish_registry_repository = apache_publish_registry_repository
        self.apache_validate_registry_repository = apache_validate_registry_repository
        self.project_path_tool = project_path_tool
        self.apache_config_validator_tool = apache_config_validator_tool

    def list_validation_records(self) -> dict[str, Any]:
        validation_records = self.apache_validate_registry_repository.list_validation_records()

        return {
            "success": True,
            "count": len(validation_records),
            "validation_records": validation_records,
        }

    def get_latest_validation(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        validation_item = self.apache_validate_registry_repository.get_latest_validation(normalized_code)

        if validation_item is None:
            return {
                "success": False,
                "error": APACHE_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "validation_record": validation_item,
        }

    def plan_project_validation(self, project_code: str) -> dict[str, Any]:
        return self.validate_project_config(project_code=project_code, dry_run=True)

    def validate_project_config(self, project_code: str, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        published_item = self.apache_publish_registry_repository.get_latest_publish(normalized_code)

        if published_item is None:
            return {
                "success": False,
                "error": APACHE_VALIDATE_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        target_config_file = self._resolve_target_config_file(published_item)
        if not target_config_file.is_file():
            return {
                "success": False,
                "error": APACHE_VALIDATE_ERROR_TARGET_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(target_config_file),
            }

        validation_result = self.apache_config_validator_tool.validate_config(
            project_code=normalized_code,
            published_config_file=target_config_file,
            dry_run=dry_run,
        )

        if validation_result.get("status") in [APACHE_VALIDATE_STATUS_VALID, APACHE_VALIDATE_STATUS_INVALID]:
            stored_record = self.apache_validate_registry_repository.append_validation_record(
                self._build_validation_record(published_item, validation_result)
            )
            validation_result["validation_record"] = stored_record

        return validation_result

    def _resolve_target_config_file(self, published_item: dict[str, Any]) -> Path:
        raw_target_file = str(published_item.get("target_file", "")).strip()
        normalized_target_file = raw_target_file.replace("\\", "/")
        target_file_path = Path(normalized_target_file)

        if target_file_path.is_absolute():
            return target_file_path.resolve()

        return (self.root_path / target_file_path).resolve()

    def _build_validation_record(
        self,
        published_item: dict[str, Any],
        validation_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = validation_result.get("plan", {})

        return {
            "project_code": published_item.get("project_code"),
            "project_name": published_item.get("project_name"),
            "domain": published_item.get("domain"),
            "port": published_item.get("port"),
            "target_file": plan.get("target_file"),
            "web_server": "apache",
            "config_syntax": "apache_vhost",
            "validation_mode": plan.get("validation_mode"),
            "status": validation_result.get("status"),
            "checks": validation_result.get("checks", []),
            "validated_from": "apache_validate_service",
            "validated_at": validation_result.get("validated_at"),
        }
