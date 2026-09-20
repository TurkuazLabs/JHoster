# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\package_download_installer_tool.py
# 📌 Amac: Indirilen paketleri cache uzerinden dogrulayip hedef bin klasorune kurar
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: Otomatik download, checksum opsiyonel dogrulama ve zip extract install tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import (
    CHECKSUM_ALGORITHM_SHA256,
    DEFAULT_PACKAGE_DOWNLOAD_MAX_BYTES,
    PACKAGE_DOWNLOAD_ERROR_ARCHIVE_MISSING,
    PACKAGE_DOWNLOAD_ERROR_CHECKSUM_MISMATCH,
    PACKAGE_DOWNLOAD_STATUS_DOWNLOADED,
    PACKAGE_DOWNLOAD_STATUS_INSTALLED,
    PACKAGE_DOWNLOAD_STATUS_PLANNED,
    PACKAGE_DOWNLOAD_MESSAGE_DOWNLOADED,
    PACKAGE_DOWNLOAD_MESSAGE_DRY_RUN,
    PACKAGE_DOWNLOAD_MESSAGE_INSTALLED,
)
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.http_download_tool import HttpDownloadTool
from tools.safe_path_tool import SafePathTool


class PackageDownloadInstallerTool:
    def __init__(
        self,
        safe_path_tool: SafePathTool,
        http_download_tool: HttpDownloadTool,
        checksum_tool: ChecksumTool,
        archive_extract_tool: ArchiveExtractTool,
    ) -> None:
        self.safe_path_tool = safe_path_tool
        self.http_download_tool = http_download_tool
        self.checksum_tool = checksum_tool
        self.archive_extract_tool = archive_extract_tool

    def build_plan(self, package: dict[str, Any]) -> dict[str, Any]:
        max_bytes = int(package.get("max_bytes", DEFAULT_PACKAGE_DOWNLOAD_MAX_BYTES))
        cache_target = str(package.get("cache_target", "")).strip()
        install_target = str(package.get("install_target", "")).strip()
        checksum = str(package.get("checksum", "")).strip().lower()
        algorithm = str(package.get("checksum_algorithm", CHECKSUM_ALGORITHM_SHA256)).strip().lower()
        source_url = str(package.get("source_url", "")).strip()

        return {
            "code": package.get("code"),
            "name": package.get("name"),
            "version": package.get("version"),
            "family": package.get("family"),
            "enabled": bool(package.get("enabled", False)),
            "source_url": source_url,
            "source_page": package.get("source_page"),
            "cache_target": cache_target,
            "install_target": install_target,
            "archive_type": str(package.get("archive_type", "zip")).strip().lower(),
            "checksum_algorithm": algorithm,
            "checksum": checksum,
            "checksum_required": bool(package.get("checksum_required", False)),
            "max_bytes": max_bytes,
            "cache_exists": self._exists_inside_root(cache_target),
            "ready_to_download": bool(source_url and cache_target),
            "ready_to_install": bool(cache_target and install_target),
        }

    def download(self, package: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        plan = self.build_plan(package)
        if dry_run:
            return {
                "success": True,
                "status": PACKAGE_DOWNLOAD_STATUS_PLANNED,
                "message": PACKAGE_DOWNLOAD_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        cache_path = self.safe_path_tool.resolve_inside_root(str(plan.get("cache_target", "")))
        download_result = self.http_download_tool.download(
            str(plan.get("source_url", "")),
            cache_path,
            int(plan.get("max_bytes", DEFAULT_PACKAGE_DOWNLOAD_MAX_BYTES)),
        )
        checksum_result = self._verify_if_configured(cache_path, plan)
        if checksum_result and not checksum_result.get("valid", False):
            return {
                "success": False,
                "error": PACKAGE_DOWNLOAD_ERROR_CHECKSUM_MISMATCH,
                "plan": plan,
                "download": download_result,
                "checksum": checksum_result,
            }

        return {
            "success": True,
            "status": PACKAGE_DOWNLOAD_STATUS_DOWNLOADED,
            "message": PACKAGE_DOWNLOAD_MESSAGE_DOWNLOADED,
            "plan": plan,
            "download": download_result,
            "checksum": checksum_result,
        }

    def install(self, package: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        plan = self.build_plan(package)
        if dry_run:
            return {
                "success": True,
                "status": PACKAGE_DOWNLOAD_STATUS_PLANNED,
                "message": PACKAGE_DOWNLOAD_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        archive_path = self.safe_path_tool.resolve_inside_root(str(plan.get("cache_target", "")))
        if not archive_path.exists():
            return {
                "success": False,
                "error": PACKAGE_DOWNLOAD_ERROR_ARCHIVE_MISSING,
                "plan": plan,
            }

        checksum_result = self._verify_if_configured(archive_path, plan)
        if checksum_result and not checksum_result.get("valid", False):
            return {
                "success": False,
                "error": PACKAGE_DOWNLOAD_ERROR_CHECKSUM_MISMATCH,
                "plan": plan,
                "checksum": checksum_result,
            }

        install_path = self.safe_path_tool.resolve_inside_root(str(plan.get("install_target", "")))
        extract_result = self.archive_extract_tool.extract_zip(
            archive_path,
            install_path,
            int(plan.get("max_bytes", DEFAULT_PACKAGE_DOWNLOAD_MAX_BYTES)),
        )
        marker_path = install_path / "jhoster.package"
        marker_path.write_text(str(package.get("code", "unknown")), encoding="utf-8")

        return {
            "success": True,
            "status": PACKAGE_DOWNLOAD_STATUS_INSTALLED,
            "message": PACKAGE_DOWNLOAD_MESSAGE_INSTALLED,
            "plan": plan,
            "checksum": checksum_result,
            "extract": extract_result,
            "install_path": self._format_relative_path(install_path),
        }

    def _verify_if_configured(self, file_path: Path, plan: dict[str, Any]) -> dict[str, Any] | None:
        checksum = str(plan.get("checksum", "")).strip()
        if not checksum:
            return None

        return self.checksum_tool.verify(
            file_path,
            checksum,
            str(plan.get("checksum_algorithm", CHECKSUM_ALGORITHM_SHA256)),
        )

    def _exists_inside_root(self, relative_path: str) -> bool:
        if not relative_path:
            return False
        try:
            return self.safe_path_tool.resolve_inside_root(relative_path).exists()
        except ValueError:
            return False

    def _format_relative_path(self, file_path: Path) -> str:
        try:
            relative_path = file_path.resolve().relative_to(self.safe_path_tool.root_path)
            return str(relative_path).replace("/", "\\")
        except ValueError:
            return str(file_path).replace("/", "\\")
