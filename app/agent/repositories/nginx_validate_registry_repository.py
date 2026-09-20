# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\nginx_validate_registry_repository.py
# 📌 Amac: JHoster Nginx validate kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Validate listeleme, son validate okuma ve append islemlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import NGINX_VALIDATE_REGISTRY_FILE_NAME


class NginxValidateRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / NGINX_VALIDATE_REGISTRY_FILE_NAME

    def list_validation_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        validation_records = registry_data.get("validation_records", [])

        if not isinstance(validation_records, list):
            return []

        return sorted(
            validation_records,
            key=lambda item: str(item.get("validated_at", "")),
            reverse=True,
        )

    def get_latest_validation(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for validation_item in self.list_validation_records():
            if str(validation_item.get("project_code", "")).strip().lower() == normalized_code:
                return validation_item

        return None

    def append_validation_record(self, validation_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        validation_records = registry_data.get("validation_records", [])

        if not isinstance(validation_records, list):
            validation_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **validation_data,
            "stored_at": now_value,
        }

        validation_records.append(stored_item)
        registry_data["validation_records"] = validation_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"validation_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"validation_records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
