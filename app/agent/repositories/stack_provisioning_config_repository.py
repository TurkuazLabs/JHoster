# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\stack_provisioning_config_repository.py
# 📌 Amac: Stack provisioning YAML config kaydini okur
# 📌 Modul - Python
# Version: 3.77.0
# Aciklama: Installer, runtime component ve database wizard eslemelerini storage katmanindan servis katmanina sunar
# Bagimli Oldugu Katman: Repo

from pathlib import Path
from typing import Any

import yaml


class StackProvisioningConfigRepository:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path

    def get_config(self) -> dict[str, Any]:
        if not self.config_path.is_file():
            return {}

        with self.config_path.open("r", encoding="utf-8") as config_file:
            data = yaml.safe_load(config_file) or {}

        return data if isinstance(data, dict) else {}
