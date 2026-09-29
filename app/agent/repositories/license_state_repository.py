# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\license_state_repository.py
# 📌 Amac: JHoster plan ve lisans durumunu JSON dosyasindan okur
# 📌 Modul - FileType
# Version: 3.80.0
# Aciklama: Legacy local plan state'i guvenli okur; eksik, bozuk veya gecersiz dosyada Community fallback saglar
# Bagimli Oldugu Katman: Repo

from pathlib import Path
from typing import Any
import json

from config.constants import LICENSE_DEFAULT_PLAN, LICENSE_STATE_FILE_NAME


class LicenseStateRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.license_file_path = storage_path / LICENSE_STATE_FILE_NAME

    def get_plan_key(self) -> str:
        license_data = self._read_license_state()
        plan_key = str(license_data.get("plan_key", LICENSE_DEFAULT_PLAN)).strip().lower()

        if not plan_key:
            return LICENSE_DEFAULT_PLAN

        return plan_key

    def get_license_state(self) -> dict[str, Any]:
        license_data = self._read_license_state()
        license_data["plan_key"] = self.get_plan_key()
        return license_data

    def _read_license_state(self) -> dict[str, Any]:
        if not self.license_file_path.exists():
            return {"plan_key": LICENSE_DEFAULT_PLAN}

        try:
            with self.license_file_path.open("r", encoding="utf-8") as license_file:
                loaded_data = json.load(license_file)
        except (OSError, json.JSONDecodeError):
            return {"plan_key": LICENSE_DEFAULT_PLAN}

        if not isinstance(loaded_data, dict):
            return {"plan_key": LICENSE_DEFAULT_PLAN}

        return loaded_data
