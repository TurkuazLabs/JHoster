# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\nginx_execution_preflight_tool.py
# 📌 Amac: Nginx real execution oncesi executable, main config ve include guvenligini kontrol eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Gercek komut calistirmadan nginx.exe, nginx.conf ve vhost include zincirini preflight eder
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os
import re

from config.constants import (
    NGINX_EXECUTABLE_FILE_NAME_WINDOWS,
    NGINX_EXECUTION_PREFLIGHT_BLOCKED_INCLUDE_TOKENS,
    NGINX_EXECUTION_PREFLIGHT_ENV_MAIN_CONFIG,
    NGINX_EXECUTION_PREFLIGHT_MAIN_CONFIG_FILE_NAME,
    NGINX_EXECUTION_PREFLIGHT_MESSAGE_BLOCKED,
    NGINX_EXECUTION_PREFLIGHT_MESSAGE_DRY_RUN,
    NGINX_EXECUTION_PREFLIGHT_MESSAGE_READY,
    NGINX_EXECUTION_PREFLIGHT_MODE,
    NGINX_EXECUTION_PREFLIGHT_REQUIRED_DIRECTIVES,
    NGINX_EXECUTION_PREFLIGHT_STATUS_BLOCKED,
    NGINX_EXECUTION_PREFLIGHT_STATUS_PLANNED,
    NGINX_EXECUTION_PREFLIGHT_STATUS_READY,
    NGINX_PUBLISHED_DIRECTORY_NAME,
    NGINX_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class NginxExecutionPreflightTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.default_main_config_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / "nginx" / "conf" / NGINX_EXECUTION_PREFLIGHT_MAIN_CONFIG_FILE_NAME
        ).resolve()

    def build_preflight_plan(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        target_path = published_config_file.resolve()
        executable_path = self._resolve_path(str(executable_record.get("path_absolute") or executable_record.get("path") or ""))
        main_config_path = self._resolve_main_config_path()

        target_checks = self._build_target_checks(target_path)
        executable_checks = self._build_executable_checks(executable_path, executable_record)
        main_config_checks = self._build_main_config_checks(main_config_path)
        include_checks = self._build_include_checks(main_config_path)

        blocking_reasons = []
        blocking_reasons.extend(target_checks["blocking_reasons"])
        blocking_reasons.extend(executable_checks["blocking_reasons"])
        blocking_reasons.extend(main_config_checks["blocking_reasons"])
        blocking_reasons.extend(include_checks["blocking_reasons"])

        path_safe = all(
            [
                target_checks["exists"],
                target_checks["is_safe"],
                target_checks["extension_is_safe"],
                executable_checks["exists"],
                executable_checks["name_is_safe"],
                executable_checks["path_is_safe"],
                main_config_checks["exists"],
                main_config_checks["name_is_safe"],
                main_config_checks["path_is_safe"],
            ]
        )
        real_execution_ready = path_safe and include_checks["ready"] and executable_checks["pe_header_valid"]

        return {
            "project_code": normalized_project_code,
            "published_config_file": self._to_relative(target_path),
            "published_config_file_absolute": str(target_path),
            "main_config_file": self._to_relative(main_config_path),
            "main_config_file_absolute": str(main_config_path),
            "nginx_executable_file": str(executable_path),
            "nginx_executable_file_absolute": str(executable_path),
            "preflight_mode": NGINX_EXECUTION_PREFLIGHT_MODE,
            "target_checks": target_checks,
            "executable_checks": executable_checks,
            "main_config_checks": main_config_checks,
            "include_checks": include_checks,
            "path_safe": path_safe,
            "real_execution_ready": real_execution_ready,
            "blocking_reasons": blocking_reasons,
            "shell_execution": False,
            "real_nginx_execution": False,
            "planned_at": self._now(),
        }

    def run_preflight(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_preflight_plan(
            project_code=project_code,
            published_config_file=published_config_file,
            executable_record=executable_record,
        )

        if dry_run:
            return {
                "success": True,
                "status": NGINX_EXECUTION_PREFLIGHT_STATUS_PLANNED,
                "message": NGINX_EXECUTION_PREFLIGHT_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        is_ready = bool(plan.get("real_execution_ready"))

        return {
            "success": True,
            "status": NGINX_EXECUTION_PREFLIGHT_STATUS_READY if is_ready else NGINX_EXECUTION_PREFLIGHT_STATUS_BLOCKED,
            "message": NGINX_EXECUTION_PREFLIGHT_MESSAGE_READY if is_ready else NGINX_EXECUTION_PREFLIGHT_MESSAGE_BLOCKED,
            "plan": plan,
            "preflight_result": {
                "real_execution_ready": is_ready,
                "shell_execution": False,
                "real_nginx_execution": False,
                "blocking_reasons": plan.get("blocking_reasons", []),
            },
            "preflighted_at": self._now(),
        }

    def _build_target_checks(self, target_path: Path) -> dict[str, Any]:
        exists = target_path.is_file()
        is_safe = self._is_inside_path(target_path, self.publish_root_path)
        extension_is_safe = target_path.suffix == NGINX_VHOST_EXTENSION
        blocking_reasons = []

        if not exists:
            blocking_reasons.append("published_config_missing")
        if not is_safe:
            blocking_reasons.append("published_config_path_not_safe")
        if not extension_is_safe:
            blocking_reasons.append("published_config_extension_not_safe")

        return {
            "exists": exists,
            "is_safe": is_safe,
            "extension_is_safe": extension_is_safe,
            "blocking_reasons": blocking_reasons,
        }

    def _build_executable_checks(self, executable_path: Path, executable_record: dict[str, Any]) -> dict[str, Any]:
        exists = executable_path.is_file()
        name_is_safe = executable_path.name.lower() == NGINX_EXECUTABLE_FILE_NAME_WINDOWS
        path_is_safe = name_is_safe and self._is_allowed_executable_path(executable_path, executable_record)
        pe_header_valid = self._has_windows_pe_header(executable_path) if exists else False
        blocking_reasons = []

        if not exists:
            blocking_reasons.append("nginx_executable_missing")
        if not name_is_safe:
            blocking_reasons.append("nginx_executable_name_not_safe")
        if not path_is_safe:
            blocking_reasons.append("nginx_executable_path_not_safe")
        if exists and not pe_header_valid:
            blocking_reasons.append("nginx_executable_pe_header_invalid")

        return {
            "exists": exists,
            "name_is_safe": name_is_safe,
            "path_is_safe": path_is_safe,
            "source": executable_record.get("source"),
            "pe_header_valid": pe_header_valid,
            "blocking_reasons": blocking_reasons,
        }

    def _build_main_config_checks(self, main_config_path: Path) -> dict[str, Any]:
        exists = main_config_path.is_file()
        name_is_safe = main_config_path.name.lower() == NGINX_EXECUTION_PREFLIGHT_MAIN_CONFIG_FILE_NAME
        path_is_safe = name_is_safe and self._is_inside_path(main_config_path, self.root_path)
        content = self._read_text(main_config_path) if exists else ""
        content_has_required_directives = all(item in content for item in NGINX_EXECUTION_PREFLIGHT_REQUIRED_DIRECTIVES)
        blocking_reasons = []

        if not exists:
            blocking_reasons.append("main_config_missing")
        if not name_is_safe:
            blocking_reasons.append("main_config_name_not_safe")
        if not path_is_safe:
            blocking_reasons.append("main_config_path_not_safe")
        if exists and not content_has_required_directives:
            blocking_reasons.append("main_config_required_directives_missing")

        return {
            "exists": exists,
            "name_is_safe": name_is_safe,
            "path_is_safe": path_is_safe,
            "required_directives_present": content_has_required_directives,
            "blocking_reasons": blocking_reasons,
        }

    def _build_include_checks(self, main_config_path: Path) -> dict[str, Any]:
        if not main_config_path.is_file():
            return {
                "includes": [],
                "has_published_include": False,
                "ready": False,
                "blocking_reasons": ["main_config_include_scan_unavailable"],
            }

        content = self._read_text(main_config_path)
        raw_includes = re.findall(r"include\s+([^;]+);", content, flags=re.IGNORECASE)
        include_items = [self._normalize_include_item(raw_include) for raw_include in raw_includes]
        has_published_include = any(item["matches_published_vhost_dir"] for item in include_items)
        has_blocked_include_token = any(item["has_blocked_token"] for item in include_items)
        ready = bool(include_items) and has_published_include and not has_blocked_include_token
        blocking_reasons = []

        if not include_items:
            blocking_reasons.append("main_config_include_missing")
        if include_items and not has_published_include:
            blocking_reasons.append("main_config_published_include_missing")
        if has_blocked_include_token:
            blocking_reasons.append("main_config_include_contains_blocked_token")

        return {
            "includes": include_items,
            "has_published_include": has_published_include,
            "has_blocked_include_token": has_blocked_include_token,
            "ready": ready,
            "blocking_reasons": blocking_reasons,
        }

    def _normalize_include_item(self, raw_include: str) -> dict[str, Any]:
        cleaned_value = raw_include.strip().strip('"').strip("'")
        normalized_value = cleaned_value.replace("\\", "/")
        normalized_publish_root = str(self.publish_root_path).replace("\\", "/")
        normalized_root = str(self.root_path).replace("\\", "/")
        relative_publish_path = str(self.publish_root_path.relative_to(self.root_path)).replace("\\", "/")
        has_blocked_token = any(token in normalized_value for token in NGINX_EXECUTION_PREFLIGHT_BLOCKED_INCLUDE_TOKENS)
        matches_published_vhost_dir = (
            normalized_publish_root in normalized_value
            or relative_publish_path in normalized_value
            or normalized_value.startswith(f"{normalized_root}/{relative_publish_path}")
        )

        return {
            "raw": raw_include.strip(),
            "normalized": normalized_value,
            "has_wildcard": "*" in normalized_value,
            "has_blocked_token": has_blocked_token,
            "matches_published_vhost_dir": matches_published_vhost_dir,
        }

    def _has_windows_pe_header(self, executable_path: Path) -> bool:
        try:
            with executable_path.open("rb") as executable_file:
                return executable_file.read(2) == b"MZ"
        except OSError:
            return False

    def _read_text(self, file_path: Path) -> str:
        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return ""

    def _resolve_main_config_path(self) -> Path:
        env_main_config = os.getenv(NGINX_EXECUTION_PREFLIGHT_ENV_MAIN_CONFIG, "").strip()
        raw_path = env_main_config if env_main_config else str(self.default_main_config_path)

        return self._resolve_path(raw_path)

    def _resolve_path(self, raw_path: str) -> Path:
        if not raw_path.strip():
            return (self.root_path / "__missing_path__").resolve()

        path_value = Path(raw_path)

        if path_value.is_absolute():
            return path_value.resolve()

        return (self.root_path / path_value).resolve()

    def _is_allowed_executable_path(self, executable_path: Path, executable_record: dict[str, Any]) -> bool:
        source = str(executable_record.get("source", "")).strip().lower()

        if source == "project_snapshot":
            return self._is_inside_path(executable_path, self.root_path)

        return executable_path.name.lower() == NGINX_EXECUTABLE_FILE_NAME_WINDOWS

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
