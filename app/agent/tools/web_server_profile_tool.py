# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\web_server_profile_tool.py
# 📌 Amac: JHoster web server profillerini ve adapter yeteneklerini tanimlar
# 📌 Modul - FileType
# Version: 1.3.0
# Aciklama: Apache ve Nginx seceneklerini ortak www document root ile tek katalog uzerinden sunan guncel tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import (
    APACHE_EXECUTABLE_FILE_NAME_WINDOWS,
    APACHE_EXECUTABLE_STANDARD_WINDOWS_PATHS,
    APACHE_MAIN_CONFIG_FILE_NAME,
    APACHE_RELOAD_COMMAND_LABEL,
    APACHE_VALIDATE_COMMAND_LABEL,
    APACHE_VHOST_EXTENSION,
    NGINX_EXECUTABLE_FILE_NAME_WINDOWS,
    NGINX_EXECUTABLE_STANDARD_WINDOWS_PATHS,
    NGINX_EXECUTABLE_VALIDATE_COMMAND_LABEL,
    NGINX_REAL_RELOAD_COMMAND_LABEL,
    NGINX_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME,
    NGINX_VHOST_EXTENSION,
    WEB_SERVER_CODE_APACHE,
    WEB_SERVER_CODE_NGINX,
    WEB_SERVER_PROFILE_APACHE_STAGE,
    WEB_SERVER_PROFILE_DEFAULT,
    WEB_SERVER_PROFILE_NGINX_STAGE,
    WEB_SERVER_PROFILE_STATUS_READY,
    WEB_SERVER_PROFILE_SUPPORTED_CODES,
    WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
)


class WebServerProfileTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path

    def list_profiles(self) -> list[dict[str, Any]]:
        return [self._build_nginx_profile(), self._build_apache_profile()]

    def get_profile(self, server_code: str) -> dict[str, Any] | None:
        normalized_code = self.normalize_server_code(server_code)

        for profile in self.list_profiles():
            if profile.get("code") == normalized_code:
                return profile

        return None

    def normalize_server_code(self, server_code: str) -> str:
        normalized_code = str(server_code or WEB_SERVER_PROFILE_DEFAULT).strip().lower()

        if not normalized_code:
            return WEB_SERVER_PROFILE_DEFAULT

        return normalized_code

    def is_supported(self, server_code: str) -> bool:
        return self.normalize_server_code(server_code) in WEB_SERVER_PROFILE_SUPPORTED_CODES

    def build_selection_plan(self, server_code: str) -> dict[str, Any]:
        normalized_code = self.normalize_server_code(server_code)
        selected_profile = self.get_profile(normalized_code)

        return {
            "server_code": normalized_code,
            "profile_found": selected_profile is not None,
            "supported": self.is_supported(normalized_code),
            "default_server_code": WEB_SERVER_PROFILE_DEFAULT,
            "profile": selected_profile,
            "ready": selected_profile is not None and selected_profile.get("status") == WEB_SERVER_PROFILE_STATUS_READY,
            "safe": (
                selected_profile is not None
                and self.is_supported(normalized_code)
                and selected_profile.get("status") == WEB_SERVER_PROFILE_STATUS_READY
            ),
        }

    def _build_nginx_profile(self) -> dict[str, Any]:
        return {
            "code": WEB_SERVER_CODE_NGINX,
            "name": "Nginx",
            "status": WEB_SERVER_PROFILE_STATUS_READY,
            "adapter_stage": WEB_SERVER_PROFILE_NGINX_STAGE,
            "default": False,
            "shared_document_root": WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "vhost_extension": NGINX_VHOST_EXTENSION,
            "main_config_file": NGINX_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME,
            "executable_file": NGINX_EXECUTABLE_FILE_NAME_WINDOWS,
            "standard_windows_paths": NGINX_EXECUTABLE_STANDARD_WINDOWS_PATHS,
            "validate_command_label": NGINX_EXECUTABLE_VALIDATE_COMMAND_LABEL,
            "reload_command_label": NGINX_REAL_RELOAD_COMMAND_LABEL,
            "implemented_routes": [
                "/api/v1/nginx-publish",
                "/api/v1/nginx-validate",
                "/api/v1/nginx-reload",
                "/api/v1/nginx-executable",
                "/api/v1/nginx-real-validate",
                "/api/v1/nginx-real-reload",
                "/api/v1/nginx-execution-preflight",
                "/api/v1/web-server-workflow",
            ],
            "notes": "Nginx adapter zinciri snapshot, publish, validate, reload ve real execution guard seviyesine geldi.",
        }

    def _build_apache_profile(self) -> dict[str, Any]:
        return {
            "code": WEB_SERVER_CODE_APACHE,
            "name": "Apache HTTP Server",
            "status": WEB_SERVER_PROFILE_STATUS_READY,
            "adapter_stage": WEB_SERVER_PROFILE_APACHE_STAGE,
            "default": True,
            "shared_document_root": WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "vhost_extension": APACHE_VHOST_EXTENSION,
            "main_config_file": APACHE_MAIN_CONFIG_FILE_NAME,
            "executable_file": APACHE_EXECUTABLE_FILE_NAME_WINDOWS,
            "standard_windows_paths": APACHE_EXECUTABLE_STANDARD_WINDOWS_PATHS,
            "validate_command_label": APACHE_VALIDATE_COMMAND_LABEL,
            "reload_command_label": APACHE_RELOAD_COMMAND_LABEL,
            "implemented_routes": [
                "/api/v1/apache-vhosts",
                "/api/v1/apache-publish",
                "/api/v1/apache-validate",
                "/api/v1/apache-executable",
                "/api/v1/apache-real-validate",
                "/api/v1/apache-real-reload",
                "/api/v1/web-server-workflow",
            ],
            "planned_routes": [],
            "notes": "Apache adapter zinciri snapshot, publish, validate, executable detect, real validate, real reload ve workflow seviyesine geldi.",
        }
