# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\virtual_host_config_tool.py
# 📌 Amac: JHoster virtual host planlarini ve guvenli nginx config dosyalarini olusturur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Domain dogrulama, document root cozumleme ve snapshot altina nginx vhost config uretimi yapar
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import re

from config.constants import (
    NGINX_VHOST_DIRECTORY_NAME,
    NGINX_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOST_DEFAULT_PORT,
    VIRTUAL_HOST_DEFAULT_SERVER_SUFFIX,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class VirtualHostConfigTool:
    DOMAIN_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.-]{1,253}[a-z0-9]$")

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.snapshot_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_VHOST_DIRECTORY_NAME
        ).resolve()

    def normalize_domain(self, domain: str, project_code: str) -> str:
        default_domain = f"{project_code}.{VIRTUAL_HOST_DEFAULT_SERVER_SUFFIX}"
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
        config_path = (self.snapshot_root_path / f"{project_code}{NGINX_VHOST_EXTENSION}").resolve()

        return {
            "project_code": project_code,
            "domain": normalized_domain,
            "port": normalized_port,
            "document_root": self._to_relative(document_root_path),
            "document_root_absolute": str(document_root_path).replace("\\", "/"),
            "config_file": self._to_relative(config_path),
            "safe": self._is_inside_root(document_root_path) and self._is_inside_snapshot_root(config_path),
            "valid_domain": self.is_valid_domain(normalized_domain),
        }

    def generate_config_file(self, project: dict[str, Any], domain: str, port: int) -> dict[str, Any]:
        plan = self.build_virtual_host_plan(project, domain, port)
        if not plan.get("safe", False) or not plan.get("valid_domain", False):
            return {
                "success": False,
                "status": "blocked",
                "message": "virtual host plan is not safe",
                "plan": plan,
            }

        project_code = str(plan.get("project_code", "")).strip().lower()
        config_path = (self.snapshot_root_path / f"{project_code}{NGINX_VHOST_EXTENSION}").resolve()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_content = self._build_nginx_config(plan)
        config_path.write_text(config_content, encoding="utf-8")

        return {
            "success": True,
            "status": "generated",
            "message": "virtual host config generated",
            "plan": plan,
            "bytes": len(config_content.encode("utf-8")),
        }

    def _normalize_port(self, port: int) -> int:
        try:
            parsed_port = int(port)
        except (TypeError, ValueError):
            return VIRTUAL_HOST_DEFAULT_PORT

        if parsed_port < 1 or parsed_port > 65535:
            return VIRTUAL_HOST_DEFAULT_PORT

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

    def _build_nginx_config(self, plan: dict[str, Any]) -> str:
        return (
            "# JHoster generated virtual host snapshot\n"
            "# This file is not applied to system nginx automatically.\n"
            "server {\n"
            f"    listen {plan.get('port')};\n"
            f"    server_name {plan.get('domain')};\n"
            f"    root {plan.get('document_root_absolute')};\n"
            "    index index.php index.html index.htm;\n"
            "\n"
            "    location / {\n"
            "        try_files $uri $uri/ /index.php?$query_string;\n"
            "    }\n"
            "}\n"
        )
