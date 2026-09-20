# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\app_registry_repository.py
# 📌 Amac: Kurulan JHoster app/component kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: App registry okuma, yazma ve component durum sorgulama repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import APP_REGISTRY_FILE_NAME, APP_STATUS_INSTALLED, APP_STATUS_UNKNOWN


class AppRegistryRepository:
    def __init__(self, storage_path: Path, root_path: Path) -> None:
        self.storage_path = storage_path
        self.root_path = root_path.resolve()
        self.registry_file_path = storage_path / APP_REGISTRY_FILE_NAME

    def list_apps(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        apps = registry_data.get("apps", [])

        if not isinstance(apps, list):
            return []

        return sorted(apps, key=lambda app: str(app.get("code", "")))

    def get_app(self, component_code: str) -> dict[str, Any] | None:
        normalized_code = str(component_code).strip()

        for app_item in self.list_apps():
            if str(app_item.get("code")) == normalized_code:
                return app_item

        return None

    def get_status(self, component_code: str) -> str:
        app_item = self.get_app(component_code)

        if app_item is None:
            return APP_STATUS_UNKNOWN

        return str(app_item.get("status", APP_STATUS_INSTALLED))

    def upsert_app(self, app_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        apps = registry_data.get("apps", [])

        if not isinstance(apps, list):
            apps = []

        component_code = str(app_data.get("code", "")).strip()
        if not component_code:
            raise ValueError("app code is required")

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            "status": APP_STATUS_INSTALLED,
            "first_installed_at": now_value,
            **app_data,
            "updated_at": now_value,
        }

        replaced = False
        for index, app_item in enumerate(apps):
            if str(app_item.get("code")) == component_code:
                stored_item["first_installed_at"] = str(app_item.get("first_installed_at", now_value))
                apps[index] = {**app_item, **stored_item}
                replaced = True
                break

        if not replaced:
            apps.append(stored_item)

        registry_data["apps"] = apps
        self._write_registry(registry_data)
        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"apps": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"apps": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
