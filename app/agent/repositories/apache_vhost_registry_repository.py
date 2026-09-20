# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\apache_vhost_registry_repository.py
# 📌 Amac: JHoster Apache virtual host kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache vhost listeleme, detay okuma ve upsert islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import APACHE_VHOST_REGISTRY_FILE_NAME, APACHE_VHOST_STATUS_GENERATED


class ApacheVhostRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / APACHE_VHOST_REGISTRY_FILE_NAME

    def list_virtual_hosts(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        virtual_hosts = registry_data.get("apache_virtual_hosts", [])

        if not isinstance(virtual_hosts, list):
            return []

        return sorted(virtual_hosts, key=lambda item: str(item.get("project_code", "")))

    def get_virtual_host(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for virtual_host_item in self.list_virtual_hosts():
            if str(virtual_host_item.get("project_code", "")).strip().lower() == normalized_code:
                return virtual_host_item

        return None

    def upsert_virtual_host(self, virtual_host_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        virtual_hosts = registry_data.get("apache_virtual_hosts", [])

        if not isinstance(virtual_hosts, list):
            virtual_hosts = []

        project_code = str(virtual_host_data.get("project_code", "")).strip().lower()
        if not project_code:
            raise ValueError("project code is required")

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            "status": APACHE_VHOST_STATUS_GENERATED,
            "created_at": now_value,
            **virtual_host_data,
            "updated_at": now_value,
        }

        replaced = False
        for index, virtual_host_item in enumerate(virtual_hosts):
            if str(virtual_host_item.get("project_code", "")).strip().lower() == project_code:
                stored_item = {
                    **virtual_host_item,
                    **virtual_host_data,
                    "updated_at": now_value,
                }
                virtual_hosts[index] = stored_item
                replaced = True
                break

        if not replaced:
            virtual_hosts.append(stored_item)

        registry_data["apache_virtual_hosts"] = virtual_hosts
        self._write_registry(registry_data)
        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"apache_virtual_hosts": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"apache_virtual_hosts": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
