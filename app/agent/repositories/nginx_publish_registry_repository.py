# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\nginx_publish_registry_repository.py
# 📌 Amac: JHoster Nginx publish kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Publish listeleme, son publish okuma ve append islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import NGINX_PUBLISH_REGISTRY_FILE_NAME


class NginxPublishRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / NGINX_PUBLISH_REGISTRY_FILE_NAME

    def list_published_configs(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        published_configs = registry_data.get("published_configs", [])

        if not isinstance(published_configs, list):
            return []

        return sorted(
            published_configs,
            key=lambda item: str(item.get("published_at", "")),
            reverse=True,
        )

    def get_latest_publish(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for published_item in self.list_published_configs():
            if str(published_item.get("project_code", "")).strip().lower() == normalized_code:
                return published_item

        return None

    def append_publish_record(self, publish_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        published_configs = registry_data.get("published_configs", [])

        if not isinstance(published_configs, list):
            published_configs = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **publish_data,
            "stored_at": now_value,
        }

        published_configs.append(stored_item)
        registry_data["published_configs"] = published_configs
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"published_configs": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"published_configs": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
