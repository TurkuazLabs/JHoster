# 📄 Dosya Yolu: E:\JHoster\app\agent\config\settings.py
# 📌 Amac: JHoster agent YAML ayarlarini Python nesnesine cevirir
# 📌 Modul - FileType
# Version: 1.5.0
# Aciklama: Sade root layout icin merkezi config okuyucu, data/jhoster storage ve guvenli path cozumleyici
# Bagimli Oldugu Katman: Config

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import os
import re

import yaml

from config.constants import CACHE_DIRECTORY_NAME, CONFIG_FILE_NAME, MODULES_DIRECTORY_NAME, DATA_DIRECTORY_NAME, JHOSTER_DATA_DIRECTORY_NAME, APP_DIRECTORY_NAME


CONFIG_FILE_PATH = Path(__file__).resolve().parent / CONFIG_FILE_NAME
# app/agent/config/settings.py -> JHoster root
PROJECT_ROOT_PATH = Path(__file__).resolve().parents[3]
WINDOWS_ABSOLUTE_PATH_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_version: str
    server_host: str
    server_port: int
    dev_reload: bool
    root_path: Path
    storage_path: Path
    modules_path: Path
    cache_path: Path
    local_only: bool
    default_dry_run: bool
    allow_shell_commands: bool
    allow_external_downloads: bool
    allow_safe_extract: bool

    @classmethod
    def load(cls) -> "AppSettings":
        config_data = cls._read_yaml(CONFIG_FILE_PATH)

        app_config = config_data.get("app", {})
        server_config = config_data.get("server", {})
        path_config = config_data.get("paths", {})
        security_config = config_data.get("security", {})
        executor_config = config_data.get("executor", {})

        root_path = cls._resolve_configured_path(
            path_config.get("root"),
            PROJECT_ROOT_PATH,
        )
        storage_path = cls._resolve_configured_path(
            path_config.get("storage"),
            PROJECT_ROOT_PATH / DATA_DIRECTORY_NAME / JHOSTER_DATA_DIRECTORY_NAME,
        )
        modules_path = cls._resolve_configured_path(
            path_config.get("modules"),
            root_path / APP_DIRECTORY_NAME / MODULES_DIRECTORY_NAME,
        )
        cache_path = cls._resolve_configured_path(
            path_config.get("cache"),
            root_path / CACHE_DIRECTORY_NAME,
        )

        return cls(
            app_name=str(app_config.get("name")),
            app_version=str(app_config.get("version")),
            server_host=str(server_config.get("host")),
            server_port=int(server_config.get("port")),
            dev_reload=bool(server_config.get("reload")),
            root_path=root_path,
            storage_path=storage_path,
            modules_path=modules_path,
            cache_path=cache_path,
            local_only=bool(security_config.get("local_only")),
            default_dry_run=bool(executor_config.get("default_dry_run", True)),
            allow_shell_commands=bool(executor_config.get("allow_shell_commands", False)),
            allow_external_downloads=bool(executor_config.get("allow_external_downloads", False)),
            allow_safe_extract=bool(executor_config.get("allow_safe_extract", True)),
        )

    @staticmethod
    def _read_yaml(file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as config_file:
            loaded_data = yaml.safe_load(config_file) or {}

        return loaded_data

    @staticmethod
    def _resolve_configured_path(path_value: Any, fallback_path: Path) -> Path:
        raw_path_value = str(path_value or "").strip()

        if not raw_path_value:
            return fallback_path

        if WINDOWS_ABSOLUTE_PATH_PATTERN.match(raw_path_value) and os.name != "nt":
            return fallback_path

        configured_path = Path(raw_path_value)

        if configured_path.is_absolute():
            return configured_path

        return (PROJECT_ROOT_PATH / configured_path).resolve()
