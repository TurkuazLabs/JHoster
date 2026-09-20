# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\state_repository.py
# 📌 Amac: JHoster agent durum bilgisini storage icinde saklar ve okur
# 📌 Modul - FileType
# Version: 1.0.1
# Aciklama: Agent state dosya repository katmani
# Bagimli Oldugu Katman: Repo

import json
from pathlib import Path
from typing import Any

from config.constants import DEFAULT_AGENT_STATE, STATE_FILE_NAME


class StateRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.state_file_path = self.storage_path / STATE_FILE_NAME

    def get_state(self) -> dict[str, Any]:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        if not self.state_file_path.exists():
            self._write_state(DEFAULT_AGENT_STATE)

        with self.state_file_path.open("r", encoding="utf-8") as state_file:
            return json.load(state_file)

    def _write_state(self, state_data: dict[str, Any]) -> None:
        with self.state_file_path.open("w", encoding="utf-8") as state_file:
            json.dump(state_data, state_file, indent=2)
