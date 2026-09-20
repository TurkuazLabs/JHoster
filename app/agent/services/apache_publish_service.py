# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_publish_service.py
# 📌 Amac: JHoster Apache virtual host publish is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache vhost kaydindan kaynak config bulur, publish planlar ve registry kaydini olusturur
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    APACHE_PUBLISH_ERROR_PATH_BLOCKED,
    APACHE_PUBLISH_ERROR_SOURCE_NOT_FOUND,
    APACHE_PUBLISH_ERROR_VHOST_NOT_FOUND,
    APACHE_PUBLISH_STATUS_PUBLISHED,
)
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_vhost_registry_repository import ApacheVhostRegistryRepository
from tools.apache_config_publisher_tool import ApacheConfigPublisherTool
from tools.project_path_tool import ProjectPathTool


class ApachePublishService:
    def __init__(
        self,
        root_path: Path,
        apache_vhost_registry_repository: ApacheVhostRegistryRepository,
        apache_publish_registry_repository: ApachePublishRegistryRepository,
        project_path_tool: ProjectPathTool,
        apache_config_publisher_tool: ApacheConfigPublisherTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.apache_vhost_registry_repository = apache_vhost_registry_repository
        self.apache_publish_registry_repository = apache_publish_registry_repository
        self.project_path_tool = project_path_tool
        self.apache_config_publisher_tool = apache_config_publisher_tool

    def list_published_configs(self) -> dict[str, Any]:
        published_configs = self.apache_publish_registry_repository.list_published_configs()

        return {
            "success": True,
            "count": len(published_configs),
            "published_configs": published_configs,
        }

    def get_latest_publish(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        published_item = self.apache_publish_registry_repository.get_latest_publish(normalized_code)

        if published_item is None:
            return {
                "success": False,
                "error": APACHE_PUBLISH_ERROR_VHOST_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "published_config": published_item,
        }

    def plan_project_publish(
        self,
        project_code: str,
        target_dir: str,
    ) -> dict[str, Any]:
        return self.publish_project_vhost(
            project_code=project_code,
            target_dir=target_dir,
            dry_run=True,
        )

    def publish_project_vhost(
        self,
        project_code: str,
        target_dir: str,
        dry_run: bool,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        virtual_host_item = self.apache_vhost_registry_repository.get_virtual_host(normalized_code)

        if virtual_host_item is None:
            return {
                "success": False,
                "error": APACHE_PUBLISH_ERROR_VHOST_NOT_FOUND,
                "project_code": normalized_code,
            }

        source_config_file = self._resolve_source_config_file(virtual_host_item)
        if not source_config_file.is_file():
            return {
                "success": False,
                "error": APACHE_PUBLISH_ERROR_SOURCE_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(source_config_file),
            }

        publish_result = self.apache_config_publisher_tool.publish_config(
            project_code=normalized_code,
            source_config_file=source_config_file,
            target_dir=target_dir,
            dry_run=dry_run,
        )

        if not publish_result.get("success", False):
            return {
                "success": False,
                "error": APACHE_PUBLISH_ERROR_PATH_BLOCKED,
                "publish_result": publish_result,
            }

        if publish_result.get("status") == APACHE_PUBLISH_STATUS_PUBLISHED:
            stored_record = self.apache_publish_registry_repository.append_publish_record(
                self._build_publish_record(virtual_host_item, publish_result)
            )
            publish_result["published_config"] = stored_record

        return publish_result

    def _resolve_source_config_file(self, virtual_host_item: dict[str, Any]) -> Path:
        raw_config_file = str(virtual_host_item.get("config_file", "")).strip()
        normalized_config_file = raw_config_file.replace("\\", "/")
        config_file_path = Path(normalized_config_file)

        if config_file_path.is_absolute():
            return config_file_path.resolve()

        return (self.root_path / config_file_path).resolve()

    def _build_publish_record(
        self,
        virtual_host_item: dict[str, Any],
        publish_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = publish_result.get("plan", {})

        return {
            "project_code": virtual_host_item.get("project_code"),
            "project_name": virtual_host_item.get("project_name"),
            "domain": virtual_host_item.get("domain"),
            "port": virtual_host_item.get("port"),
            "source_config_file": plan.get("source_config_file"),
            "target_file": plan.get("target_file"),
            "web_server": "apache",
            "config_syntax": "apache_vhost",
            "runtime_family": virtual_host_item.get("runtime_family"),
            "runtime_version": virtual_host_item.get("runtime_version"),
            "runtime_adapter": virtual_host_item.get("runtime_adapter"),
            "checksum": publish_result.get("checksum"),
            "backup": publish_result.get("backup"),
            "status": publish_result.get("status"),
            "published_from": "apache_publish_service",
            "published_at": publish_result.get("published_at"),
        }
