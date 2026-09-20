# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\manifest_repository.py
# 📌 Amac: JHoster module manifest YAML dosyalarini okur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Manifest dosya okuma ve arama repository katmani
# Bagimli Oldugu Katman: Repo

from pathlib import Path
from typing import Any

import yaml

from config.constants import MANIFEST_FILE_NAME


class ManifestRepository:
    def __init__(self, modules_path: Path) -> None:
        self.modules_path = modules_path

    def get_all_manifests(self) -> list[dict[str, Any]]:
        if not self.modules_path.exists():
            return []

        manifest_items: list[dict[str, Any]] = []

        for manifest_path in sorted(self.modules_path.rglob(MANIFEST_FILE_NAME)):
            manifest_items.append(self._read_manifest(manifest_path))

        return manifest_items

    def get_manifest_by_code(self, package_code: str) -> dict[str, Any] | None:
        for manifest_item in self.get_all_manifests():
            package_data = manifest_item["content"].get("package", {})
            if str(package_data.get("code")) == package_code:
                return manifest_item

        return None

    def _read_manifest(self, manifest_path: Path) -> dict[str, Any]:
        with manifest_path.open("r", encoding="utf-8") as manifest_file:
            manifest_content = yaml.safe_load(manifest_file) or {}

        return {
            "file_path": manifest_path,
            "content": manifest_content,
        }
