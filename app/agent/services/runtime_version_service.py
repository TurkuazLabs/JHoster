# 📄 Dosya Yolu: E:\JHoster\app\agent\services\runtime_version_service.py
# 📌 Amac: Kurulu runtime ve portable servis version listeleme, aktif version secimi ve profil senkronizasyonunu yonetir
# 📌 Modul - FileType
# Version: 2.0.0
# Aciklama: App registry, portable bin scan, active version, latest activation ve process profile sync is kurallarini uygular
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    RUNTIME_FAMILY_KEY,
    RUNTIME_VERSION_ERROR_APP_NOT_FOUND,
    RUNTIME_VERSION_ERROR_FAMILY_NOT_FOUND,
    RUNTIME_VERSION_MESSAGE_ACTIVATED,
    RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATE_DRY_RUN,
    RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATED,
    RUNTIME_VERSION_MESSAGE_PORTABLE_SCAN_READY,
    RUNTIME_VERSION_ERROR_PORTABLE_FAMILY_NOT_FOUND,
    RUNTIME_VERSION_ERROR_PORTABLE_FOLDER_NOT_FOUND,
    RUNTIME_VERSION_MESSAGE_DRY_RUN,
    RUNTIME_VERSION_STATUS_ACTIVE,
    RUNTIME_VERSION_STATUS_INACTIVE,
    SERVICE_ADAPTER_MODE_SIMULATED,
    SERVICE_ADAPTER_RUNTIME_KEY,
)
from repositories.app_registry_repository import AppRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from tools.portable_version_scanner_tool import PortableVersionScannerTool


class RuntimeVersionService:
    STATUS_PLANNED = "planned"
    MESSAGE_PORTABLE_SUMMARY_READY = "portable version summary ready"
    MESSAGE_PORTABLE_DEFINITIONS_READY = "portable family definitions ready"
    MESSAGE_PORTABLE_LATEST_NOT_FOUND = "portable latest version not found"
    SYNC_REASON_CREATED_BASE_PROFILE = "base_process_profile_created"
    SYNC_REASON_UPDATED_BASE_PROFILE = "base_process_profile_updated"
    APP_STATUS_INSTALLED = "installed"

    def __init__(
        self,
        app_registry_repository: AppRegistryRepository,
        runtime_version_repository: RuntimeVersionRepository,
    ) -> None:
        self.app_registry_repository = app_registry_repository
        self.runtime_version_repository = runtime_version_repository
        self.portable_version_scanner_tool = PortableVersionScannerTool(app_registry_repository.root_path)

    def list_runtime_versions(self) -> dict[str, Any]:
        grouped_versions = self._group_installed_apps()
        families = [
            self._build_family_payload(family, versions)
            for family, versions in sorted(grouped_versions.items())
        ]

        return {
            "success": True,
            "count": len(families),
            "families": families,
        }

    def get_runtime_family(self, family: str) -> dict[str, Any]:
        grouped_versions = self._group_installed_apps()
        normalized_family = self._normalize_family(family)

        if normalized_family not in grouped_versions:
            return {
                "success": False,
                "error": RUNTIME_VERSION_ERROR_FAMILY_NOT_FOUND,
                "family": normalized_family,
            }

        return {
            "success": True,
            "family": self._build_family_payload(normalized_family, grouped_versions[normalized_family]),
        }

    def list_active_versions(self) -> dict[str, Any]:
        active_versions = self.runtime_version_repository.list_active_versions()
        return {
            "success": True,
            "count": len(active_versions),
            "active_versions": active_versions,
        }

    def get_active_version(self, family: str) -> dict[str, Any]:
        normalized_family = self._normalize_family(family)
        active_version = self.runtime_version_repository.get_active_version(normalized_family)

        return {
            "success": True,
            "family": normalized_family,
            "status": RUNTIME_VERSION_STATUS_ACTIVE if active_version is not None else RUNTIME_VERSION_STATUS_INACTIVE,
            "active": active_version,
        }

    def list_portable_family_definitions(self) -> dict[str, Any]:
        definition_result = self.portable_version_scanner_tool.list_family_definitions()
        return {
            **definition_result,
            "message": self.MESSAGE_PORTABLE_DEFINITIONS_READY,
        }

    def scan_portable_versions(self) -> dict[str, Any]:
        scan_result = self.portable_version_scanner_tool.scan_all()
        return {
            **scan_result,
            "message": RUNTIME_VERSION_MESSAGE_PORTABLE_SCAN_READY,
        }

    def scan_portable_family(self, family: str) -> dict[str, Any]:
        scan_result = self.portable_version_scanner_tool.scan_family(family)
        if not bool(scan_result.get("success", False)):
            return {
                **scan_result,
                "message": RUNTIME_VERSION_ERROR_PORTABLE_FAMILY_NOT_FOUND,
            }

        return {
            **self._merge_active_into_scan_family(scan_result),
            "message": RUNTIME_VERSION_MESSAGE_PORTABLE_SCAN_READY,
        }

    def portable_summary(self) -> dict[str, Any]:
        scan_result = self.portable_version_scanner_tool.scan_all()
        families = scan_result.get("families", [])
        if not isinstance(families, list):
            families = []

        enriched_families = [self._merge_active_into_scan_family(family_result) for family_result in families]
        detected_count = sum(int(family.get("count", 0)) for family in enriched_families)
        active_count = sum(1 for family in enriched_families if bool(family.get("active")))

        return {
            "success": True,
            "source": scan_result.get("source"),
            "message": self.MESSAGE_PORTABLE_SUMMARY_READY,
            "count": detected_count,
            "family_count": len(enriched_families),
            "active_count": active_count,
            "families": enriched_families,
        }

    def activate_latest_portable_version(self, family: str, dry_run: bool) -> dict[str, Any]:
        normalized_family = self._normalize_family(family)
        portable_version = self.portable_version_scanner_tool.get_latest_version(normalized_family)
        if portable_version is None:
            return {
                "success": False,
                "error": self.MESSAGE_PORTABLE_LATEST_NOT_FOUND,
                "family": normalized_family,
            }

        return self._activate_portable_version_payload(portable_version, dry_run)

    def activate_portable_version(self, family: str, folder_name: str, dry_run: bool) -> dict[str, Any]:
        normalized_family = self._normalize_family(family)
        portable_version = self.portable_version_scanner_tool.get_version_by_folder(normalized_family, folder_name)
        if portable_version is None:
            return {
                "success": False,
                "error": RUNTIME_VERSION_ERROR_PORTABLE_FOLDER_NOT_FOUND,
                "family": normalized_family,
                "folder_name": str(folder_name).strip(),
            }

        return self._activate_portable_version_payload(portable_version, dry_run)

    def activate_runtime_version(self, component_code: str, dry_run: bool) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return {
                "success": False,
                "error": RUNTIME_VERSION_ERROR_APP_NOT_FOUND,
                "component_code": component_code,
            }

        family = self._resolve_runtime_family(app_item)
        activation_payload = {
            "family": family,
            "component_code": app_item.get("code"),
            "name": app_item.get("name"),
            "version": app_item.get("version"),
            "install_path": app_item.get("install_path"),
            "runtime_adapter": app_item.get(SERVICE_ADAPTER_RUNTIME_KEY, SERVICE_ADAPTER_MODE_SIMULATED),
            "planned_at": self._now(),
        }

        if dry_run:
            return {
                "success": True,
                "status": self.STATUS_PLANNED,
                "message": RUNTIME_VERSION_MESSAGE_DRY_RUN,
                "activation": activation_payload,
            }

        stored_activation = self.runtime_version_repository.set_active_version(activation_payload)

        return {
            "success": True,
            "family": stored_activation.get("family"),
            "component_code": stored_activation.get("component_code"),
            "version": stored_activation.get("version"),
            "status": RUNTIME_VERSION_STATUS_ACTIVE,
            "message": RUNTIME_VERSION_MESSAGE_ACTIVATED,
            "activation": stored_activation,
        }

    def _activate_portable_version_payload(self, portable_version: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        activation_payload = self._build_portable_activation_payload(portable_version)

        if dry_run:
            return {
                "success": True,
                "status": self.STATUS_PLANNED,
                "message": RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATE_DRY_RUN,
                "family": activation_payload.get("family"),
                "folder_name": activation_payload.get("folder_name"),
                "component_code": activation_payload.get("component_code"),
                "version": activation_payload.get("version"),
                "activation": activation_payload,
            }

        stored_activation = self.runtime_version_repository.set_active_version(activation_payload)
        synced_process_profile = self._sync_process_profile_from_portable_version(portable_version)

        return {
            "success": True,
            "status": RUNTIME_VERSION_STATUS_ACTIVE,
            "message": RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATED,
            "family": stored_activation.get("family"),
            "folder_name": stored_activation.get("folder_name"),
            "component_code": stored_activation.get("component_code"),
            "version": stored_activation.get("version"),
            "activation": stored_activation,
            "synced_process_profile": synced_process_profile,
        }

    def _build_portable_activation_payload(self, portable_version: dict[str, Any]) -> dict[str, Any]:
        return {
            "family": portable_version.get("family"),
            "component_code": portable_version.get("code"),
            "name": portable_version.get("name"),
            "version": portable_version.get("version"),
            "install_path": portable_version.get("install_path"),
            "runtime_adapter": portable_version.get("runtime_adapter"),
            "source": portable_version.get("source"),
            "folder_name": portable_version.get("folder_name"),
            "executable_path": portable_version.get("executable_path"),
            "executable_exists": portable_version.get("executable_exists"),
            "metadata": portable_version.get("metadata"),
            "planned_at": self._now(),
        }

    def _merge_active_into_scan_family(self, family_result: dict[str, Any]) -> dict[str, Any]:
        family = self._normalize_family(str(family_result.get("family", "")))
        active_version = self.runtime_version_repository.get_active_version(family)
        active_folder_name = str(active_version.get("folder_name", "")) if active_version else ""
        active_component_code = str(active_version.get("component_code", "")) if active_version else ""

        versions = family_result.get("versions", [])
        if not isinstance(versions, list):
            versions = []

        version_items = []
        for version_item in versions:
            is_active = bool(
                active_folder_name and str(version_item.get("folder_name", "")) == active_folder_name
            ) or bool(
                active_component_code and str(version_item.get("code", "")) == active_component_code
            )
            version_items.append({
                **version_item,
                "active": is_active,
                "status": RUNTIME_VERSION_STATUS_ACTIVE if is_active else RUNTIME_VERSION_STATUS_INACTIVE,
            })

        return {
            **family_result,
            "active": active_version,
            "active_folder_name": active_folder_name,
            "active_component_code": active_component_code,
            "versions": version_items,
        }

    def _sync_process_profile_from_portable_version(self, portable_version: dict[str, Any]) -> dict[str, Any]:
        family = self._normalize_family(str(portable_version.get("family", "")))
        base_app_item = self.app_registry_repository.get_app(family)
        created = False
        if base_app_item is None:
            base_app_item = self._build_base_app_item_from_portable_version(portable_version)
            created = True

        process_profile = portable_version.get("process_profile", {})
        if not isinstance(process_profile, dict):
            process_profile = {}

        base_real_process = base_app_item.get("real_process", {})
        if not isinstance(base_real_process, dict):
            base_real_process = {}

        next_real_process = {
            **base_real_process,
            "enabled": bool(base_real_process.get("enabled", False)),
            "process_name": process_profile.get("process_name", base_real_process.get("process_name", "")),
            "working_dir": process_profile.get("working_dir", base_real_process.get("working_dir", "")),
            "executable_candidates": process_profile.get("executable_candidates", base_real_process.get("executable_candidates", [])),
            "start_args": process_profile.get("start_args", base_real_process.get("start_args", [])),
            "stop_args": process_profile.get("stop_args", base_real_process.get("stop_args", [])),
            "status_args": process_profile.get("status_args", base_real_process.get("status_args", [])),
        }

        next_app_item = {
            **base_app_item,
            "code": family,
            "name": portable_version.get("display_name", base_app_item.get("name", family)),
            "version": portable_version.get("version"),
            "category": portable_version.get("category", base_app_item.get("category")),
            "install_path": portable_version.get("install_path"),
            "runtime_adapter": portable_version.get("runtime_adapter", base_app_item.get("runtime_adapter")),
            "runtime_family": portable_version.get("family", base_app_item.get("runtime_family")),
            "portable_folder_name": portable_version.get("folder_name"),
            "portable_source": portable_version.get("source"),
            "portable_metadata": portable_version.get("metadata"),
            "real_process": next_real_process,
        }
        stored_app_item = self.app_registry_repository.upsert_app(next_app_item)

        return {
            "success": True,
            "synced": True,
            "reason": self.SYNC_REASON_CREATED_BASE_PROFILE if created else self.SYNC_REASON_UPDATED_BASE_PROFILE,
            "code": stored_app_item.get("code"),
            "version": stored_app_item.get("version"),
            "install_path": stored_app_item.get("install_path"),
            "real_process_enabled": stored_app_item.get("real_process", {}).get("enabled", False),
        }

    def _build_base_app_item_from_portable_version(self, portable_version: dict[str, Any]) -> dict[str, Any]:
        family = self._normalize_family(str(portable_version.get("family", "")))
        process_profile = portable_version.get("process_profile", {})
        if not isinstance(process_profile, dict):
            process_profile = {}

        return {
            "code": family,
            "name": portable_version.get("display_name", family),
            "version": portable_version.get("version"),
            "category": portable_version.get("category", "runtime"),
            "runtime_adapter": portable_version.get("runtime_adapter", SERVICE_ADAPTER_MODE_SIMULATED),
            "runtime_family": family,
            "install_path": portable_version.get("install_path"),
            "status": self.APP_STATUS_INSTALLED,
            "description": "Portable version base profile generated by JHoster scanner.",
            "real_process": {
                "enabled": False,
                "process_name": process_profile.get("process_name", ""),
                "working_dir": process_profile.get("working_dir", ""),
                "executable_candidates": process_profile.get("executable_candidates", []),
                "start_args": process_profile.get("start_args", []),
                "stop_args": process_profile.get("stop_args", []),
                "status_args": process_profile.get("status_args", []),
            },
        }

    def _group_installed_apps(self) -> dict[str, list[dict[str, Any]]]:
        grouped_versions: dict[str, list[dict[str, Any]]] = {}

        for app_item in self.app_registry_repository.list_apps():
            family = self._resolve_runtime_family(app_item)
            grouped_versions.setdefault(family, []).append(app_item)

        for versions in grouped_versions.values():
            versions.sort(key=lambda item: self._version_sort_key(str(item.get("version", ""))), reverse=True)

        return grouped_versions

    def _build_family_payload(self, family: str, versions: list[dict[str, Any]]) -> dict[str, Any]:
        active_version = self.runtime_version_repository.get_active_version(family)
        active_component_code = ""
        if active_version is not None:
            active_component_code = str(active_version.get("component_code", ""))

        version_items = [
            self._build_version_payload(app_item, active_component_code)
            for app_item in versions
        ]

        return {
            "family": family,
            "active": active_version,
            "count": len(version_items),
            "versions": version_items,
        }

    def _build_version_payload(self, app_item: dict[str, Any], active_component_code: str) -> dict[str, Any]:
        component_code = str(app_item.get("code", ""))
        is_active = bool(component_code and component_code == active_component_code)

        return {
            "code": app_item.get("code"),
            "name": app_item.get("name"),
            "version": app_item.get("version"),
            "category": app_item.get("category"),
            "edition": app_item.get("edition"),
            "install_path": app_item.get("install_path"),
            "runtime_adapter": app_item.get(SERVICE_ADAPTER_RUNTIME_KEY, SERVICE_ADAPTER_MODE_SIMULATED),
            "status": RUNTIME_VERSION_STATUS_ACTIVE if is_active else RUNTIME_VERSION_STATUS_INACTIVE,
            "active": is_active,
        }

    def _resolve_runtime_family(self, app_item: dict[str, Any]) -> str:
        explicit_family = self._normalize_family(str(app_item.get(RUNTIME_FAMILY_KEY, "")))
        if explicit_family:
            return explicit_family

        category = str(app_item.get("category", "")).strip()
        adapter = str(app_item.get(SERVICE_ADAPTER_RUNTIME_KEY, SERVICE_ADAPTER_MODE_SIMULATED)).strip()
        if category == "runtime" and adapter and adapter != SERVICE_ADAPTER_MODE_SIMULATED:
            return adapter

        return self._normalize_family(str(app_item.get("code", "unknown")))

    def _normalize_family(self, family: str) -> str:
        definition = self.portable_version_scanner_tool.resolve_definition(family)
        if definition is not None:
            return definition.family
        return str(family or "").strip().lower()

    def _version_sort_key(self, version: str) -> list[int]:
        parts = []
        for part in str(version or "").split("."):
            if part.isdigit():
                parts.append(int(part))
        while len(parts) < 4:
            parts.append(0)
        return parts[:4]

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
