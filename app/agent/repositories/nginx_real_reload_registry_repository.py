# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\nginx_real_reload_registry_repository.py
# 📌 Amac: JHoster Nginx real reload kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Real reload listeleme, son kayit okuma ve append islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import NGINX_REAL_RELOAD_REGISTRY_FILE_NAME


class NginxRealReloadRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / NGINX_REAL_RELOAD_REGISTRY_FILE_NAME

    def list_real_reload_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        reload_records = registry_data.get("real_reload_records", [])

        if not isinstance(reload_records, list):
            return []

        return sorted(
            reload_records,
            key=lambda item: str(item.get("reloaded_at", item.get("stored_at", ""))),
            reverse=True,
        )

    def get_latest_real_reload(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for reload_item in self.list_real_reload_records():
            if str(reload_item.get("project_code", "")).strip().lower() == normalized_code:
                return reload_item

        return None

    def append_real_reload_record(self, reload_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        reload_records = registry_data.get("real_reload_records", [])

        if not isinstance(reload_records, list):
            reload_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **reload_data,
            "stored_at": now_value,
        }

        reload_records.append(stored_item)
        registry_data["real_reload_records"] = reload_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"real_reload_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"real_reload_records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
