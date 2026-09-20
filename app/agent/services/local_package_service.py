# 📄 Dosya Yolu: E:\JHoster\app\agent\services\local_package_service.py
# 📌 Amac: Local package kurulum is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Local package liste, detay, plan, kurulum ve app registry ve runtime family service katmani
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    INSTALLER_MODE_KEY,
    INSTALLER_MODE_LOCAL_PACKAGE,
    LOCAL_PACKAGE_ERROR_NOT_FOUND,
    LOCAL_PACKAGE_ERROR_UNSUPPORTED_MODE,
    PACKAGE_CATEGORY_KEY,
    SERVICE_ADAPTER_RUNTIME_KEY,
    RUNTIME_FAMILY_KEY,
)
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.local_package_repository import LocalPackageRepository
from tools.local_package_installer_tool import LocalPackageInstallerTool
from tools.manifest_validation_tool import ManifestValidationTool


class LocalPackageService:
    def __init__(
        self,
        local_package_repository: LocalPackageRepository,
        manifest_validation_tool: ManifestValidationTool,
        local_package_installer_tool: LocalPackageInstallerTool,
        execution_log_repository: ExecutionLogRepository,
        app_registry_repository: AppRegistryRepository,
    ) -> None:
        self.local_package_repository = local_package_repository
        self.manifest_validation_tool = manifest_validation_tool
        self.local_package_installer_tool = local_package_installer_tool
        self.execution_log_repository = execution_log_repository
        self.app_registry_repository = app_registry_repository

    def list_local_packages(self) -> dict[str, Any]:
        components = [
            self.manifest_validation_tool.normalize(manifest_item)
            for manifest_item in self.local_package_repository.get_all_local_package_manifests()
        ]
        sorted_components = sorted(components, key=lambda component: str(component.get("code", "")))

        return {
            "success": True,
            "count": len(sorted_components),
            "local_packages": [self._to_summary(component) for component in sorted_components],
        }

    def get_local_package_detail(self, component_code: str) -> dict[str, Any]:
        component = self._find_component(component_code)
        if component is None:
            return self._not_found_response(component_code)

        return {
            "success": True,
            "local_package": component,
        }

    def get_local_package_plan(self, component_code: str) -> dict[str, Any]:
        component = self._find_component(component_code)
        if component is None:
            return self._not_found_response(component_code)

        return {
            "success": True,
            "component": self._to_summary(component),
            "installer": component.get("installer", {}),
            "local_package_plan": self.local_package_installer_tool.build_plan(component),
        }

    def install_local_package(self, component_code: str, dry_run: bool) -> dict[str, Any]:
        component = self._find_component(component_code)
        if component is None:
            return self._not_found_response(component_code)

        mode_error = self._validate_local_package_mode(component)
        if mode_error:
            return {
                "success": False,
                "error": mode_error,
                "component_code": component_code,
            }

        install_result = self.local_package_installer_tool.install(component, dry_run)
        execution_payload = self._build_execution_payload(component, install_result, dry_run)
        stored_execution = self.execution_log_repository.append_execution(execution_payload)
        app_record = self._register_app(component, install_result, stored_execution, dry_run)

        return {
            "success": bool(install_result.get("success", False)),
            "execution": stored_execution,
            "install_result": install_result,
            "app": app_record,
        }

    def _find_component(self, component_code: str) -> dict[str, Any] | None:
        manifest_item = self.local_package_repository.get_local_package_manifest_by_code(component_code)
        if manifest_item is None:
            return None

        return self.manifest_validation_tool.normalize(manifest_item)

    def _validate_local_package_mode(self, component: dict[str, Any]) -> str:
        installer_data = component.get("installer", {})
        if str(installer_data.get(INSTALLER_MODE_KEY, "")).strip() != INSTALLER_MODE_LOCAL_PACKAGE:
            return LOCAL_PACKAGE_ERROR_UNSUPPORTED_MODE

        return ""

    def _build_execution_payload(
        self,
        component: dict[str, Any],
        install_result: dict[str, Any],
        dry_run: bool,
    ) -> dict[str, Any]:
        return {
            "component_code": component.get("code"),
            "component_name": component.get("name"),
            "component_version": component.get("version"),
            "dry_run": dry_run,
            "installer": component.get("installer", {}),
            "summary": {
                "local_package": True,
                "safe_completed": bool(install_result.get("success", False)) and not dry_run,
            },
            "actions": [install_result],
            "created_by": "local_package_service",
        }

    def _register_app(
        self,
        component: dict[str, Any],
        install_result: dict[str, Any],
        stored_execution: dict[str, Any],
        dry_run: bool,
    ) -> dict[str, Any] | None:
        if dry_run or not install_result.get("success", False):
            return None

        app_data = {
            "code": component.get("code"),
            "name": component.get("name"),
            "version": component.get("version"),
            "category": component.get(PACKAGE_CATEGORY_KEY),
            "edition": component.get("edition"),
            "install_path": install_result.get("install_path"),
            SERVICE_ADAPTER_RUNTIME_KEY: component.get(SERVICE_ADAPTER_RUNTIME_KEY, "simulated"),
            RUNTIME_FAMILY_KEY: component.get(RUNTIME_FAMILY_KEY, component.get("code")),
            "last_execution_at": stored_execution.get("created_at", datetime.now(timezone.utc).isoformat()),
        }

        return self.app_registry_repository.upsert_app(app_data)

    def _to_summary(self, component: dict[str, Any]) -> dict[str, Any]:
        return {
            "code": component.get("code"),
            "name": component.get("name"),
            "version": component.get("version"),
            "category": component.get("category"),
            "edition": component.get("edition"),
            "description": component.get("description"),
            "runtime_adapter": component.get(SERVICE_ADAPTER_RUNTIME_KEY),
            "runtime_family": component.get(RUNTIME_FAMILY_KEY),
            "valid": component.get("valid"),
        }

    def _not_found_response(self, component_code: str) -> dict[str, Any]:
        return {
            "success": False,
            "error": LOCAL_PACKAGE_ERROR_NOT_FOUND,
            "component_code": component_code,
        }
