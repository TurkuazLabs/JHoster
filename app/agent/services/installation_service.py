# 📄 Dosya Yolu: E:\JHoster\app\agent\services\installation_service.py
# 📌 Amac: Component kurulum planini is kurallariyla calistirir veya simule eder
# 📌 Modul - FileType
# Version: 1.3.0
# Aciklama: Manifest executor orchestration, relative install path, runtime adapter ve app registry service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import (
    ACTION_STATUS_BLOCKED,
    ACTION_STATUS_FAILED,
    APPS_DIRECTORY_NAME,
    INSTALLER_SECTION_KEY,
    PATH_SEPARATOR_WINDOWS,
    SERVICE_ADAPTER_RUNTIME_KEY,
)
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.manifest_repository import ManifestRepository
from tools.action_executor_tool import ActionExecutorTool
from tools.manifest_validation_tool import ManifestValidationTool


class InstallationService:
    def __init__(
        self,
        manifest_repository: ManifestRepository,
        manifest_validation_tool: ManifestValidationTool,
        action_executor_tool: ActionExecutorTool,
        execution_log_repository: ExecutionLogRepository,
        app_registry_repository: AppRegistryRepository,
    ) -> None:
        self.manifest_repository = manifest_repository
        self.manifest_validation_tool = manifest_validation_tool
        self.action_executor_tool = action_executor_tool
        self.execution_log_repository = execution_log_repository
        self.app_registry_repository = app_registry_repository

    def execute_component(self, component_code: str, dry_run: bool) -> dict[str, Any]:
        manifest_item = self.manifest_repository.get_manifest_by_code(component_code)

        if manifest_item is None:
            return self._not_found_response(component_code)

        component = self.manifest_validation_tool.normalize(manifest_item)
        actions = component.get("actions", [])
        action_results = self.action_executor_tool.execute_actions(actions, dry_run=dry_run)
        summary = self._build_summary(action_results)
        execution_payload = {
            "component_code": component.get("code"),
            "component_name": component.get("name"),
            "component_version": component.get("version"),
            "dry_run": dry_run,
            "installer": component.get(INSTALLER_SECTION_KEY, {}),
            "summary": summary,
            "actions": action_results,
        }
        stored_execution = self.execution_log_repository.append_execution(execution_payload)
        app_record = self._register_installed_app(component, stored_execution, action_results, dry_run, summary)

        return {
            "success": True,
            "execution": stored_execution,
            "app": app_record,
        }

    def get_history(self) -> dict[str, Any]:
        history_items = self.execution_log_repository.get_history()

        return {
            "success": True,
            "count": len(history_items),
            "history": history_items[-20:],
        }

    def _build_summary(self, action_results: list[dict[str, Any]]) -> dict[str, Any]:
        total_count = len(action_results)
        blocked_count = len([
            action_result
            for action_result in action_results
            if action_result.get("status") == ACTION_STATUS_BLOCKED
        ])
        failed_count = len([
            action_result
            for action_result in action_results
            if action_result.get("status") == ACTION_STATUS_FAILED
        ])

        return {
            "total": total_count,
            "blocked": blocked_count,
            "failed": failed_count,
            "safe_completed": blocked_count == 0 and failed_count == 0,
        }

    def _register_installed_app(
        self,
        component: dict[str, Any],
        stored_execution: dict[str, Any],
        action_results: list[dict[str, Any]],
        dry_run: bool,
        summary: dict[str, Any],
    ) -> dict[str, Any] | None:
        if dry_run or not summary.get("safe_completed"):
            return None

        install_path = self._resolve_install_path(component, action_results)
        app_data = {
            "code": component.get("code"),
            "name": component.get("name"),
            "version": component.get("version"),
            "category": component.get("category"),
            "edition": component.get("edition"),
            "install_path": install_path,
            SERVICE_ADAPTER_RUNTIME_KEY: component.get(SERVICE_ADAPTER_RUNTIME_KEY, "simulated"),
            "last_execution_at": stored_execution.get("created_at"),
        }

        return self.app_registry_repository.upsert_app(app_data)

    def _resolve_install_path(self, component: dict[str, Any], action_results: list[dict[str, Any]]) -> str:
        component_code = str(component.get("code", "")).strip()

        for action_result in action_results:
            extract_data = action_result.get("extract")
            target_value = self._extract_target_value(action_result, extract_data)
            relative_target = self._normalize_apps_relative_path(target_value)

            if relative_target:
                return relative_target

        return self._build_default_install_path(component_code)

    def _extract_target_value(self, action_result: dict[str, Any], extract_data: Any) -> str:
        if isinstance(extract_data, dict) and extract_data.get("target"):
            return str(extract_data.get("target"))

        if action_result.get("target"):
            return str(action_result.get("target"))

        return ""

    def _normalize_apps_relative_path(self, path_value: str) -> str:
        normalized_path = str(path_value or "").strip().replace("/", PATH_SEPARATOR_WINDOWS)

        if not normalized_path:
            return ""

        path_parts = [path_part for path_part in normalized_path.split(PATH_SEPARATOR_WINDOWS) if path_part]
        lowered_parts = [path_part.lower() for path_part in path_parts]

        if APPS_DIRECTORY_NAME in lowered_parts:
            apps_index = lowered_parts.index(APPS_DIRECTORY_NAME)
            return PATH_SEPARATOR_WINDOWS.join(path_parts[apps_index:])

        return ""

    def _build_default_install_path(self, component_code: str) -> str:
        return f"{APPS_DIRECTORY_NAME}{PATH_SEPARATOR_WINDOWS}{component_code}"

    def _not_found_response(self, component_code: str) -> dict[str, Any]:
        return {
            "success": False,
            "error": "component_not_found",
            "component_code": component_code,
        }
