# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\apache_vhost_config_tool.py
# 📌 Amac: JHoster Apache virtual host planlarini ve guvenli config dosyalarini olusturur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Domain dogrulama, document root cozumleme ve snapshot altina Apache vhost config uretimi yapar
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import re

from config.constants import (
    APACHE_VHOST_DEFAULT_PORT,
    APACHE_VHOST_DEFAULT_SERVER_SUFFIX,
    APACHE_VHOST_DIRECTORY_NAME,
    APACHE_VHOST_EXTENSION,
    APACHE_VHOST_MESSAGE_DRY_RUN,
    APACHE_VHOST_MESSAGE_GENERATED,
    APACHE_VHOST_STATUS_GENERATED,
    APACHE_VHOST_STATUS_PLANNED,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class ApacheVhostConfigTool:
    DOMAIN_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,253}[a-z0-9]$")

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.snapshot_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / APACHE_VHOST_DIRECTORY_NAME
        ).resolve()

    def normalize_domain(self, domain: str, project_code: str) -> str:
        default_domain = f"{project_code}.{APACHE_VHOST_DEFAULT_SERVER_SUFFIX}"
        return str(domain or default_domain).strip().lower().replace(" ", "-")

    def is_valid_domain(self, domain: str) -> bool:
        normalized_domain = str(domain).strip().lower()
        blocked_tokens = ["/", "\\", ":", ".."]

        if any(token in normalized_domain for token in blocked_tokens):
            return False

        return bool(self.DOMAIN_PATTERN.match(normalized_domain))

    def build_virtual_host_plan(self, project: dict[str, Any], domain: str, port: int) -> dict[str, Any]:
        project_code = str(project.get("code", "")).strip().lower()
        normalized_domain = self.normalize_domain(domain, project_code)
        normalized_port = self._normalize_port(port)
        document_root_path = self._resolve_project_path(str(project.get("document_root", "")))
        config_path = (self.snapshot_root_path / f"{project_code}{APACHE_VHOST_EXTENSION}").resolve()

        return {
            "project_code": project_code,
            "domain": normalized_domain,
            "port": normalized_port,
            "document_root": self._to_relative(document_root_path),
            "document_root_absolute": self._to_apache_path(document_root_path),
            "config_file": self._to_relative(config_path),
            "config_file_absolute": str(config_path),
            "web_server": "apache",
            "config_syntax": "apache_vhost",
            "safe": self._is_inside_root(document_root_path) and self._is_inside_snapshot_root(config_path),
            "valid_domain": self.is_valid_domain(normalized_domain),
        }

    def generate_config_file(self, project: dict[str, Any], domain: str, port: int) -> dict[str, Any]:
        plan = self.build_virtual_host_plan(project, domain, port)

        if not plan.get("safe", False) or not plan.get("valid_domain", False):
            return {
                "success": False,
                "status": "blocked",
                "message": "apache virtual host plan is not safe",
                "plan": plan,
            }

        project_code = str(plan.get("project_code", "")).strip().lower()
        config_path = (self.snapshot_root_path / f"{project_code}{APACHE_VHOST_EXTENSION}").resolve()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_content = self._build_apache_config(plan)
        config_path.write_text(config_content, encoding="utf-8")

        return {
            "success": True,
            "status": APACHE_VHOST_STATUS_GENERATED,
            "message": APACHE_VHOST_MESSAGE_GENERATED,
            "plan": plan,
            "bytes": len(config_content.encode("utf-8")),
        }

    def build_dry_run_response(self, plan: dict[str, Any]) -> dict[str, Any]:
        return {
            "success": True,
            "status": APACHE_VHOST_STATUS_PLANNED,
            "message": APACHE_VHOST_MESSAGE_DRY_RUN,
            "apache_virtual_host_plan": plan,
        }

    def _normalize_port(self, port: int) -> int:
        try:
            parsed_port = int(port)
        except (TypeError, ValueError):
            return APACHE_VHOST_DEFAULT_PORT

        if parsed_port < 1 or parsed_port > 65535:
            return APACHE_VHOST_DEFAULT_PORT

        return parsed_port

    def _resolve_project_path(self, relative_path: str) -> Path:
        cleaned_path = str(relative_path).strip().replace("\\", "/")
        return (self.root_path / cleaned_path).resolve()

    def _is_inside_root(self, target_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(self.root_path)
            return True
        except ValueError:
            return False

    def _is_inside_snapshot_root(self, target_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(self.snapshot_root_path)
            return True
        except ValueError:
            return False

    def _to_relative(self, target_path: Path) -> str:
        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _to_apache_path(self, target_path: Path) -> str:
        return str(target_path.resolve()).replace("\\", "/")

    def _build_apache_config(self, plan: dict[str, Any]) -> str:
        project_code = str(plan.get("project_code", "site")).strip().lower()
        document_root = str(plan.get("document_root_absolute", "")).replace("\\", "/")

        return (
            "# JHoster generated Apache virtual host snapshot\n"
            "# This file is not applied to system Apache automatically.\n"
            f"<VirtualHost *:{plan.get('port')}>\n"
            f"    ServerName {plan.get('domain')}\n"
            f"    DocumentRoot \"{document_root}\"\n"
            "    DirectoryIndex index.php index.html index.htm\n"
            "\n"
            f"    <Directory \"{document_root}\">\n"
            "        Options Indexes FollowSymLinks\n"
            "        AllowOverride All\n"
            "        Require all granted\n"
            "    </Directory>\n"
            "\n"
            f"    ErrorLog \"logs/{project_code}-error.log\"\n"
            f"    CustomLog \"logs/{project_code}-access.log\" common\n"
            "</VirtualHost>\n"
        )
