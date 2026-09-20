# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\quick_app_registry_repository.py
# 📌 Amac: JHoster Quick App olusturma kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Quick App create/plan sonuc kayitlarini listeleme, detay okuma ve upsert islemleriyle yonetir
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import QUICK_APP_REGISTRY_FILE_NAME


class QuickAppRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / QUICK_APP_REGISTRY_FILE_NAME

    def list_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        records = registry_data.get("records", [])

        if not isinstance(records, list):
            return []

        return sorted(records, key=lambda item: str(item.get("created_at", "")), reverse=True)

    def get_latest_record(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for record_item in self.list_records():
            if str(record_item.get("project_code", "")).strip().lower() == normalized_code:
                return record_item

        return None

    def append_record(self, record_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        records = registry_data.get("records", [])

        if not isinstance(records, list):
            records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **record_data,
            "created_at": now_value,
        }
        records.append(stored_item)
        registry_data["records"] = records
        self._write_registry(registry_data)
        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
