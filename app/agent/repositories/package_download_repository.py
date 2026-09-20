# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\package_download_repository.py
# 📌 Amac: Otomatik indirilebilir paket katalog kayitlarini okur
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: package_download_registry.json uzerinden package downloader repo katmani
# Bagimli Oldugu Katman: Repo

from pathlib import Path
from typing import Any
import json

from config.constants import PACKAGE_DOWNLOAD_REGISTRY_FILE_NAME


class PackageDownloadRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_path = storage_path / PACKAGE_DOWNLOAD_REGISTRY_FILE_NAME

    def list_packages(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        packages = registry_data.get("packages", [])
        if not isinstance(packages, list):
            return []

        return [package for package in packages if isinstance(package, dict)]

    def get_package(self, package_code: str) -> dict[str, Any] | None:
        normalized_code = str(package_code or "").strip()
        for package in self.list_packages():
            if str(package.get("code", "")).strip() == normalized_code:
                return package
        return None

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_path.exists():
            return {"packages": []}

        with self.registry_path.open("r", encoding="utf-8") as registry_file:
            data = json.load(registry_file)

        return data if isinstance(data, dict) else {"packages": []}
