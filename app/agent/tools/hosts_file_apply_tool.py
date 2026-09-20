# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\hosts_file_apply_tool.py
# 📌 Amac: JHoster hosts satirini snapshot veya gercek Windows hosts dosyasina guvenli uygular
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Admin kontrolu, backup, apply ve rollback islemlerini izole eden tool katmani
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
from typing import Any
import re
import shutil

from config.constants import (
    APPLY_DIRECTORY_NAME,
    BACKUP_DIRECTORY_NAME,
    HOSTS_APPLIED_DIRECTORY_NAME,
    HOSTS_APPLIED_FILE_NAME,
    HOSTS_APPLY_MESSAGE_APPLIED,
    HOSTS_APPLY_MESSAGE_DRY_RUN,
    HOSTS_APPLY_MESSAGE_REJECTED,
    HOSTS_APPLY_MESSAGE_ROLLBACK_DRY_RUN,
    HOSTS_APPLY_MESSAGE_ROLLED_BACK,
    HOSTS_APPLY_MODE_REAL_WINDOWS,
    HOSTS_APPLY_MODE_SNAPSHOT,
    HOSTS_APPLY_STATUS_APPLIED,
    HOSTS_APPLY_STATUS_PLANNED,
    HOSTS_APPLY_STATUS_REJECTED,
    HOSTS_APPLY_STATUS_ROLLBACK_PLANNED,
    HOSTS_APPLY_STATUS_ROLLED_BACK,
    HOSTS_DIRECTORY_NAME,
    HOSTS_PUBLISH_DEFAULT_IP,
    HOSTS_PUBLISH_LINE_MARKER_PREFIX,
    HOSTS_WINDOWS_SYSTEM_FILE,
    SNAPSHOT_DIRECTORY_NAME,
)
from tools.admin_privilege_tool import AdminPrivilegeTool


class HostsFileApplyTool:
    DOMAIN_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,253}[a-z0-9]$")

    def __init__(self, root_path: Path, admin_privilege_tool: AdminPrivilegeTool) -> None:
        self.root_path = root_path.resolve()
        self.admin_privilege_tool = admin_privilege_tool
        self.snapshot_apply_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / HOSTS_APPLIED_DIRECTORY_NAME
        ).resolve()
        self.backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / APPLY_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()
        self.real_windows_hosts_file_path = Path(HOSTS_WINDOWS_SYSTEM_FILE)

    def build_apply_plan(
        self,
        project_code: str,
        domain: str,
        ip_value: str | None,
        real_write: bool,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        normalized_domain = self._normalize_domain(domain)
        normalized_ip = self._normalize_ip(ip_value)
        line_marker = self._build_line_marker(normalized_project_code)
        host_line = self._build_host_line(normalized_project_code, normalized_domain, normalized_ip)
        privilege_state = self.admin_privilege_tool.get_privilege_state()

        target_file = self._resolve_target_file(real_write)
        target_is_safe = self._is_target_safe(target_file, real_write)
        valid_domain = self._is_valid_domain(normalized_domain)
        valid_ip = self._is_valid_ip(normalized_ip)
        admin_required = bool(real_write)
        admin_ok = bool(privilege_state.get("is_admin")) if real_write else True
        platform_ok = bool(privilege_state.get("is_windows")) if real_write else True

        return {
            "project_code": normalized_project_code,
            "domain": normalized_domain,
            "ip": normalized_ip,
            "target_file": self._to_relative_or_absolute(target_file),
            "target_file_absolute": str(target_file.resolve()),
            "target_exists": target_file.is_file(),
            "target_is_safe": target_is_safe,
            "valid_domain": valid_domain,
            "valid_ip": valid_ip,
            "line_marker": line_marker,
            "host_line": host_line,
            "apply_mode": HOSTS_APPLY_MODE_REAL_WINDOWS if real_write else HOSTS_APPLY_MODE_SNAPSHOT,
            "real_hosts_file_write": bool(real_write),
            "admin_required": admin_required,
            "admin_ok": admin_ok,
            "platform_ok": platform_ok,
            "privilege": privilege_state,
            "safe": target_is_safe and valid_domain and valid_ip and admin_ok and platform_ok,
            "planned_at": self._now(),
        }

    def apply_entry(
        self,
        project_code: str,
        domain: str,
        ip_value: str | None,
        real_write: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_apply_plan(
            project_code=project_code,
            domain=domain,
            ip_value=ip_value,
            real_write=real_write,
        )

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": HOSTS_APPLY_STATUS_REJECTED,
                "message": HOSTS_APPLY_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": HOSTS_APPLY_STATUS_PLANNED,
                "message": HOSTS_APPLY_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        target_file = Path(str(plan.get("target_file_absolute")))
        if not real_write:
            target_file.parent.mkdir(parents=True, exist_ok=True)

        backup_result = self._backup_existing_file(target_file, real_write)
        write_result = self._write_or_replace_host_line(
            target_file=target_file,
            line_marker=str(plan.get("line_marker")),
            host_line=str(plan.get("host_line")),
            real_write=real_write,
        )

        return {
            "success": True,
            "status": HOSTS_APPLY_STATUS_APPLIED,
            "message": HOSTS_APPLY_MESSAGE_APPLIED,
            "plan": plan,
            "backup": backup_result,
            "write_result": write_result,
            "applied_at": self._now(),
        }

    def build_rollback_plan(self, apply_record: dict[str, Any]) -> dict[str, Any]:
        backup_file = self._resolve_record_path(str(apply_record.get("backup", {}).get("backup_file", "")))
        target_file = self._resolve_record_path(str(apply_record.get("target_file", "")))
        real_write = bool(apply_record.get("real_hosts_file_write", False))
        privilege_state = self.admin_privilege_tool.get_privilege_state()
        target_is_safe = self._is_target_safe(target_file, real_write)
        backup_is_safe = self._is_backup_safe(backup_file)
        admin_ok = bool(privilege_state.get("is_admin")) if real_write else True
        platform_ok = bool(privilege_state.get("is_windows")) if real_write else True

        return {
            "project_code": apply_record.get("project_code"),
            "domain": apply_record.get("domain"),
            "target_file": self._to_relative_or_absolute(target_file),
            "target_file_absolute": str(target_file.resolve()),
            "backup_file": self._to_relative_or_absolute(backup_file),
            "backup_file_absolute": str(backup_file.resolve()),
            "target_exists": target_file.is_file(),
            "backup_exists": backup_file.is_file(),
            "target_is_safe": target_is_safe,
            "backup_is_safe": backup_is_safe,
            "apply_mode": apply_record.get("apply_mode"),
            "real_hosts_file_write": real_write,
            "admin_required": real_write,
            "admin_ok": admin_ok,
            "platform_ok": platform_ok,
            "privilege": privilege_state,
            "safe": target_is_safe and backup_is_safe and backup_file.is_file() and admin_ok and platform_ok,
            "planned_at": self._now(),
        }

    def rollback_entry(self, apply_record: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        plan = self.build_rollback_plan(apply_record)

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": HOSTS_APPLY_STATUS_REJECTED,
                "message": HOSTS_APPLY_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": HOSTS_APPLY_STATUS_ROLLBACK_PLANNED,
                "message": HOSTS_APPLY_MESSAGE_ROLLBACK_DRY_RUN,
                "plan": plan,
            }

        backup_file = Path(str(plan.get("backup_file_absolute")))
        target_file = Path(str(plan.get("target_file_absolute")))
        if not bool(plan.get("real_hosts_file_write")):
            target_file.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(backup_file, target_file)

        return {
            "success": True,
            "status": HOSTS_APPLY_STATUS_ROLLED_BACK,
            "message": HOSTS_APPLY_MESSAGE_ROLLED_BACK,
            "plan": plan,
            "rollback_result": {
                "restored": True,
                "source_backup": self._to_relative_or_absolute(backup_file),
                "target_file": self._to_relative_or_absolute(target_file),
                "real_hosts_file_write": bool(plan.get("real_hosts_file_write")),
            },
            "rolled_back_at": self._now(),
        }

    def _resolve_target_file(self, real_write: bool) -> Path:
        if real_write:
            return self.real_windows_hosts_file_path
        return (self.snapshot_apply_root_path / HOSTS_APPLIED_FILE_NAME).resolve()

    def _write_or_replace_host_line(
        self,
        target_file: Path,
        line_marker: str,
        host_line: str,
        real_write: bool,
    ) -> dict[str, Any]:
        existing_lines: list[str] = []
        removed_count = 0

        if target_file.is_file():
            existing_lines = target_file.read_text(encoding="utf-8", errors="ignore").splitlines()

        next_lines: list[str] = []
        for line in existing_lines:
            if line_marker in line:
                removed_count += 1
                continue
            next_lines.append(line)

        next_lines.append(host_line)
        target_file.write_text("\n".join(next_lines).strip() + "\n", encoding="utf-8")

        return {
            "target_file": self._to_relative_or_absolute(target_file),
            "removed_existing_lines": removed_count,
            "added_line": True,
            "real_hosts_file_write": real_write,
        }

    def _backup_existing_file(self, target_file: Path, real_write: bool) -> dict[str, Any]:
        if not target_file.is_file():
            return {
                "created": False,
                "reason": "target file does not exist",
            }

        self.backup_root_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = ".hosts" if real_write else target_file.suffix
        backup_file = self.backup_root_path / f"{target_file.stem}.{timestamp}{suffix}"
        shutil.copy2(target_file, backup_file)

        return {
            "created": True,
            "backup_file": self._to_relative_or_absolute(backup_file),
            "backup_file_absolute": str(backup_file.resolve()),
            "real_hosts_file_write": real_write,
        }

    def _resolve_record_path(self, path_value: str) -> Path:
        raw_value = str(path_value or "").strip()
        if not raw_value:
            return Path("")

        normalized_value = raw_value.replace("\\", "/")
        candidate = Path(normalized_value)
        if candidate.is_absolute():
            return candidate

        return (self.root_path / normalized_value).resolve()

    def _is_target_safe(self, target_file: Path, real_write: bool) -> bool:
        resolved_target = target_file.resolve()
        if real_write:
            return str(resolved_target).lower() == str(self.real_windows_hosts_file_path.resolve()).lower()
        return self._is_inside_path(resolved_target, self.snapshot_apply_root_path)

    def _is_backup_safe(self, backup_file: Path) -> bool:
        if not str(backup_file).strip():
            return False
        return self._is_inside_path(backup_file.resolve(), self.backup_root_path)

    def _normalize_domain(self, domain: str) -> str:
        return str(domain or "").strip().lower().replace(" ", "-")

    def _normalize_ip(self, ip_value: str | None) -> str:
        raw_ip = str(ip_value or "").strip()
        return raw_ip if raw_ip else HOSTS_PUBLISH_DEFAULT_IP

    def _is_valid_domain(self, domain: str) -> bool:
        blocked_tokens = ["/", "\\", ":", ".."]
        if any(token in domain for token in blocked_tokens):
            return False
        return bool(self.DOMAIN_PATTERN.match(domain))

    def _is_valid_ip(self, ip_value: str) -> bool:
        try:
            ip_address(ip_value)
            return True
        except ValueError:
            return False

    def _build_line_marker(self, project_code: str) -> str:
        return f"{HOSTS_PUBLISH_LINE_MARKER_PREFIX}{project_code}"

    def _build_host_line(self, project_code: str, domain: str, ip_value: str) -> str:
        return f"{ip_value} {domain} {self._build_line_marker(project_code)}"

    def _is_inside_path(self, target_path: Path, parent_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(parent_path.resolve())
            return True
        except ValueError:
            return False

    def _to_relative_or_absolute(self, target_path: Path) -> str:
        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
