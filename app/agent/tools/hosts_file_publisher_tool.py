# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\hosts_file_publisher_tool.py
# 📌 Amac: JHoster proje domainlerini guvenli snapshot hosts dosyasina publish eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Hosts satiri planlama, path guvenligi, backup, replace ve snapshot publish islemlerini yapar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path
from typing import Any
import re
import shutil

from config.constants import (
    BACKUP_DIRECTORY_NAME,
    HOSTS_DIRECTORY_NAME,
    HOSTS_PUBLISHED_DIRECTORY_NAME,
    HOSTS_PUBLISHED_FILE_NAME,
    HOSTS_PUBLISH_DEFAULT_IP,
    HOSTS_PUBLISH_LINE_MARKER_PREFIX,
    HOSTS_PUBLISH_MESSAGE_DRY_RUN,
    HOSTS_PUBLISH_MESSAGE_PUBLISHED,
    HOSTS_PUBLISH_MESSAGE_REJECTED,
    HOSTS_PUBLISH_STATUS_PLANNED,
    HOSTS_PUBLISH_STATUS_PUBLISHED,
    HOSTS_PUBLISH_STATUS_REJECTED,
    PUBLISH_DIRECTORY_NAME,
    SNAPSHOT_DIRECTORY_NAME,
)


class HostsFilePublisherTool:
    DOMAIN_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,253}[a-z0-9]$")

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.hosts_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / HOSTS_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / PUBLISH_DIRECTORY_NAME / HOSTS_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()

    def build_publish_plan(
        self,
        project_code: str,
        domain: str,
        ip_value: str | None = None,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        normalized_domain = self._normalize_domain(domain)
        normalized_ip = self._normalize_ip(ip_value)
        target_file_path = (self.hosts_root_path / HOSTS_PUBLISHED_FILE_NAME).resolve()
        host_line = self._build_host_line(normalized_project_code, normalized_domain, normalized_ip)

        target_is_safe = self._is_inside_path(target_file_path, self.hosts_root_path)
        valid_domain = self._is_valid_domain(normalized_domain)
        valid_ip = self._is_valid_ip(normalized_ip)

        return {
            "project_code": normalized_project_code,
            "domain": normalized_domain,
            "ip": normalized_ip,
            "target_file": self._to_relative(target_file_path),
            "target_file_absolute": str(target_file_path),
            "target_is_safe": target_is_safe,
            "valid_domain": valid_domain,
            "valid_ip": valid_ip,
            "safe": target_is_safe and valid_domain and valid_ip,
            "line_marker": self._build_line_marker(normalized_project_code),
            "host_line": host_line,
            "real_hosts_file_write": False,
            "planned_at": self._now(),
        }

    def publish_entry(
        self,
        project_code: str,
        domain: str,
        ip_value: str | None,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_publish_plan(
            project_code=project_code,
            domain=domain,
            ip_value=ip_value,
        )

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": HOSTS_PUBLISH_STATUS_REJECTED,
                "message": HOSTS_PUBLISH_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": HOSTS_PUBLISH_STATUS_PLANNED,
                "message": HOSTS_PUBLISH_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        target_file = Path(str(plan.get("target_file_absolute")))
        target_file.parent.mkdir(parents=True, exist_ok=True)
        backup_result = self._backup_existing_file(target_file)
        replaced = self._write_or_replace_host_line(target_file, str(plan.get("line_marker")), str(plan.get("host_line")))

        return {
            "success": True,
            "status": HOSTS_PUBLISH_STATUS_PUBLISHED,
            "message": HOSTS_PUBLISH_MESSAGE_PUBLISHED,
            "plan": plan,
            "backup": backup_result,
            "write_result": replaced,
            "published_at": self._now(),
        }

    def _write_or_replace_host_line(self, target_file: Path, line_marker: str, host_line: str) -> dict[str, Any]:
        existing_lines: list[str] = []
        removed_count = 0

        if target_file.is_file():
            existing_lines = target_file.read_text(encoding="utf-8").splitlines()

        next_lines: list[str] = []
        for line in existing_lines:
            if line_marker in line:
                removed_count += 1
                continue
            next_lines.append(line)

        next_lines.append(host_line)
        target_file.write_text("\n".join(next_lines).strip() + "\n", encoding="utf-8")

        return {
            "target_file": self._to_relative(target_file),
            "removed_existing_lines": removed_count,
            "added_line": True,
            "real_hosts_file_write": False,
        }

    def _backup_existing_file(self, target_file: Path) -> dict[str, Any]:
        if not target_file.is_file():
            return {
                "created": False,
                "reason": "target file does not exist",
            }

        self.backup_root_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        backup_file = self.backup_root_path / f"{target_file.stem}.{timestamp}{target_file.suffix}"
        shutil.copy2(target_file, backup_file)

        return {
            "created": True,
            "backup_file": self._to_relative(backup_file),
            "backup_file_absolute": str(backup_file.resolve()),
        }

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

    def _to_relative(self, target_path: Path) -> str:
        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
