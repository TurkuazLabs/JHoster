# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\execution_log_repository.py
# 📌 Amac: JHoster install execution gecmisini JSON olarak saklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Executor history okuma ve yazma repository katmani
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import INSTALL_HISTORY_FILE_NAME


class ExecutionLogRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.history_file_path = storage_path / INSTALL_HISTORY_FILE_NAME

    def append_execution(self, execution_data: dict[str, Any]) -> dict[str, Any]:
        history_items = self.get_history()
        stored_item = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            **execution_data,
        }
        history_items.append(stored_item)
        self._write_history(history_items)
        return stored_item

    def get_history(self) -> list[dict[str, Any]]:
        if not self.history_file_path.exists():
            return []

        with self.history_file_path.open("r", encoding="utf-8") as history_file:
            loaded_data = json.load(history_file)

        if not isinstance(loaded_data, list):
            return []

        return loaded_data

    def _write_history(self, history_items: list[dict[str, Any]]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.history_file_path.open("w", encoding="utf-8") as history_file:
            json.dump(history_items, history_file, indent=2, ensure_ascii=False)
