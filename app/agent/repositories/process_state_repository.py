# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\process_state_repository.py
# 📌 Amac: JHoster process durum kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Runtime process status bilgisini kalici storage uzerinde yoneten repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import (
    PROCESS_STATE_FILE_NAME,
    PROCESS_STATUS_STOPPED,
    PROCESS_STATUS_UNKNOWN,
)


class ProcessStateRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.state_file_path = storage_path / PROCESS_STATE_FILE_NAME

    def list_processes(self) -> list[dict[str, Any]]:
        state_data = self._read_state()
        processes = state_data.get("processes", [])

        if not isinstance(processes, list):
            return []

        return sorted(processes, key=lambda process: str(process.get("code", "")))

    def get_process(self, component_code: str) -> dict[str, Any] | None:
        normalized_code = str(component_code).strip()

        for process_item in self.list_processes():
            if str(process_item.get("code")) == normalized_code:
                return process_item

        return None

    def get_status(self, component_code: str) -> str:
        process_item = self.get_process(component_code)

        if process_item is None:
            return PROCESS_STATUS_UNKNOWN

        return str(process_item.get("status", PROCESS_STATUS_STOPPED))

    def upsert_process(self, process_data: dict[str, Any]) -> dict[str, Any]:
        state_data = self._read_state()
        processes = state_data.get("processes", [])

        if not isinstance(processes, list):
            processes = []

        component_code = str(process_data.get("code", "")).strip()
        if not component_code:
            raise ValueError("process code is required")

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **process_data,
            "updated_at": now_value,
        }

        replaced = False
        for index, process_item in enumerate(processes):
            if str(process_item.get("code")) == component_code:
                processes[index] = {**process_item, **stored_item}
                replaced = True
                break

        if not replaced:
            processes.append(stored_item)

        state_data["processes"] = processes
        self._write_state(state_data)
        return stored_item

    def _read_state(self) -> dict[str, Any]:
        if not self.state_file_path.exists():
            return {"processes": []}

        with self.state_file_path.open("r", encoding="utf-8") as state_file:
            loaded_data = json.load(state_file)

        if not isinstance(loaded_data, dict):
            return {"processes": []}

        return loaded_data

    def _write_state(self, state_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.state_file_path.open("w", encoding="utf-8") as state_file:
            json.dump(state_data, state_file, indent=2, ensure_ascii=False)
