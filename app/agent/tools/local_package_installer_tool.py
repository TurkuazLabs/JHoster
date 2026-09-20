# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\local_package_installer_tool.py
# 📌 Amac: Cache icindeki dogrulanmis local package arsivlerini guvenli kurar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Local package plan, checksum dogrulama ve safe extract tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import (
    CHECKSUM_ALGORITHM_SHA256,
    DEFAULT_LOCAL_PACKAGE_MAX_BYTES,
    INSTALLER_PACKAGE_ALGORITHM_KEY,
    INSTALLER_PACKAGE_CHECKSUM_KEY,
    INSTALLER_PACKAGE_MAX_BYTES_KEY,
    INSTALLER_PACKAGE_SOURCE_KEY,
    INSTALLER_PACKAGE_TARGET_KEY,
    LOCAL_PACKAGE_ERROR_CHECKSUM_MISMATCH,
    LOCAL_PACKAGE_ERROR_CHECKSUM_MISSING,
    LOCAL_PACKAGE_ERROR_SOURCE_MISSING,
    LOCAL_PACKAGE_ERROR_TARGET_MISSING,
    LOCAL_PACKAGE_MESSAGE_DRY_RUN,
    LOCAL_PACKAGE_MESSAGE_INSTALLED,
    LOCAL_PACKAGE_STATUS_INSTALLED,
    LOCAL_PACKAGE_STATUS_PLANNED,
)
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.safe_path_tool import SafePathTool


class LocalPackageInstallerTool:
    def __init__(
        self,
        safe_path_tool: SafePathTool,
        checksum_tool: ChecksumTool,
        archive_extract_tool: ArchiveExtractTool,
    ) -> None:
        self.safe_path_tool = safe_path_tool
        self.checksum_tool = checksum_tool
        self.archive_extract_tool = archive_extract_tool

    def build_plan(self, component: dict[str, Any]) -> dict[str, Any]:
        installer_data = component.get("installer", {})
        source_value = str(installer_data.get(INSTALLER_PACKAGE_SOURCE_KEY, "")).strip()
        target_value = str(installer_data.get(INSTALLER_PACKAGE_TARGET_KEY, "")).strip()
        checksum_value = str(installer_data.get(INSTALLER_PACKAGE_CHECKSUM_KEY, "")).strip()
        algorithm_value = str(installer_data.get(INSTALLER_PACKAGE_ALGORITHM_KEY, CHECKSUM_ALGORITHM_SHA256)).strip().lower()
        max_bytes_value = int(installer_data.get(INSTALLER_PACKAGE_MAX_BYTES_KEY, DEFAULT_LOCAL_PACKAGE_MAX_BYTES))

        return {
            "source": source_value,
            "target": target_value,
            "checksum": checksum_value,
            "algorithm": algorithm_value,
            "max_bytes": max_bytes_value,
            "ready": bool(source_value and target_value and checksum_value),
        }

    def install(self, component: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        plan = self.build_plan(component)
        validation_error = self._validate_plan(plan)

        if validation_error:
            return {
                "success": False,
                "error": validation_error,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": LOCAL_PACKAGE_STATUS_PLANNED,
                "message": LOCAL_PACKAGE_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        source_path = self.safe_path_tool.resolve_inside_root(plan.get("source"))
        target_path = self.safe_path_tool.resolve_inside_root(plan.get("target"))
        verification_result = self.checksum_tool.verify(
            source_path,
            str(plan.get("checksum")),
            str(plan.get("algorithm")),
        )

        if not verification_result.get("valid", False):
            return {
                "success": False,
                "error": LOCAL_PACKAGE_ERROR_CHECKSUM_MISMATCH,
                "plan": plan,
                "checksum": verification_result,
            }

        extract_result = self.archive_extract_tool.extract_zip(
            source_path,
            target_path,
            int(plan.get("max_bytes", DEFAULT_LOCAL_PACKAGE_MAX_BYTES)),
        )

        return {
            "success": True,
            "status": LOCAL_PACKAGE_STATUS_INSTALLED,
            "message": LOCAL_PACKAGE_MESSAGE_INSTALLED,
            "plan": plan,
            "checksum": verification_result,
            "extract": extract_result,
            "install_path": self._format_relative_path(target_path),
        }

    def _validate_plan(self, plan: dict[str, Any]) -> str:
        if not plan.get("source"):
            return LOCAL_PACKAGE_ERROR_SOURCE_MISSING

        if not plan.get("target"):
            return LOCAL_PACKAGE_ERROR_TARGET_MISSING

        if not plan.get("checksum"):
            return LOCAL_PACKAGE_ERROR_CHECKSUM_MISSING

        return ""

    def _format_relative_path(self, file_path: Path) -> str:
        try:
            relative_path = file_path.resolve().relative_to(self.safe_path_tool.root_path)
            return str(relative_path).replace("/", "\\")
        except ValueError:
            return str(file_path).replace("/", "\\")
