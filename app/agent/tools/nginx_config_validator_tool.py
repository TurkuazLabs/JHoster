# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\nginx_config_validator_tool.py
# 📌 Amac: Publish edilmis Nginx virtual host config dosyasini guvenli sekilde dogrular
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Path guvenligi, dosya varligi ve temel nginx config icerik kontrolu yapar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config.constants import (
    NGINX_PUBLISHED_DIRECTORY_NAME,
    NGINX_VALIDATE_MESSAGE_DRY_RUN,
    NGINX_VALIDATE_MESSAGE_INVALID,
    NGINX_VALIDATE_MESSAGE_REJECTED,
    NGINX_VALIDATE_MESSAGE_VALID,
    NGINX_VALIDATE_REQUIRED_DIRECTIVES,
    NGINX_VALIDATE_STATUS_INVALID,
    NGINX_VALIDATE_STATUS_PLANNED,
    NGINX_VALIDATE_STATUS_REJECTED,
    NGINX_VALIDATE_STATUS_VALID,
    NGINX_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class NginxConfigValidatorTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_PUBLISHED_DIRECTORY_NAME
        ).resolve()

    def build_validation_plan(
        self,
        project_code: str,
        published_config_file: Path,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        target_path = published_config_file.resolve()

        target_exists = target_path.is_file()
        target_is_safe = self._is_inside_path(target_path, self.publish_root_path)
        target_extension_is_safe = target_path.suffix == NGINX_VHOST_EXTENSION

        return {
            "project_code": normalized_project_code,
            "target_file": self._to_relative(target_path),
            "target_file_absolute": str(target_path),
            "target_exists": target_exists,
            "target_is_safe": target_is_safe,
            "target_extension_is_safe": target_extension_is_safe,
            "safe": target_exists and target_is_safe and target_extension_is_safe,
            "validation_mode": "internal_static_scan",
            "nginx_command": "nginx -t is planned for later real adapter step",
            "planned_at": self._now(),
        }

    def validate_config(
        self,
        project_code: str,
        published_config_file: Path,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_validation_plan(project_code, published_config_file)

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": NGINX_VALIDATE_STATUS_REJECTED,
                "message": NGINX_VALIDATE_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": NGINX_VALIDATE_STATUS_PLANNED,
                "message": NGINX_VALIDATE_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        target_path = Path(str(plan.get("target_file_absolute"))).resolve()
        content = target_path.read_text(encoding="utf-8")
        checks = self._run_static_checks(content)
        is_valid = all(bool(check.get("passed")) for check in checks)

        return {
            "success": is_valid,
            "status": NGINX_VALIDATE_STATUS_VALID if is_valid else NGINX_VALIDATE_STATUS_INVALID,
            "message": NGINX_VALIDATE_MESSAGE_VALID if is_valid else NGINX_VALIDATE_MESSAGE_INVALID,
            "plan": plan,
            "checks": checks,
            "validated_at": self._now(),
        }

    def _run_static_checks(self, content: str) -> list[dict[str, Any]]:
        return [
            self._check_not_empty(content),
            self._check_required_directives(content),
            self._check_balanced_braces(content),
            self._check_no_blocked_tokens(content),
        ]

    def _check_not_empty(self, content: str) -> dict[str, Any]:
        return {
            "name": "not_empty",
            "passed": bool(content.strip()),
        }

    def _check_required_directives(self, content: str) -> dict[str, Any]:
        normalized_content = content.lower()
        missing_directives = [
            directive
            for directive in NGINX_VALIDATE_REQUIRED_DIRECTIVES
            if directive.lower() not in normalized_content
        ]

        return {
            "name": "required_directives",
            "passed": len(missing_directives) == 0,
            "missing": missing_directives,
        }

    def _check_balanced_braces(self, content: str) -> dict[str, Any]:
        open_count = content.count("{")
        close_count = content.count("}")

        return {
            "name": "balanced_braces",
            "passed": open_count == close_count and open_count > 0,
            "open": open_count,
            "close": close_count,
        }

    def _check_no_blocked_tokens(self, content: str) -> dict[str, Any]:
        blocked_tokens = ["..\\", "../", "$document_root"]
        found_tokens = [token for token in blocked_tokens if token in content]

        return {
            "name": "blocked_tokens",
            "passed": len(found_tokens) == 0,
            "found": found_tokens,
        }

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
