# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\web_server_workflow_lock_repository.py
# 📌 Amac: Unified web server workflow aktif kilitlerini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Proje bazli workflow lock acquire, release, list ve force unlock islemlerini yapar
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import (
    WEB_SERVER_WORKFLOW_ERROR_LOCK_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_LOCK_RUN_MISMATCH,
    WEB_SERVER_WORKFLOW_ERROR_LOCKED,
    WEB_SERVER_WORKFLOW_LOCK_REGISTRY_FILE_NAME,
    WEB_SERVER_WORKFLOW_LOCK_STATUS_ACTIVE,
    WEB_SERVER_WORKFLOW_LOCK_STATUS_RELEASED,
    WEB_SERVER_WORKFLOW_MESSAGE_LOCK_ACQUIRED,
    WEB_SERVER_WORKFLOW_MESSAGE_LOCK_RELEASED,
    WEB_SERVER_WORKFLOW_MESSAGE_LOCKED,
)


class WebServerWorkflowLockRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / WEB_SERVER_WORKFLOW_LOCK_REGISTRY_FILE_NAME

    def list_locks(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        active_locks = registry_data.get("active_locks", [])

        if not isinstance(active_locks, list):
            return []

        return sorted(
            [item for item in active_locks if isinstance(item, dict)],
            key=lambda item: str(item.get("locked_at", "")),
            reverse=True,
        )

    def get_project_lock(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = self._normalize_project_code(project_code)

        for lock_record in self.list_locks():
            if str(lock_record.get("project_code", "")).strip().lower() == normalized_code:
                return lock_record

        return None

    def acquire_lock(self, project_code: str, run_id: str, server_code: str) -> dict[str, Any]:
        normalized_code = self._normalize_project_code(project_code)
        active_lock = self.get_project_lock(normalized_code)

        if active_lock is not None:
            return {
                "success": False,
                "status": WEB_SERVER_WORKFLOW_LOCK_STATUS_ACTIVE,
                "message": WEB_SERVER_WORKFLOW_MESSAGE_LOCKED,
                "error": WEB_SERVER_WORKFLOW_ERROR_LOCKED,
                "project_code": normalized_code,
                "active_lock": active_lock,
            }

        lock_record = {
            "project_code": normalized_code,
            "run_id": str(run_id).strip().lower(),
            "web_server": str(server_code).strip().lower(),
            "status": WEB_SERVER_WORKFLOW_LOCK_STATUS_ACTIVE,
            "locked_at": datetime.now(timezone.utc).isoformat(),
        }

        registry_data = self._read_registry()
        active_locks = registry_data.get("active_locks", [])
        if not isinstance(active_locks, list):
            active_locks = []

        active_locks.append(lock_record)
        registry_data["active_locks"] = active_locks
        self._write_registry(registry_data)

        return {
            "success": True,
            "status": WEB_SERVER_WORKFLOW_LOCK_STATUS_ACTIVE,
            "message": WEB_SERVER_WORKFLOW_MESSAGE_LOCK_ACQUIRED,
            "lock": lock_record,
        }

    def release_lock(self, project_code: str, run_id: str, force: bool = False) -> dict[str, Any]:
        normalized_code = self._normalize_project_code(project_code)
        normalized_run_id = str(run_id).strip().lower()
        registry_data = self._read_registry()
        active_locks = registry_data.get("active_locks", [])

        if not isinstance(active_locks, list):
            active_locks = []

        if not force and not normalized_run_id:
            active_lock = self.get_project_lock(normalized_code)
            if active_lock is not None:
                return {
                    "success": False,
                    "project_code": normalized_code,
                    "run_id": normalized_run_id,
                    "error": WEB_SERVER_WORKFLOW_ERROR_LOCK_RUN_MISMATCH,
                    "active_lock": active_lock,
                }

        kept_locks = []
        released_lock: dict[str, Any] | None = None

        for lock_record in active_locks:
            if not isinstance(lock_record, dict):
                continue

            lock_project_code = str(lock_record.get("project_code", "")).strip().lower()
            lock_run_id = str(lock_record.get("run_id", "")).strip().lower()

            if lock_project_code != normalized_code:
                kept_locks.append(lock_record)
                continue

            if not force and normalized_run_id and lock_run_id != normalized_run_id:
                kept_locks.append(lock_record)
                continue

            released_lock = {
                **lock_record,
                "status": WEB_SERVER_WORKFLOW_LOCK_STATUS_RELEASED,
                "released_at": datetime.now(timezone.utc).isoformat(),
                "released_by_force": bool(force),
            }

        if released_lock is None:
            active_lock = self.get_project_lock(normalized_code)
            if active_lock is not None:
                return {
                    "success": False,
                    "project_code": normalized_code,
                    "run_id": normalized_run_id,
                    "error": WEB_SERVER_WORKFLOW_ERROR_LOCK_RUN_MISMATCH,
                    "active_lock": active_lock,
                }

            return {
                "success": False,
                "project_code": normalized_code,
                "run_id": normalized_run_id,
                "error": WEB_SERVER_WORKFLOW_ERROR_LOCK_NOT_FOUND,
            }

        registry_data["active_locks"] = kept_locks
        self._write_registry(registry_data)

        return {
            "success": True,
            "status": WEB_SERVER_WORKFLOW_LOCK_STATUS_RELEASED,
            "message": WEB_SERVER_WORKFLOW_MESSAGE_LOCK_RELEASED,
            "lock": released_lock,
        }

    def _normalize_project_code(self, project_code: str) -> str:
        return str(project_code).strip().lower()

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"active_locks": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"active_locks": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
