# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\nginx_reload_tool.py
# 📌 Amac: JHoster Nginx reload islemini guvenli simule eder ve reload plani uretir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Path guvenligi, validate kaydi ve simulated reload sonucunu yonetir
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config.constants import (
    NGINX_PUBLISHED_DIRECTORY_NAME,
    NGINX_RELOAD_COMMAND_LABEL,
    NGINX_RELOAD_MESSAGE_DRY_RUN,
    NGINX_RELOAD_MESSAGE_REJECTED,
    NGINX_RELOAD_MESSAGE_RELOADED,
    NGINX_RELOAD_MODE_SIMULATED,
    NGINX_RELOAD_STATUS_PLANNED,
    NGINX_RELOAD_STATUS_REJECTED,
    NGINX_RELOAD_STATUS_RELOADED,
    NGINX_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class NginxReloadTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_PUBLISHED_DIRECTORY_NAME
        ).resolve()

    def build_reload_plan(
        self,
        project_code: str,
        validated_config_file: Path,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        target_path = validated_config_file.resolve()

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
            "reload_mode": NGINX_RELOAD_MODE_SIMULATED,
            "command_label": NGINX_RELOAD_COMMAND_LABEL,
            "shell_execution": False,
            "planned_at": self._now(),
        }

    def reload_config(
        self,
        project_code: str,
        validated_config_file: Path,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_reload_plan(
            project_code=project_code,
            validated_config_file=validated_config_file,
        )

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": NGINX_RELOAD_STATUS_REJECTED,
                "message": NGINX_RELOAD_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": NGINX_RELOAD_STATUS_PLANNED,
                "message": NGINX_RELOAD_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        return {
            "success": True,
            "status": NGINX_RELOAD_STATUS_RELOADED,
            "message": NGINX_RELOAD_MESSAGE_RELOADED,
            "plan": plan,
            "reload_result": {
                "mode": NGINX_RELOAD_MODE_SIMULATED,
                "shell_execution": False,
                "real_nginx_reload": False,
            },
            "reloaded_at": self._now(),
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
