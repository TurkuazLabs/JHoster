# 📄 Dosya Yolu: E:/JHoster/app/agent/services/hosts_auto_service.py
# 📌 Amac: JHoster projeleri icin otomatik Windows hosts senkron, inspect ve repair is kurallarini yonetir
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Aktif projelerden domain toplar, imzali hosts blok planlar, eksik domainleri denetler, repair uygular ve Quick App akisina baglanir
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import HOSTS_AUTO_DEFAULT_IP
from repositories.hosts_auto_registry_repository import HostsAutoRegistryRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from tools.hosts_auto_file_tool import HostsAutoFileTool
from tools.project_path_tool import ProjectPathTool


class HostsAutoService:
    def __init__(
        self,
        project_registry_repository: ProjectRegistryRepository,
        hosts_auto_registry_repository: HostsAutoRegistryRepository,
        project_path_tool: ProjectPathTool,
        hosts_auto_file_tool: HostsAutoFileTool,
    ) -> None:
        self.project_registry_repository = project_registry_repository
        self.hosts_auto_registry_repository = hosts_auto_registry_repository
        self.project_path_tool = project_path_tool
        self.hosts_auto_file_tool = hosts_auto_file_tool

    def list_sync_records(self) -> dict[str, Any]:
        sync_records = self.hosts_auto_registry_repository.list_sync_records()
        return {
            "success": True,
            "count": len(sync_records),
            "sync_records": sync_records,
        }

    def get_latest_sync(self) -> dict[str, Any]:
        sync_record = self.hosts_auto_registry_repository.get_latest_sync()
        return {
            "success": sync_record is not None,
            "hosts_auto_sync": sync_record,
        }

    def inspect_all(self, ip_value: str | None, real_write: bool) -> dict[str, Any]:
        entries = self._collect_project_entries()
        return self.hosts_auto_file_tool.inspect_entries(
            entries=entries,
            ip_value=ip_value or HOSTS_AUTO_DEFAULT_IP,
            real_write=real_write,
        )

    def plan_repair_all(self, ip_value: str | None, real_write: bool) -> dict[str, Any]:
        return self.repair_all(ip_value=ip_value, real_write=real_write, dry_run=True)

    def repair_all(self, ip_value: str | None, real_write: bool, dry_run: bool) -> dict[str, Any]:
        entries = self._collect_project_entries()
        repair_result = self.hosts_auto_file_tool.repair_entries(
            entries=entries,
            ip_value=ip_value or HOSTS_AUTO_DEFAULT_IP,
            real_write=real_write,
            dry_run=dry_run,
        )

        if repair_result.get("success") is True and dry_run is False and repair_result.get("status") == "synced":
            stored_record = self.hosts_auto_registry_repository.append_sync_record(
                self._build_sync_record(repair_result)
            )
            repair_result["hosts_auto_sync"] = stored_record

        return repair_result

    def plan_sync_all(self, ip_value: str | None, real_write: bool) -> dict[str, Any]:
        return self.sync_all(ip_value=ip_value, real_write=real_write, dry_run=True)

    def sync_all(self, ip_value: str | None, real_write: bool, dry_run: bool) -> dict[str, Any]:
        entries = self._collect_project_entries()
        sync_result = self.hosts_auto_file_tool.sync_entries(
            entries=entries,
            ip_value=ip_value or HOSTS_AUTO_DEFAULT_IP,
            real_write=real_write,
            dry_run=dry_run,
        )

        if sync_result.get("success") is True and dry_run is False:
            stored_record = self.hosts_auto_registry_repository.append_sync_record(
                self._build_sync_record(sync_result)
            )
            sync_result["hosts_auto_sync"] = stored_record

        return sync_result

    def sync_project(
        self,
        project_payload: dict[str, Any],
        ip_value: str | None,
        real_write: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        sync_result = self.hosts_auto_file_tool.sync_entries(
            entries=[self._build_project_entry(project_payload)],
            ip_value=ip_value or HOSTS_AUTO_DEFAULT_IP,
            real_write=real_write,
            dry_run=dry_run,
        )

        if sync_result.get("success") is True and dry_run is False:
            stored_record = self.hosts_auto_registry_repository.append_sync_record(
                self._build_sync_record(sync_result)
            )
            sync_result["hosts_auto_sync"] = stored_record

        return sync_result

    def _collect_project_entries(self) -> list[dict[str, Any]]:
        entries: list[dict[str, Any]] = []
        for project_item in self.project_registry_repository.list_projects():
            entries.append(self._build_project_entry(project_item))
        return entries

    def _build_project_entry(self, project_item: dict[str, Any]) -> dict[str, Any]:
        project_code = self.project_path_tool.normalize_project_code(str(project_item.get("code", "")))
        domain = str(project_item.get("domain", "")).strip()
        if not domain and project_code:
            domain = f"{project_code}.test"

        return {
            "project_code": project_code,
            "project_name": project_item.get("name", project_code),
            "domain": domain,
        }

    def _build_sync_record(self, sync_result: dict[str, Any]) -> dict[str, Any]:
        plan = sync_result.get("plan", {})
        if not isinstance(plan, dict):
            plan = {}

        return {
            "status": sync_result.get("status"),
            "message": sync_result.get("message"),
            "target_file": plan.get("target_file"),
            "target_file_absolute": plan.get("target_file_absolute"),
            "entry_count": plan.get("entry_count"),
            "entries": plan.get("entries", []),
            "apply_mode": plan.get("apply_mode"),
            "real_hosts_file_write": plan.get("real_hosts_file_write"),
            "admin_required": plan.get("admin_required"),
            "admin_ok": plan.get("admin_ok"),
            "platform_ok": plan.get("platform_ok"),
            "backup": sync_result.get("backup"),
            "write_result": sync_result.get("write_result"),
            "inspect_before_repair": sync_result.get("inspect_before_repair"),
            "synced_at": sync_result.get("synced_at"),
        }
