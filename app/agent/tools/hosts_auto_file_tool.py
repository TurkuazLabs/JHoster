# 📄 Dosya Yolu: E:/JHoster/app/agent/tools/hosts_auto_file_tool.py
# 📌 Amac: JHoster domainlerini Windows hosts dosyasinda imzali blok olarak guvenli sekilde senkronlar ve denetler
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Hosts blok planlama, inspect count ozeti, repair, backup, snapshot sync ve gercek Windows hosts yazma islemlerini izole eder
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
    HOSTS_AUTO_BLOCK_BEGIN,
    HOSTS_AUTO_BLOCK_END,
    HOSTS_AUTO_COMMENT_PREFIX,
    HOSTS_AUTO_DEFAULT_IP,
    HOSTS_AUTO_MESSAGE_DRY_RUN,
    HOSTS_AUTO_MESSAGE_INSPECTED,
    HOSTS_AUTO_MESSAGE_REJECTED,
    HOSTS_AUTO_MESSAGE_REPAIR_NOT_REQUIRED,
    HOSTS_AUTO_MESSAGE_SYNCED,
    HOSTS_AUTO_MODE_REAL_WINDOWS,
    HOSTS_AUTO_MODE_SNAPSHOT,
    HOSTS_AUTO_SNAPSHOT_DIRECTORY_NAME,
    HOSTS_AUTO_SNAPSHOT_FILE_NAME,
    HOSTS_AUTO_STATUS_INSPECTED,
    HOSTS_AUTO_STATUS_PLANNED,
    HOSTS_AUTO_STATUS_REJECTED,
    HOSTS_AUTO_STATUS_REPAIR_NOT_REQUIRED,
    HOSTS_AUTO_STATUS_SYNCED,
    HOSTS_DIRECTORY_NAME,
    HOSTS_WINDOWS_SYSTEM_FILE,
    SNAPSHOT_DIRECTORY_NAME,
)
from tools.admin_privilege_tool import AdminPrivilegeTool


class HostsAutoFileTool:
    DOMAIN_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,253}[a-z0-9]$")
    HOST_LINE_PATTERN = re.compile(r"^\s*(?P<ip>\S+)\s+(?P<domain>[^\s#]+)(?P<comment>.*)$")

    def __init__(self, root_path: Path, admin_privilege_tool: AdminPrivilegeTool) -> None:
        self.root_path = root_path.resolve()
        self.admin_privilege_tool = admin_privilege_tool
        self.snapshot_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / HOSTS_AUTO_SNAPSHOT_DIRECTORY_NAME
        ).resolve()
        self.backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / APPLY_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()
        self.real_windows_hosts_file_path = Path(HOSTS_WINDOWS_SYSTEM_FILE)

    def build_sync_plan(
        self,
        entries: list[dict[str, Any]],
        ip_value: str | None,
        real_write: bool,
    ) -> dict[str, Any]:
        normalized_ip = self._normalize_ip(ip_value)
        normalized_entries = self._normalize_entries(entries, normalized_ip)
        invalid_entries = [entry for entry in normalized_entries if not entry.get("valid", False)]
        target_file = self._resolve_target_file(real_write)
        privilege_state = self.admin_privilege_tool.get_privilege_state()
        admin_ok = bool(privilege_state.get("is_admin")) if real_write else True
        platform_ok = bool(privilege_state.get("is_windows")) if real_write else True
        target_is_safe = self._is_target_safe(target_file, real_write)
        valid_ip = self._is_valid_ip(normalized_ip)

        return {
            "entries": normalized_entries,
            "entry_count": len(normalized_entries),
            "invalid_entries": invalid_entries,
            "invalid_count": len(invalid_entries),
            "ip": normalized_ip,
            "valid_ip": valid_ip,
            "target_file": self._to_relative_or_absolute(target_file),
            "target_file_absolute": str(target_file.resolve()),
            "target_exists": target_file.is_file(),
            "target_is_safe": target_is_safe,
            "block_begin": HOSTS_AUTO_BLOCK_BEGIN,
            "block_end": HOSTS_AUTO_BLOCK_END,
            "apply_mode": HOSTS_AUTO_MODE_REAL_WINDOWS if real_write else HOSTS_AUTO_MODE_SNAPSHOT,
            "real_hosts_file_write": bool(real_write),
            "admin_required": bool(real_write),
            "admin_ok": admin_ok,
            "platform_ok": platform_ok,
            "privilege": privilege_state,
            "safe": target_is_safe and valid_ip and not invalid_entries and admin_ok and platform_ok,
            "planned_at": self._now(),
        }

    def inspect_entries(
        self,
        entries: list[dict[str, Any]],
        ip_value: str | None,
        real_write: bool,
    ) -> dict[str, Any]:
        plan = self.build_sync_plan(entries=entries, ip_value=ip_value, real_write=real_write)
        if not plan.get("safe", False):
            return {
                "success": False,
                "status": HOSTS_AUTO_STATUS_REJECTED,
                "message": HOSTS_AUTO_MESSAGE_REJECTED,
                "plan": plan,
            }

        target_file = Path(str(plan.get("target_file_absolute")))
        existing_text = ""
        if target_file.is_file():
            existing_text = target_file.read_text(encoding="utf-8", errors="ignore")

        expected_entries = plan.get("entries", [])
        managed_entries = self._extract_managed_entries(existing_text)
        external_conflicts = self._find_external_conflicts(existing_text, expected_entries)
        expected_domains = {str(entry.get("domain", "")) for entry in expected_entries}
        managed_domains = {str(entry.get("domain", "")) for entry in managed_entries}

        missing_domains = sorted(expected_domains - managed_domains)
        stale_domains = sorted(managed_domains - expected_domains)
        wrong_ip_domains = self._find_wrong_ip_domains(expected_entries, managed_entries)
        duplicate_domains = self._find_duplicate_domains(managed_entries)
        repair_required = bool(missing_domains or stale_domains or wrong_ip_domains or duplicate_domains)

        inspect_result = {
            "target_file": plan.get("target_file"),
            "target_file_absolute": plan.get("target_file_absolute"),
            "target_exists": target_file.is_file(),
            "expected_count": len(expected_entries),
            "managed_count": len(managed_entries),
            "expected_domains": sorted(expected_domains),
            "managed_domains": sorted(managed_domains),
            "missing_domains": missing_domains,
            "missing_count": len(missing_domains),
            "stale_domains": stale_domains,
            "stale_count": len(stale_domains),
            "wrong_ip_domains": wrong_ip_domains,
            "wrong_ip_count": len(wrong_ip_domains),
            "duplicate_domains": duplicate_domains,
            "duplicate_count": len(duplicate_domains),
            "external_conflicts": external_conflicts,
            "external_conflict_count": len(external_conflicts),
            "repair_required": repair_required,
            "safe_to_repair": bool(plan.get("safe", False)),
            "inspected_at": self._now(),
        }

        return {
            "success": True,
            "status": HOSTS_AUTO_STATUS_INSPECTED,
            "message": HOSTS_AUTO_MESSAGE_INSPECTED,
            "plan": plan,
            "inspect": inspect_result,
        }

    def repair_entries(
        self,
        entries: list[dict[str, Any]],
        ip_value: str | None,
        real_write: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        inspect_result = self.inspect_entries(entries=entries, ip_value=ip_value, real_write=real_write)
        if not inspect_result.get("success", False):
            return inspect_result

        inspect_payload = inspect_result.get("inspect", {})
        if not isinstance(inspect_payload, dict):
            inspect_payload = {}

        if not inspect_payload.get("repair_required", False):
            return {
                "success": True,
                "status": HOSTS_AUTO_STATUS_REPAIR_NOT_REQUIRED,
                "message": HOSTS_AUTO_MESSAGE_REPAIR_NOT_REQUIRED,
                "plan": inspect_result.get("plan"),
                "inspect": inspect_payload,
            }

        sync_result = self.sync_entries(entries=entries, ip_value=ip_value, real_write=real_write, dry_run=dry_run)
        sync_result["inspect_before_repair"] = inspect_payload
        return sync_result

    def sync_entries(
        self,
        entries: list[dict[str, Any]],
        ip_value: str | None,
        real_write: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_sync_plan(entries=entries, ip_value=ip_value, real_write=real_write)

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": HOSTS_AUTO_STATUS_REJECTED,
                "message": HOSTS_AUTO_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": HOSTS_AUTO_STATUS_PLANNED,
                "message": HOSTS_AUTO_MESSAGE_DRY_RUN,
                "plan": plan,
                "preview": self._render_block(plan.get("entries", [])),
            }

        target_file = Path(str(plan.get("target_file_absolute")))
        if not real_write:
            target_file.parent.mkdir(parents=True, exist_ok=True)

        backup_result = self._backup_existing_file(target_file, real_write)
        write_result = self._write_managed_block(target_file, plan.get("entries", []), real_write)

        return {
            "success": True,
            "status": HOSTS_AUTO_STATUS_SYNCED,
            "message": HOSTS_AUTO_MESSAGE_SYNCED,
            "plan": plan,
            "backup": backup_result,
            "write_result": write_result,
            "synced_at": self._now(),
        }

    def _normalize_entries(self, entries: list[dict[str, Any]], ip_value: str) -> list[dict[str, Any]]:
        normalized_items: list[dict[str, Any]] = []
        seen_domains: set[str] = set()

        for item in entries:
            project_code = str(item.get("project_code", item.get("code", ""))).strip().lower()
            domain = self._normalize_domain(str(item.get("domain", "")))
            if not domain and project_code:
                domain = f"{project_code}.test"

            if not domain or domain in seen_domains:
                continue

            seen_domains.add(domain)
            normalized_items.append(
                {
                    "project_code": project_code,
                    "project_name": str(item.get("project_name", item.get("name", project_code))).strip(),
                    "domain": domain,
                    "ip": ip_value,
                    "valid": self._is_valid_domain(domain),
                    "line": self._build_host_line(project_code, domain, ip_value),
                }
            )

        return sorted(normalized_items, key=lambda entry: str(entry.get("domain", "")))

    def _write_managed_block(self, target_file: Path, entries: list[dict[str, Any]], real_write: bool) -> dict[str, Any]:
        existing_text = ""
        if target_file.is_file():
            existing_text = target_file.read_text(encoding="utf-8", errors="ignore")

        next_text, removed_old_block = self._replace_managed_block(existing_text, entries)
        target_file.write_text(next_text, encoding="utf-8")

        return {
            "target_file": self._to_relative_or_absolute(target_file),
            "entry_count": len(entries),
            "removed_old_block": removed_old_block,
            "real_hosts_file_write": real_write,
        }

    def _replace_managed_block(self, existing_text: str, entries: list[dict[str, Any]]) -> tuple[str, bool]:
        normalized_existing = existing_text.replace("\r\n", "\n").replace("\r", "\n")
        block_text = self._render_block(entries)
        begin_index = normalized_existing.find(HOSTS_AUTO_BLOCK_BEGIN)
        end_index = normalized_existing.find(HOSTS_AUTO_BLOCK_END)

        if begin_index >= 0 and end_index >= begin_index:
            end_index = end_index + len(HOSTS_AUTO_BLOCK_END)
            before_text = normalized_existing[:begin_index].rstrip()
            after_text = normalized_existing[end_index:].strip()
            parts = [part for part in [before_text, block_text, after_text] if part]
            return "\n\n".join(parts).strip() + "\n", True

        if not normalized_existing.strip():
            return block_text + "\n", False

        return normalized_existing.rstrip() + "\n\n" + block_text + "\n", False

    def _render_block(self, entries: list[dict[str, Any]]) -> str:
        lines = [HOSTS_AUTO_BLOCK_BEGIN]
        for entry in entries:
            lines.append(str(entry.get("line", "")).strip())
        lines.append(HOSTS_AUTO_BLOCK_END)
        return "\n".join(lines)

    def _extract_managed_entries(self, hosts_text: str) -> list[dict[str, Any]]:
        block_text = self._extract_managed_block(hosts_text)
        if not block_text:
            return []

        parsed_entries: list[dict[str, Any]] = []
        for line_number, line_text in enumerate(block_text.splitlines(), start=1):
            stripped_line = line_text.strip()
            if not stripped_line or stripped_line.startswith("#"):
                continue
            parsed_item = self._parse_host_line(stripped_line, line_number)
            if parsed_item is not None:
                parsed_entries.append(parsed_item)
        return parsed_entries

    def _extract_managed_block(self, hosts_text: str) -> str:
        normalized_text = hosts_text.replace("\r\n", "\n").replace("\r", "\n")
        begin_index = normalized_text.find(HOSTS_AUTO_BLOCK_BEGIN)
        end_index = normalized_text.find(HOSTS_AUTO_BLOCK_END)
        if begin_index < 0 or end_index < begin_index:
            return ""
        begin_index = begin_index + len(HOSTS_AUTO_BLOCK_BEGIN)
        return normalized_text[begin_index:end_index].strip()

    def _find_external_conflicts(
        self,
        hosts_text: str,
        expected_entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        normalized_text = hosts_text.replace("\r\n", "\n").replace("\r", "\n")
        expected_domain_map = {str(entry.get("domain", "")): str(entry.get("ip", "")) for entry in expected_entries}
        conflicts: list[dict[str, Any]] = []
        inside_managed_block = False

        for line_number, line_text in enumerate(normalized_text.splitlines(), start=1):
            stripped_line = line_text.strip()
            if stripped_line == HOSTS_AUTO_BLOCK_BEGIN:
                inside_managed_block = True
                continue
            if stripped_line == HOSTS_AUTO_BLOCK_END:
                inside_managed_block = False
                continue
            if inside_managed_block or not stripped_line or stripped_line.startswith("#"):
                continue

            parsed_item = self._parse_host_line(stripped_line, line_number)
            if parsed_item is None:
                continue

            domain = str(parsed_item.get("domain", ""))
            expected_ip = expected_domain_map.get(domain)
            if expected_ip is None:
                continue
            conflicts.append({
                **parsed_item,
                "expected_ip": expected_ip,
                "same_ip": str(parsed_item.get("ip", "")) == expected_ip,
            })

        return conflicts

    def _parse_host_line(self, line_text: str, line_number: int) -> dict[str, Any] | None:
        match = self.HOST_LINE_PATTERN.match(line_text)
        if match is None:
            return None

        return {
            "ip": match.group("ip").strip(),
            "domain": self._normalize_domain(match.group("domain")),
            "comment": match.group("comment").strip(),
            "line": line_text,
            "line_number": line_number,
        }

    def _find_wrong_ip_domains(
        self,
        expected_entries: list[dict[str, Any]],
        managed_entries: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        managed_ip_map = {str(entry.get("domain", "")): str(entry.get("ip", "")) for entry in managed_entries}
        wrong_items: list[dict[str, Any]] = []

        for expected_entry in expected_entries:
            domain = str(expected_entry.get("domain", ""))
            expected_ip = str(expected_entry.get("ip", ""))
            managed_ip = managed_ip_map.get(domain)
            if managed_ip is not None and managed_ip != expected_ip:
                wrong_items.append({
                    "domain": domain,
                    "expected_ip": expected_ip,
                    "current_ip": managed_ip,
                })

        return wrong_items

    def _find_duplicate_domains(self, managed_entries: list[dict[str, Any]]) -> list[str]:
        seen_domains: set[str] = set()
        duplicate_domains: set[str] = set()

        for entry in managed_entries:
            domain = str(entry.get("domain", ""))
            if domain in seen_domains:
                duplicate_domains.add(domain)
            seen_domains.add(domain)

        return sorted(duplicate_domains)

    def _backup_existing_file(self, target_file: Path, real_write: bool) -> dict[str, Any]:
        if not target_file.is_file():
            return {
                "created": False,
                "reason": "target file does not exist",
            }

        self.backup_root_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        suffix = ".hosts" if real_write else target_file.suffix
        backup_file = self.backup_root_path / f"{target_file.stem}.auto.{timestamp}{suffix}"
        shutil.copy2(target_file, backup_file)

        return {
            "created": True,
            "backup_file": self._to_relative_or_absolute(backup_file),
            "backup_file_absolute": str(backup_file.resolve()),
            "real_hosts_file_write": real_write,
        }

    def _resolve_target_file(self, real_write: bool) -> Path:
        if real_write:
            return self.real_windows_hosts_file_path
        return (self.snapshot_root_path / HOSTS_AUTO_SNAPSHOT_FILE_NAME).resolve()

    def _is_target_safe(self, target_file: Path, real_write: bool) -> bool:
        resolved_target = target_file.resolve()
        if real_write:
            return str(resolved_target).lower() == str(self.real_windows_hosts_file_path.resolve()).lower()
        return self._is_inside_path(resolved_target, self.snapshot_root_path)

    def _normalize_domain(self, domain: str) -> str:
        return str(domain or "").strip().lower().replace(" ", "-")

    def _normalize_ip(self, ip_value: str | None) -> str:
        raw_ip = str(ip_value or "").strip()
        return raw_ip if raw_ip else HOSTS_AUTO_DEFAULT_IP

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

    def _build_host_line(self, project_code: str, domain: str, ip_value: str) -> str:
        marker = f"{HOSTS_AUTO_COMMENT_PREFIX}{project_code}" if project_code else HOSTS_AUTO_COMMENT_PREFIX.rstrip(":")
        return f"{ip_value:<14} {domain:<24} {marker}"

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
