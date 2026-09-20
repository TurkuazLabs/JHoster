# 📄 Dosya Yolu: E:\JHoster\app\agent\services\package_download_service.py
# 📌 Amac: Otomatik paket indirme ve kurulum is kurallarini yonetir
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: Package katalog, plan, download, install ve app registry kayitlarini yoneten service katmani
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    PACKAGE_DOWNLOAD_ERROR_DISABLED,
    PACKAGE_DOWNLOAD_ERROR_EXTERNAL_DOWNLOADS_DISABLED,
    PACKAGE_DOWNLOAD_ERROR_NOT_FOUND,
    PACKAGE_DOWNLOAD_ERROR_URL_MISSING,
)
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.package_download_repository import PackageDownloadRepository
from tools.package_download_installer_tool import PackageDownloadInstallerTool


class PackageDownloadService:
    def __init__(
        self,
        package_download_repository: PackageDownloadRepository,
        package_download_installer_tool: PackageDownloadInstallerTool,
        execution_log_repository: ExecutionLogRepository,
        app_registry_repository: AppRegistryRepository,
        allow_external_downloads: bool,
    ) -> None:
        self.package_download_repository = package_download_repository
        self.package_download_installer_tool = package_download_installer_tool
        self.execution_log_repository = execution_log_repository
        self.app_registry_repository = app_registry_repository
        self.allow_external_downloads = allow_external_downloads

    def list_packages(self) -> dict[str, Any]:
        packages = self.package_download_repository.list_packages()
        summaries = [self._to_summary(package) for package in packages]
        return {
            "success": True,
            "count": len(summaries),
            "packages": sorted(summaries, key=lambda item: str(item.get("code", ""))),
        }

    def get_package_detail(self, package_code: str) -> dict[str, Any]:
        package = self.package_download_repository.get_package(package_code)
        if package is None:
            return self._not_found(package_code)
        return {"success": True, "package": package, "plan": self.package_download_installer_tool.build_plan(package)}

    def get_plan(self, package_code: str) -> dict[str, Any]:
        package = self.package_download_repository.get_package(package_code)
        if package is None:
            return self._not_found(package_code)
        return {"success": True, "package": self._to_summary(package), "download_plan": self.package_download_installer_tool.build_plan(package)}

    def download_package(self, package_code: str, dry_run: bool) -> dict[str, Any]:
        package = self.package_download_repository.get_package(package_code)
        if package is None:
            return self._not_found(package_code)

        validation_error = self._validate_download(package)
        if validation_error:
            return {"success": False, "error": validation_error, "component_code": package_code}

        result = self.package_download_installer_tool.download(package, dry_run)
        stored_execution = self.execution_log_repository.append_execution(self._build_execution_payload(package, result, dry_run, "download"))
        return {"success": bool(result.get("success", False)), "execution": stored_execution, "download_result": result}

    def install_package(self, package_code: str, dry_run: bool) -> dict[str, Any]:
        package = self.package_download_repository.get_package(package_code)
        if package is None:
            return self._not_found(package_code)

        if not bool(package.get("enabled", False)):
            return {"success": False, "error": PACKAGE_DOWNLOAD_ERROR_DISABLED, "component_code": package_code}

        result = self.package_download_installer_tool.install(package, dry_run)
        stored_execution = self.execution_log_repository.append_execution(self._build_execution_payload(package, result, dry_run, "install"))
        app_record = self._register_app(package, result, stored_execution, dry_run)
        return {"success": bool(result.get("success", False)), "execution": stored_execution, "install_result": result, "app": app_record}

    def _validate_download(self, package: dict[str, Any]) -> str:
        if not bool(package.get("enabled", False)):
            return PACKAGE_DOWNLOAD_ERROR_DISABLED
        if not str(package.get("source_url", "")).strip():
            return PACKAGE_DOWNLOAD_ERROR_URL_MISSING
        if not self.allow_external_downloads:
            return PACKAGE_DOWNLOAD_ERROR_EXTERNAL_DOWNLOADS_DISABLED
        return ""

    def _build_execution_payload(self, package: dict[str, Any], result: dict[str, Any], dry_run: bool, operation: str) -> dict[str, Any]:
        return {
            "component_code": package.get("code"),
            "component_name": package.get("name"),
            "component_version": package.get("version"),
            "dry_run": dry_run,
            "operation": operation,
            "installer": {"mode": "download_package", "family": package.get("family")},
            "summary": {"package_download": True, "safe_completed": bool(result.get("success", False)) and not dry_run},
            "actions": [result],
            "created_by": "package_download_service",
        }

    def _register_app(self, package: dict[str, Any], result: dict[str, Any], stored_execution: dict[str, Any], dry_run: bool) -> dict[str, Any] | None:
        if dry_run or not result.get("success", False):
            return None
        app_data = {
            "code": package.get("code"),
            "name": package.get("name"),
            "version": package.get("version"),
            "category": package.get("category"),
            "edition": "community",
            "install_path": result.get("install_path"),
            "runtime_adapter": package.get("family", "package"),
            "runtime_family": package.get("family", package.get("code")),
            "last_execution_at": stored_execution.get("created_at", datetime.now(timezone.utc).isoformat()),
        }
        return self.app_registry_repository.upsert_app(app_data)

    def _to_summary(self, package: dict[str, Any]) -> dict[str, Any]:
        plan = self.package_download_installer_tool.build_plan(package)
        return {
            "code": package.get("code"),
            "name": package.get("name"),
            "version": package.get("version"),
            "family": package.get("family"),
            "category": package.get("category"),
            "enabled": bool(package.get("enabled", False)),
            "cache_target": package.get("cache_target"),
            "install_target": package.get("install_target"),
            "cache_exists": plan.get("cache_exists"),
            "source_page": package.get("source_page"),
            "description": package.get("description"),
        }

    def _not_found(self, package_code: str) -> dict[str, Any]:
        return {"success": False, "error": PACKAGE_DOWNLOAD_ERROR_NOT_FOUND, "component_code": package_code}
