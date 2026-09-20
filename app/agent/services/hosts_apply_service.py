# 📄 Dosya Yolu: E:\JHoster\app\agent\services\hosts_apply_service.py
# 📌 Amac: JHoster hosts apply ve rollback is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Virtual host kaydindan domain alir, admin guvenligi ile apply/rollback akisini koordine eder
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import (
    HOSTS_APPLY_ERROR_BACKUP_NOT_FOUND,
    HOSTS_APPLY_ERROR_RECORD_NOT_FOUND,
    HOSTS_APPLY_ERROR_VHOST_NOT_FOUND,
    HOSTS_APPLY_STATUS_APPLIED,
    HOSTS_APPLY_STATUS_ROLLED_BACK,
)
from repositories.hosts_apply_registry_repository import HostsApplyRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from tools.hosts_file_apply_tool import HostsFileApplyTool
from tools.project_path_tool import ProjectPathTool


class HostsApplyService:
    def __init__(
        self,
        virtual_host_registry_repository: VirtualHostRegistryRepository,
        hosts_apply_registry_repository: HostsApplyRegistryRepository,
        project_path_tool: ProjectPathTool,
        hosts_file_apply_tool: HostsFileApplyTool,
    ) -> None:
        self.virtual_host_registry_repository = virtual_host_registry_repository
        self.hosts_apply_registry_repository = hosts_apply_registry_repository
        self.project_path_tool = project_path_tool
        self.hosts_file_apply_tool = hosts_file_apply_tool

    def list_apply_records(self) -> dict[str, Any]:
        apply_records = self.hosts_apply_registry_repository.list_apply_records()
        rollback_records = self.hosts_apply_registry_repository.list_rollback_records()

        return {
            "success": True,
            "apply_count": len(apply_records),
            "rollback_count": len(rollback_records),
            "apply_records": apply_records,
            "rollback_records": rollback_records,
        }

    def get_latest_apply(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        apply_item = self.hosts_apply_registry_repository.get_latest_apply(normalized_code)

        if apply_item is None:
            return {
                "success": False,
                "error": HOSTS_APPLY_ERROR_RECORD_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "hosts_apply_record": apply_item,
        }

    def plan_project_hosts_apply(
        self,
        project_code: str,
        ip_value: str | None,
        real_write: bool,
    ) -> dict[str, Any]:
        return self.apply_project_hosts(
            project_code=project_code,
            ip_value=ip_value,
            real_write=real_write,
            dry_run=True,
        )

    def apply_project_hosts(
        self,
        project_code: str,
        ip_value: str | None,
        real_write: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        virtual_host_item = self.virtual_host_registry_repository.get_virtual_host(normalized_code)

        if virtual_host_item is None:
            return {
                "success": False,
                "error": HOSTS_APPLY_ERROR_VHOST_NOT_FOUND,
                "project_code": normalized_code,
            }

        domain = str(virtual_host_item.get("domain", "")).strip()
        apply_result = self.hosts_file_apply_tool.apply_entry(
            project_code=normalized_code,
            domain=domain,
            ip_value=ip_value,
            real_write=real_write,
            dry_run=dry_run,
        )

        if apply_result.get("status") == HOSTS_APPLY_STATUS_APPLIED:
            stored_record = self.hosts_apply_registry_repository.append_apply_record(
                self._build_apply_record(virtual_host_item, apply_result)
            )
            apply_result["hosts_apply_record"] = stored_record

        return apply_result

    def plan_project_hosts_rollback(self, project_code: str) -> dict[str, Any]:
        return self.rollback_project_hosts(project_code=project_code, dry_run=True)

    def rollback_project_hosts(self, project_code: str, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        latest_apply = self.hosts_apply_registry_repository.get_latest_apply(normalized_code)

        if latest_apply is None:
            return {
                "success": False,
                "error": HOSTS_APPLY_ERROR_RECORD_NOT_FOUND,
                "project_code": normalized_code,
            }

        backup = latest_apply.get("backup", {})
        if not isinstance(backup, dict) or backup.get("created") is not True:
            return {
                "success": False,
                "error": HOSTS_APPLY_ERROR_BACKUP_NOT_FOUND,
                "project_code": normalized_code,
                "hosts_apply_record": latest_apply,
            }

        rollback_result = self.hosts_file_apply_tool.rollback_entry(
            apply_record=latest_apply,
            dry_run=dry_run,
        )

        if rollback_result.get("status") == HOSTS_APPLY_STATUS_ROLLED_BACK:
            stored_record = self.hosts_apply_registry_repository.append_rollback_record(
                self._build_rollback_record(latest_apply, rollback_result)
            )
            rollback_result["hosts_rollback_record"] = stored_record

        return rollback_result

    def _build_apply_record(
        self,
        virtual_host_item: dict[str, Any],
        apply_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = apply_result.get("plan", {})

        return {
            "project_code": virtual_host_item.get("project_code"),
            "project_name": virtual_host_item.get("project_name"),
            "domain": plan.get("domain"),
            "ip": plan.get("ip"),
            "port": virtual_host_item.get("port"),
            "target_file": plan.get("target_file"),
            "target_file_absolute": plan.get("target_file_absolute"),
            "host_line": plan.get("host_line"),
            "line_marker": plan.get("line_marker"),
            "apply_mode": plan.get("apply_mode"),
            "real_hosts_file_write": plan.get("real_hosts_file_write"),
            "admin_required": plan.get("admin_required"),
            "admin_ok": plan.get("admin_ok"),
            "platform_ok": plan.get("platform_ok"),
            "backup": apply_result.get("backup"),
            "write_result": apply_result.get("write_result"),
            "status": apply_result.get("status"),
            "applied_from": "hosts_apply_service",
            "applied_at": apply_result.get("applied_at"),
        }

    def _build_rollback_record(
        self,
        apply_record: dict[str, Any],
        rollback_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = rollback_result.get("plan", {})

        return {
            "project_code": apply_record.get("project_code"),
            "project_name": apply_record.get("project_name"),
            "domain": apply_record.get("domain"),
            "target_file": plan.get("target_file"),
            "target_file_absolute": plan.get("target_file_absolute"),
            "backup_file": plan.get("backup_file"),
            "backup_file_absolute": plan.get("backup_file_absolute"),
            "apply_mode": plan.get("apply_mode"),
            "real_hosts_file_write": plan.get("real_hosts_file_write"),
            "rollback_result": rollback_result.get("rollback_result"),
            "status": rollback_result.get("status"),
            "rolled_back_from": "hosts_apply_service",
            "rolled_back_at": rollback_result.get("rolled_back_at"),
        }
