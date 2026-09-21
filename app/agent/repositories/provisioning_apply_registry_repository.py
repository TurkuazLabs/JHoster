# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\provisioning_apply_registry_repository.py
# 📌 Amac: Provisioning apply calisma kayitlarini JSON storage uzerinde saklar
# 📌 Modul - Python
# Version: 3.78.0
# Aciklama: New Site apply run listesi, proje bazli son kayit ve yeni run ekleme repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import PROVISIONING_APPLY_REGISTRY_FILE_NAME


class ProvisioningApplyRegistryRepository:
    RECORDS_KEY = "records"

    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_path = storage_path / PROVISIONING_APPLY_REGISTRY_FILE_NAME

    def list_records(self) -> list[dict[str, Any]]:
        data = self._read_registry()
        records = data.get(self.RECORDS_KEY, [])
        if not isinstance(records, list):
            return []
        return sorted(
            [item for item in records if isinstance(item, dict)],
            key=lambda item: str(item.get("created_at", "")),
            reverse=True,
        )

    def get_latest_record(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code or "").strip().lower()
        for item in self.list_records():
            if str(item.get("project_code", "")).strip().lower() == normalized_code:
                return item
        return None

    def append_record(self, record: dict[str, Any]) -> dict[str, Any]:
        data = self._read_registry()
        records = data.get(self.RECORDS_KEY, [])
        if not isinstance(records, list):
            records = []

        stored = {
            **record,
            "created_at": str(record.get("created_at") or datetime.now(timezone.utc).isoformat()),
        }
        records.append(stored)
        data[self.RECORDS_KEY] = records
        self._write_registry(data)
        return stored

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            return {"schema_version": "1.0.0", self.RECORDS_KEY: []}
        with self.registry_path.open("r", encoding="utf-8") as registry_file:
            loaded = json.load(registry_file)
        if not isinstance(loaded, dict):
            return {"schema_version": "1.0.0", self.RECORDS_KEY: []}
        return loaded

    def _write_registry(self, data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)
        with self.registry_path.open("w", encoding="utf-8") as registry_file:
            json.dump(data, registry_file, indent=2, ensure_ascii=False)
