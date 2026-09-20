# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\manifest_validation_tool.py
# 📌 Amac: JHoster manifest verisini dogrular ve standart component formatina cevirir
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Manifest validation, runtime adapter, runtime family ve normalize tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import (
    ACTIONS_SECTION_KEY,
    DEFAULT_PACKAGE_EDITION,
    INSTALLER_SECTION_KEY,
    PACKAGE_CATEGORY_KEY,
    PACKAGE_CODE_KEY,
    PACKAGE_DESCRIPTION_KEY,
    PACKAGE_EDITION_KEY,
    PACKAGE_NAME_KEY,
    PACKAGE_SECTION_KEY,
    PACKAGE_VERSION_KEY,
    REQUIREMENTS_SECTION_KEY,
    UNKNOWN_PACKAGE_VALUE,
    SERVICE_ADAPTER_RUNTIME_KEY,
    RUNTIME_FAMILY_KEY,
)


class ManifestValidationTool:
    def normalize(self, manifest_item: dict[str, Any]) -> dict[str, Any]:
        file_path = manifest_item["file_path"]
        manifest_content = manifest_item["content"]
        package_data = manifest_content.get(PACKAGE_SECTION_KEY, {})
        actions_data = manifest_content.get(ACTIONS_SECTION_KEY, [])
        requirements_data = manifest_content.get(REQUIREMENTS_SECTION_KEY, {})
        installer_data = manifest_content.get(INSTALLER_SECTION_KEY, {})

        return {
            "code": str(package_data.get(PACKAGE_CODE_KEY, UNKNOWN_PACKAGE_VALUE)),
            "name": str(package_data.get(PACKAGE_NAME_KEY, UNKNOWN_PACKAGE_VALUE)),
            "version": str(package_data.get(PACKAGE_VERSION_KEY, UNKNOWN_PACKAGE_VALUE)),
            "category": str(package_data.get(PACKAGE_CATEGORY_KEY, UNKNOWN_PACKAGE_VALUE)),
            "edition": str(package_data.get(PACKAGE_EDITION_KEY, DEFAULT_PACKAGE_EDITION)),
            "description": str(package_data.get(PACKAGE_DESCRIPTION_KEY, "")),
            "manifest_path": self._format_path(file_path),
            "requirements": requirements_data,
            "installer": installer_data,
            SERVICE_ADAPTER_RUNTIME_KEY: str(installer_data.get(SERVICE_ADAPTER_RUNTIME_KEY, "simulated")),
            RUNTIME_FAMILY_KEY: str(installer_data.get(RUNTIME_FAMILY_KEY, package_data.get(PACKAGE_CODE_KEY, UNKNOWN_PACKAGE_VALUE))),
            "actions_count": len(actions_data),
            "actions": actions_data,
            "valid": self._is_valid(package_data, actions_data),
        }

    def _is_valid(self, package_data: dict[str, Any], actions_data: list[dict[str, Any]]) -> bool:
        required_package_fields = [
            PACKAGE_CODE_KEY,
            PACKAGE_NAME_KEY,
            PACKAGE_VERSION_KEY,
            PACKAGE_CATEGORY_KEY,
        ]

        has_package_fields = all(package_data.get(field_name) for field_name in required_package_fields)
        has_actions = isinstance(actions_data, list)

        return has_package_fields and has_actions

    def _format_path(self, file_path: Path) -> str:
        return str(file_path).replace("/", "\\")
