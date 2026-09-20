# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\runtime_version_repository.py
# 📌 Amac: Aktif runtime version secimlerini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Runtime family bazli aktif component ve version secimlerini yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import RUNTIME_VERSION_STATE_FILE_NAME


class RuntimeVersionRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.state_file_path = storage_path / RUNTIME_VERSION_STATE_FILE_NAME

    def list_active_versions(self) -> list[dict[str, Any]]:
        state_data = self._read_state()
        active_versions = state_data.get("active_versions", [])

        if not isinstance(active_versions, list):
            return []

        return sorted(active_versions, key=lambda item: str(item.get("family", "")))

    def get_active_version(self, family: str) -> dict[str, Any] | None:
        normalized_family = str(family).strip()

        for active_item in self.list_active_versions():
            if str(active_item.get("family")) == normalized_family:
                return active_item

        return None

    def set_active_version(self, active_data: dict[str, Any]) -> dict[str, Any]:
        state_data = self._read_state()
        active_versions = state_data.get("active_versions", [])

        if not isinstance(active_versions, list):
            active_versions = []

        family = str(active_data.get("family", "")).strip()
        if not family:
            raise ValueError("runtime family is required")

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **active_data,
            "activated_at": now_value,
        }

        replaced = False
        for index, active_item in enumerate(active_versions):
            if str(active_item.get("family")) == family:
                active_versions[index] = {**active_item, **stored_item}
                replaced = True
                break

        if not replaced:
            active_versions.append(stored_item)

        state_data["active_versions"] = active_versions
        self._write_state(state_data)
        return stored_item

    def _read_state(self) -> dict[str, Any]:
        if not self.state_file_path.exists():
            return {"active_versions": []}

        with self.state_file_path.open("r", encoding="utf-8") as state_file:
            loaded_data = json.load(state_file)

        if not isinstance(loaded_data, dict):
            return {"active_versions": []}

        return loaded_data

    def _write_state(self, state_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.state_file_path.open("w", encoding="utf-8") as state_file:
            json.dump(state_data, state_file, indent=2, ensure_ascii=False)
