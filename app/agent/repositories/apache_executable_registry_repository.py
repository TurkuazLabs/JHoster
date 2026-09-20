# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\apache_executable_registry_repository.py
# 📌 Amac: JHoster Apache executable tespit kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache executable listeleme, son kayit okuma ve append islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import APACHE_EXECUTABLE_REGISTRY_FILE_NAME


class ApacheExecutableRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / APACHE_EXECUTABLE_REGISTRY_FILE_NAME

    def list_detection_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        detection_records = registry_data.get("detection_records", [])

        if not isinstance(detection_records, list):
            return []

        return sorted(
            detection_records,
            key=lambda item: str(item.get("detected_at", item.get("stored_at", ""))),
            reverse=True,
        )

    def get_latest_detection(self) -> dict[str, Any] | None:
        detection_records = self.list_detection_records()

        if not detection_records:
            return None

        return detection_records[0]

    def append_detection_record(self, detection_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        detection_records = registry_data.get("detection_records", [])

        if not isinstance(detection_records, list):
            detection_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **detection_data,
            "stored_at": now_value,
        }

        detection_records.append(stored_item)
        registry_data["detection_records"] = detection_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"detection_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"detection_records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
