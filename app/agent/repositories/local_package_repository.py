# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\local_package_repository.py
# 📌 Amac: Local package uyumlu manifestleri katalogdan secer
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Manifest repository uzerinden local package filtreleme repo katmani
# Bagimli Oldugu Katman: Repo

from typing import Any

from config.constants import INSTALLER_MODE_KEY, INSTALLER_MODE_LOCAL_PACKAGE, INSTALLER_SECTION_KEY
from repositories.manifest_repository import ManifestRepository


class LocalPackageRepository:
    def __init__(self, manifest_repository: ManifestRepository) -> None:
        self.manifest_repository = manifest_repository

    def get_all_local_package_manifests(self) -> list[dict[str, Any]]:
        return [
            manifest_item
            for manifest_item in self.manifest_repository.get_all_manifests()
            if self._is_local_package_manifest(manifest_item)
        ]

    def get_local_package_manifest_by_code(self, component_code: str) -> dict[str, Any] | None:
        normalized_code = str(component_code).strip()

        for manifest_item in self.get_all_local_package_manifests():
            package_data = manifest_item.get("content", {}).get("package", {})
            if str(package_data.get("code")) == normalized_code:
                return manifest_item

        return None

    def _is_local_package_manifest(self, manifest_item: dict[str, Any]) -> bool:
        installer_data = manifest_item.get("content", {}).get(INSTALLER_SECTION_KEY, {})
        return str(installer_data.get(INSTALLER_MODE_KEY, "")).strip() == INSTALLER_MODE_LOCAL_PACKAGE
