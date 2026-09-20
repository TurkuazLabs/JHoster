# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\web_server_workflow_rollback_tool.py
# 📌 Amac: Unified web server workflow icin publish sonrasi guvenli rollback islemini yapar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Publish sonucundaki backup bilgisini kullanarak eski vhost config dosyasini geri yukler veya yeni dosyayi kaldirir
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import shutil

from config.constants import (
    APACHE_PUBLISHED_DIRECTORY_NAME,
    APACHE_VHOST_DIRECTORY_NAME,
    BACKUP_DIRECTORY_NAME,
    NGINX_PUBLISHED_DIRECTORY_NAME,
    NGINX_VHOST_DIRECTORY_NAME,
    PUBLISH_DIRECTORY_NAME,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
    WEB_SERVER_CODE_APACHE,
    WEB_SERVER_CODE_NGINX,
    WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_PATH_BLOCKED,
    WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_SOURCE_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_TARGET_NOT_FOUND,
    WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_COMPLETED,
    WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_DRY_RUN,
    WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_SKIPPED,
    WEB_SERVER_WORKFLOW_STATUS_PLANNED,
    WEB_SERVER_WORKFLOW_STATUS_ROLLED_BACK,
    WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
)


class WebServerWorkflowRollbackTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.nginx_publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.apache_publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / APACHE_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.nginx_backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / PUBLISH_DIRECTORY_NAME / NGINX_VHOST_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()
        self.apache_backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / PUBLISH_DIRECTORY_NAME / APACHE_VHOST_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()

    def build_rollback_plan(self, server_code: str, publish_result: dict[str, Any]) -> dict[str, Any]:
        normalized_server_code = str(server_code).strip().lower()
        plan = publish_result.get("plan", {})
        backup = publish_result.get("backup", {})

        if not isinstance(plan, dict):
            plan = {}

        if not isinstance(backup, dict):
            backup = {}

        target_file = self._resolve_record_path(str(plan.get("target_file_absolute") or plan.get("target_file") or ""))
        backup_file = self._resolve_record_path(str(backup.get("backup_file_absolute") or backup.get("backup_file") or ""))
        publish_root_path = self._get_publish_root_path(normalized_server_code)
        backup_root_path = self._get_backup_root_path(normalized_server_code)
        backup_created = backup.get("created") is True
        target_is_safe = target_file is not None and self._is_inside_path(target_file, publish_root_path)
        backup_is_safe = backup_file is not None and self._is_inside_path(backup_file, backup_root_path)
        backup_exists = backup_file is not None and backup_file.is_file()
        target_exists = target_file is not None and target_file.is_file()

        return {
            "server_code": normalized_server_code,
            "target_file": self._to_relative_or_empty(target_file),
            "target_file_absolute": str(target_file) if target_file is not None else "",
            "target_exists": target_exists,
            "target_is_safe": target_is_safe,
            "backup_file": self._to_relative_or_empty(backup_file),
            "backup_file_absolute": str(backup_file) if backup_file is not None else "",
            "backup_created": backup_created,
            "backup_exists": backup_exists,
            "backup_is_safe": backup_is_safe,
            "safe": target_is_safe and target_file is not None and (not backup_created or (backup_is_safe and backup_exists)),
            "planned_at": self._now(),
        }

    def rollback_publish_result(
        self,
        server_code: str,
        publish_result: dict[str, Any],
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_rollback_plan(server_code=server_code, publish_result=publish_result)

        if not plan.get("target_is_safe", False):
            return {
                "success": False,
                "status": WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
                "message": WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_SKIPPED,
                "error": WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_PATH_BLOCKED,
                "plan": plan,
            }

        if not plan.get("target_exists", False):
            return {
                "success": False,
                "status": WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
                "message": WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_SKIPPED,
                "error": WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_TARGET_NOT_FOUND,
                "plan": plan,
            }

        if plan.get("backup_created", False) and not plan.get("backup_exists", False):
            return {
                "success": False,
                "status": WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
                "message": WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_SKIPPED,
                "error": WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_SOURCE_NOT_FOUND,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": WEB_SERVER_WORKFLOW_STATUS_PLANNED,
                "message": WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_DRY_RUN,
                "plan": plan,
            }

        target_file = Path(str(plan.get("target_file_absolute"))).resolve()

        if plan.get("backup_created", False):
            backup_file = Path(str(plan.get("backup_file_absolute"))).resolve()
            shutil.copy2(backup_file, target_file)
            rollback_action = "restored_backup"
        else:
            target_file.unlink()
            rollback_action = "removed_created_file"

        return {
            "success": True,
            "status": WEB_SERVER_WORKFLOW_STATUS_ROLLED_BACK,
            "message": WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_COMPLETED,
            "plan": plan,
            "rollback_result": {
                "action": rollback_action,
                "target_file": self._to_relative_or_empty(target_file),
            },
            "rolled_back_at": self._now(),
        }

    def _get_publish_root_path(self, server_code: str) -> Path:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_publish_root_path

        return self.nginx_publish_root_path

    def _get_backup_root_path(self, server_code: str) -> Path:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_backup_root_path

        return self.nginx_backup_root_path

    def _resolve_record_path(self, raw_path: str) -> Path | None:
        cleaned_path = str(raw_path or "").strip()

        if not cleaned_path:
            return None

        normalized_path = cleaned_path.replace("\\", "/")
        path = Path(normalized_path)

        if path.is_absolute():
            return path.resolve()

        return (self.root_path / path).resolve()

    def _is_inside_path(self, target_path: Path, parent_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(parent_path.resolve())
            return True
        except ValueError:
            return False

    def _to_relative_or_empty(self, target_path: Path | None) -> str:
        if target_path is None:
            return ""

        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
