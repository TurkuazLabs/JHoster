# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\apache_config_publisher_tool.py
# 📌 Amac: Snapshot altinda uretilmis Apache virtual host config dosyasini guvenli publish hedefine kopyalar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Dry-run planlama, path guvenligi, backup, checksum ve dosya kopyalama islemlerini yapar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import hashlib
import shutil

from config.constants import (
    APACHE_PUBLISHED_DIRECTORY_NAME,
    APACHE_PUBLISH_MESSAGE_DRY_RUN,
    APACHE_PUBLISH_MESSAGE_PUBLISHED,
    APACHE_PUBLISH_MESSAGE_REJECTED,
    APACHE_PUBLISH_STATUS_PLANNED,
    APACHE_PUBLISH_STATUS_PUBLISHED,
    APACHE_PUBLISH_STATUS_REJECTED,
    APACHE_VHOST_DIRECTORY_NAME,
    APACHE_VHOST_EXTENSION,
    BACKUP_DIRECTORY_NAME,
    CHECKSUM_ALGORITHM_SHA256,
    PUBLISH_DIRECTORY_NAME,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class ApacheConfigPublisherTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.source_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / APACHE_VHOST_DIRECTORY_NAME
        ).resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / APACHE_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.backup_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / PUBLISH_DIRECTORY_NAME / APACHE_VHOST_DIRECTORY_NAME / BACKUP_DIRECTORY_NAME
        ).resolve()

    def build_publish_plan(
        self,
        project_code: str,
        source_config_file: Path,
        target_dir: str,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        source_path = source_config_file.resolve()
        target_directory_path = self._resolve_target_dir(target_dir)
        target_file_path = (target_directory_path / f"{normalized_project_code}{APACHE_VHOST_EXTENSION}").resolve()

        source_exists = source_path.is_file()
        source_is_safe = self._is_inside_path(source_path, self.source_root_path)
        source_extension_is_safe = source_path.suffix == APACHE_VHOST_EXTENSION
        target_is_safe = self._is_inside_path(target_file_path, self.publish_root_path)
        target_extension_is_safe = target_file_path.suffix == APACHE_VHOST_EXTENSION

        return {
            "project_code": normalized_project_code,
            "source_config_file": self._to_relative(source_path),
            "source_config_file_absolute": str(source_path),
            "target_dir": self._to_relative(target_directory_path),
            "target_dir_absolute": str(target_directory_path),
            "target_file": self._to_relative(target_file_path),
            "target_file_absolute": str(target_file_path),
            "source_exists": source_exists,
            "source_is_safe": source_is_safe,
            "source_extension_is_safe": source_extension_is_safe,
            "target_is_safe": target_is_safe,
            "target_extension_is_safe": target_extension_is_safe,
            "safe": source_exists and source_is_safe and source_extension_is_safe and target_is_safe and target_extension_is_safe,
            "planned_at": self._now(),
        }

    def publish_config(
        self,
        project_code: str,
        source_config_file: Path,
        target_dir: str,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_publish_plan(project_code, source_config_file, target_dir)

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": APACHE_PUBLISH_STATUS_REJECTED,
                "message": APACHE_PUBLISH_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": APACHE_PUBLISH_STATUS_PLANNED,
                "message": APACHE_PUBLISH_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        source_path = Path(str(plan.get("source_config_file_absolute"))).resolve()
        target_path = Path(str(plan.get("target_file_absolute"))).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        backup_result = self._backup_existing_file(target_path)
        shutil.copy2(source_path, target_path)

        source_checksum = self._calculate_sha256(source_path)
        target_checksum = self._calculate_sha256(target_path)

        return {
            "success": True,
            "status": APACHE_PUBLISH_STATUS_PUBLISHED,
            "message": APACHE_PUBLISH_MESSAGE_PUBLISHED,
            "plan": plan,
            "backup": backup_result,
            "checksum": {
                "algorithm": CHECKSUM_ALGORITHM_SHA256,
                "source": source_checksum,
                "target": target_checksum,
                "valid": source_checksum == target_checksum,
            },
            "published_at": self._now(),
        }

    def _resolve_target_dir(self, target_dir: str) -> Path:
        cleaned_target_dir = str(target_dir or "").strip()

        if not cleaned_target_dir:
            return self.publish_root_path

        configured_target_dir = Path(cleaned_target_dir)
        if configured_target_dir.is_absolute():
            return configured_target_dir.resolve()

        return (self.root_path / cleaned_target_dir).resolve()

    def _backup_existing_file(self, target_path: Path) -> dict[str, Any]:
        if not target_path.is_file():
            return {
                "created": False,
                "reason": "target file does not exist",
            }

        self.backup_root_path.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        backup_file_path = (self.backup_root_path / f"{target_path.stem}.{timestamp}{target_path.suffix}").resolve()
        shutil.copy2(target_path, backup_file_path)

        return {
            "created": True,
            "backup_file": self._to_relative(backup_file_path),
            "backup_file_absolute": str(backup_file_path),
        }

    def _calculate_sha256(self, file_path: Path) -> str:
        digest = hashlib.sha256()

        with file_path.open("rb") as config_file:
            for chunk in iter(lambda: config_file.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()

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
