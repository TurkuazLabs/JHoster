# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\hosts_publish_registry_repository.py
# 📌 Amac: JHoster hosts publish kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Hosts publish listeleme, son kayit okuma ve append islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import HOSTS_PUBLISH_REGISTRY_FILE_NAME


class HostsPublishRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / HOSTS_PUBLISH_REGISTRY_FILE_NAME

    def list_publish_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        publish_records = registry_data.get("publish_records", [])

        if not isinstance(publish_records, list):
            return []

        return sorted(
            publish_records,
            key=lambda item: str(item.get("published_at", "")),
            reverse=True,
        )

    def get_latest_publish(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for publish_item in self.list_publish_records():
            if str(publish_item.get("project_code", "")).strip().lower() == normalized_code:
                return publish_item

        return None

    def append_publish_record(self, publish_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        publish_records = registry_data.get("publish_records", [])

        if not isinstance(publish_records, list):
            publish_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **publish_data,
            "stored_at": now_value,
        }

        publish_records.append(stored_item)
        registry_data["publish_records"] = publish_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"publish_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"publish_records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
