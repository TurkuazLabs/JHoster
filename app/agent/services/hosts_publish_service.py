# 📄 Dosya Yolu: E:\JHoster\app\agent\services\hosts_publish_service.py
# 📌 Amac: JHoster hosts publish is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Virtual host kaydindan domain alir, hosts publish planlar ve registry kaydini olusturur
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import (
    HOSTS_PUBLISH_ERROR_VHOST_NOT_FOUND,
    HOSTS_PUBLISH_STATUS_PUBLISHED,
)
from repositories.hosts_publish_registry_repository import HostsPublishRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from tools.hosts_file_publisher_tool import HostsFilePublisherTool
from tools.project_path_tool import ProjectPathTool


class HostsPublishService:
    def __init__(
        self,
        virtual_host_registry_repository: VirtualHostRegistryRepository,
        hosts_publish_registry_repository: HostsPublishRegistryRepository,
        project_path_tool: ProjectPathTool,
        hosts_file_publisher_tool: HostsFilePublisherTool,
    ) -> None:
        self.virtual_host_registry_repository = virtual_host_registry_repository
        self.hosts_publish_registry_repository = hosts_publish_registry_repository
        self.project_path_tool = project_path_tool
        self.hosts_file_publisher_tool = hosts_file_publisher_tool

    def list_publish_records(self) -> dict[str, Any]:
        publish_records = self.hosts_publish_registry_repository.list_publish_records()

        return {
            "success": True,
            "count": len(publish_records),
            "publish_records": publish_records,
        }

    def get_latest_publish(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        publish_item = self.hosts_publish_registry_repository.get_latest_publish(normalized_code)

        if publish_item is None:
            return {
                "success": False,
                "error": HOSTS_PUBLISH_ERROR_VHOST_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "hosts_publish_record": publish_item,
        }

    def plan_project_hosts_publish(self, project_code: str, ip_value: str | None) -> dict[str, Any]:
        return self.publish_project_hosts(
            project_code=project_code,
            ip_value=ip_value,
            dry_run=True,
        )

    def publish_project_hosts(self, project_code: str, ip_value: str | None, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        virtual_host_item = self.virtual_host_registry_repository.get_virtual_host(normalized_code)

        if virtual_host_item is None:
            return {
                "success": False,
                "error": HOSTS_PUBLISH_ERROR_VHOST_NOT_FOUND,
                "project_code": normalized_code,
            }

        domain = str(virtual_host_item.get("domain", "")).strip()
        publish_result = self.hosts_file_publisher_tool.publish_entry(
            project_code=normalized_code,
            domain=domain,
            ip_value=ip_value,
            dry_run=dry_run,
        )

        if publish_result.get("status") == HOSTS_PUBLISH_STATUS_PUBLISHED:
            stored_record = self.hosts_publish_registry_repository.append_publish_record(
                self._build_publish_record(virtual_host_item, publish_result)
            )
            publish_result["hosts_publish_record"] = stored_record

        return publish_result

    def _build_publish_record(
        self,
        virtual_host_item: dict[str, Any],
        publish_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = publish_result.get("plan", {})

        return {
            "project_code": virtual_host_item.get("project_code"),
            "project_name": virtual_host_item.get("project_name"),
            "domain": plan.get("domain"),
            "ip": plan.get("ip"),
            "port": virtual_host_item.get("port"),
            "target_file": plan.get("target_file"),
            "host_line": plan.get("host_line"),
            "line_marker": plan.get("line_marker"),
            "real_hosts_file_write": plan.get("real_hosts_file_write"),
            "backup": publish_result.get("backup"),
            "write_result": publish_result.get("write_result"),
            "status": publish_result.get("status"),
            "published_from": "hosts_publish_service",
            "published_at": publish_result.get("published_at"),
        }
