# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\hosts_auto_registry_repository.py
# 📌 Amac: JHoster otomatik hosts senkron kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Hosts auto sync gecmisini, son sync kaydini ve sistem dosyasi yazma sonucunu repo katmaninda yonetir
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import HOSTS_AUTO_REGISTRY_FILE_NAME


class HostsAutoRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / HOSTS_AUTO_REGISTRY_FILE_NAME

    def list_sync_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        sync_records = registry_data.get("sync_records", [])

        if not isinstance(sync_records, list):
            return []

        return sorted(
            sync_records,
            key=lambda item: str(item.get("synced_at", item.get("stored_at", ""))),
            reverse=True,
        )

    def get_latest_sync(self) -> dict[str, Any] | None:
        sync_records = self.list_sync_records()
        if not sync_records:
            return None
        return sync_records[0]

    def append_sync_record(self, sync_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        sync_records = registry_data.get("sync_records", [])

        if not isinstance(sync_records, list):
            sync_records = []

        stored_item = {
            **sync_data,
            "stored_at": self._now(),
        }
        sync_records.append(stored_item)
        registry_data["sync_records"] = sync_records
        self._write_registry(registry_data)
        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"sync_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"sync_records": []}

        loaded_data.setdefault("sync_records", [])
        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
