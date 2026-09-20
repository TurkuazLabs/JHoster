# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\hosts_apply_registry_repository.py
# 📌 Amac: JHoster hosts apply ve rollback kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apply kayitlari, son kayit okuma ve rollback kayit ekleme islemlerini yonetir
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import HOSTS_APPLY_REGISTRY_FILE_NAME


class HostsApplyRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / HOSTS_APPLY_REGISTRY_FILE_NAME

    def list_apply_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        apply_records = registry_data.get("apply_records", [])

        if not isinstance(apply_records, list):
            return []

        return sorted(
            apply_records,
            key=lambda item: str(item.get("applied_at", "")),
            reverse=True,
        )

    def list_rollback_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        rollback_records = registry_data.get("rollback_records", [])

        if not isinstance(rollback_records, list):
            return []

        return sorted(
            rollback_records,
            key=lambda item: str(item.get("rolled_back_at", "")),
            reverse=True,
        )

    def get_latest_apply(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for apply_item in self.list_apply_records():
            if str(apply_item.get("project_code", "")).strip().lower() == normalized_code:
                return apply_item

        return None

    def append_apply_record(self, apply_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        apply_records = registry_data.get("apply_records", [])

        if not isinstance(apply_records, list):
            apply_records = []

        stored_item = {
            **apply_data,
            "stored_at": self._now(),
        }

        apply_records.append(stored_item)
        registry_data["apply_records"] = apply_records
        self._write_registry(registry_data)

        return stored_item

    def append_rollback_record(self, rollback_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        rollback_records = registry_data.get("rollback_records", [])

        if not isinstance(rollback_records, list):
            rollback_records = []

        stored_item = {
            **rollback_data,
            "stored_at": self._now(),
        }

        rollback_records.append(stored_item)
        registry_data["rollback_records"] = rollback_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {
                "apply_records": [],
                "rollback_records": [],
            }

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {
                "apply_records": [],
                "rollback_records": [],
            }

        loaded_data.setdefault("apply_records", [])
        loaded_data.setdefault("rollback_records", [])
        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
