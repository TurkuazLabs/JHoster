# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\web_server_profile_registry_repository.py
# 📌 Amac: JHoster web server profile secim kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Apache/Nginx aktif web server secimini tek current profile olarak JSON storage uzerinde yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import (
    WEB_SERVER_PROFILE_LEGACY_SELECTED_KEY,
    WEB_SERVER_PROFILE_RECORDS_KEY,
    WEB_SERVER_PROFILE_REGISTRY_FILE_NAME,
    WEB_SERVER_PROFILE_STATUS_SELECTED,
)


class WebServerProfileRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / WEB_SERVER_PROFILE_REGISTRY_FILE_NAME

    def list_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        profile_records = registry_data.get(WEB_SERVER_PROFILE_RECORDS_KEY, [])

        if not isinstance(profile_records, list):
            return []

        return sorted(
            profile_records,
            key=lambda item: str(item.get("selected_at", item.get("stored_at", ""))),
            reverse=True,
        )

    def get_current_profile(self) -> dict[str, Any] | None:
        for profile_record in self.list_records():
            if str(profile_record.get("status", "")).strip().lower() == WEB_SERVER_PROFILE_STATUS_SELECTED:
                return profile_record

        return None

    def append_record(self, profile_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        profile_records = registry_data.get(WEB_SERVER_PROFILE_RECORDS_KEY, [])

        if not isinstance(profile_records, list):
            profile_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **profile_data,
            "stored_at": now_value,
        }

        profile_records.append(stored_item)
        registry_data[WEB_SERVER_PROFILE_RECORDS_KEY] = profile_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {WEB_SERVER_PROFILE_RECORDS_KEY: []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {WEB_SERVER_PROFILE_RECORDS_KEY: []}

        if WEB_SERVER_PROFILE_RECORDS_KEY not in loaded_data:
            legacy_records = loaded_data.get(WEB_SERVER_PROFILE_LEGACY_SELECTED_KEY, [])
            loaded_data[WEB_SERVER_PROFILE_RECORDS_KEY] = legacy_records if isinstance(legacy_records, list) else []

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
