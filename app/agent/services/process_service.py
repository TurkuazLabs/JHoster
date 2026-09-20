# 📄 Dosya Yolu: E:\JHoster\app\agent\services\process_service.py
# 📌 Amac: Kurulu app process durumlarini, aktif web server modunu ve real process profilini is kurallariyla yonetir
# 📌 Modul - FileType
# Version: 1.7.0
# Aciklama: Start, stop, restart, preflight, inspect, real profile, aktif Apache/Nginx secimi, port guard, status, adapter secimi, verification sonucu ve process listeleme service katmani
# Bagimli Oldugu Katman: Service

from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config.constants import (
    PROCESS_MESSAGE_ALREADY_RUNNING,
    PROCESS_MESSAGE_ALREADY_STOPPED,
    PROCESS_MESSAGE_APP_NOT_FOUND,
    PROCESS_MESSAGE_DRY_RUN,
    PROCESS_MESSAGE_PREFLIGHT_READY,
    PROCESS_MESSAGE_INSPECTION_READY,
    PROCESS_MESSAGE_REAL_PROFILE_DRY_RUN,
    PROCESS_MESSAGE_REAL_PROFILE_INVALID_PATH,
    PROCESS_MESSAGE_REAL_PROFILE_PLANNED,
    PROCESS_MESSAGE_REAL_PROFILE_READY,
    PROCESS_MESSAGE_REAL_PROFILE_UPDATED,
    PROCESS_MESSAGE_RESTARTED,
    PROCESS_MESSAGE_STARTED,
    PROCESS_MESSAGE_STATUS_READY,
    PROCESS_MESSAGE_STOPPED,
    PROCESS_MESSAGE_WEB_SERVER_PROFILE_MISMATCH,
    PROCESS_MESSAGE_WEB_SERVER_SWITCH_STOP_FAILED,
    WEB_SERVER_ACTIVE_PROFILE_KEY,
    WEB_SERVER_PORT_GUARD_ALLOWED_KEY,
    WEB_SERVER_PORT_GUARD_MESSAGE_KEY,
    WEB_SERVER_PROFILE_DEFAULT,
    WEB_SERVER_PROFILE_SELECTED_FROM_PROCESS,
    WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY,
    WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
    PROCESS_MODE_SIMULATED,
    PROCESS_OPERATION_PREFLIGHT,
    PROCESS_OPERATION_INSPECT,
    PROCESS_OPERATION_REAL_PROFILE,
    PROCESS_OPERATION_REAL_PROFILE_APPLY,
    PROCESS_OPERATION_REAL_PROFILE_PLAN,
    PROCESS_OPERATION_RESTART,
    PROCESS_OPERATION_START,
    PROCESS_OPERATION_STATUS,
    PROCESS_OPERATION_STOP,
    PROCESS_STATUS_RUNNING,
    PROCESS_STATUS_STOPPED,
    SERVICE_CODE_APACHE,
    SERVICE_CODE_NGINX,
    WEB_SERVER_FRONTEND_CODES,
)
from repositories.app_registry_repository import AppRegistryRepository
from repositories.process_state_repository import ProcessStateRepository
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from tools.process_guard_tool import ProcessGuardTool
from tools.service_adapters.adapter_registry import ServiceAdapterRegistryTool
from tools.web_server_port_guard_tool import WebServerPortGuardTool


class ProcessService:
    def __init__(
        self,
        app_registry_repository: AppRegistryRepository,
        process_state_repository: ProcessStateRepository,
        process_guard_tool: ProcessGuardTool,
        service_adapter_registry_tool: ServiceAdapterRegistryTool,
        web_server_port_guard_tool: WebServerPortGuardTool,
        web_server_profile_registry_repository: WebServerProfileRegistryRepository,
    ) -> None:
        self.app_registry_repository = app_registry_repository
        self.process_state_repository = process_state_repository
        self.process_guard_tool = process_guard_tool
        self.service_adapter_registry_tool = service_adapter_registry_tool
        self.web_server_port_guard_tool = web_server_port_guard_tool
        self.web_server_profile_registry_repository = web_server_profile_registry_repository

    def list_processes(self) -> dict[str, Any]:
        apps = self.app_registry_repository.list_apps()
        processes = [self._build_process_view(app_item) for app_item in apps]

        return {
            "success": True,
            "count": len(processes),
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "processes": processes,
        }

    def get_process_status(self, component_code: str, prefer_real: bool = False) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_STATUS)

        process_item = self.process_state_repository.get_process(component_code)
        runtime_context = self.process_guard_tool.build_runtime_context(app_item)
        adapter = self.service_adapter_registry_tool.resolve_adapter(app_item, prefer_real=prefer_real)
        adapter_result = adapter.status(app_item, process_item, runtime_context)

        return {
            "success": bool(adapter_result.get("success", True)),
            "operation": PROCESS_OPERATION_STATUS,
            "message": PROCESS_MESSAGE_STATUS_READY,
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "process": self._build_process_view(app_item, adapter_result=adapter_result),
            "adapter_result": adapter_result,
        }

    def inspect_process(self, component_code: str) -> dict[str, Any]:
        result = self.get_process_status(component_code, prefer_real=True)
        result["operation"] = PROCESS_OPERATION_INSPECT
        result["message"] = PROCESS_MESSAGE_INSPECTION_READY
        return result

    def preflight_process(self, component_code: str) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_PREFLIGHT)

        runtime_context = self.process_guard_tool.build_runtime_context(app_item)
        adapter = self.service_adapter_registry_tool.resolve_adapter(app_item, prefer_real=True)
        adapter_result = adapter.preflight(app_item, runtime_context)

        return {
            "success": bool(adapter_result.get("success", True)),
            "operation": PROCESS_OPERATION_PREFLIGHT,
            "message": PROCESS_MESSAGE_PREFLIGHT_READY,
            "process": self._build_process_view(app_item, adapter_result=adapter_result),
            "runtime_context": runtime_context,
            "adapter_result": adapter_result,
        }

    def get_real_profile(self, component_code: str) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_REAL_PROFILE)

        runtime_context = self.process_guard_tool.build_runtime_context(app_item)
        return {
            "success": True,
            "operation": PROCESS_OPERATION_REAL_PROFILE,
            "message": PROCESS_MESSAGE_REAL_PROFILE_READY,
            "profile": self._build_real_profile_view(app_item, runtime_context),
            "runtime_context": runtime_context,
        }

    def plan_real_profile(
        self,
        component_code: str,
        install_path: str = "",
        enabled: bool | None = None,
    ) -> dict[str, Any]:
        return self._real_profile_update_response(
            component_code=component_code,
            install_path=install_path,
            enabled=enabled,
            dry_run=True,
        )

    def apply_real_profile(
        self,
        component_code: str,
        install_path: str = "",
        enabled: bool | None = None,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        return self._real_profile_update_response(
            component_code=component_code,
            install_path=install_path,
            enabled=enabled,
            dry_run=dry_run,
        )

    def start_process(self, component_code: str, dry_run: bool, allow_real_execution: bool = False) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_START)

        normalized_code = self._normalize_web_code(component_code)
        current_status = self.process_state_repository.get_status(component_code)
        process_item = self.process_state_repository.get_process(component_code)
        runtime_context = self.process_guard_tool.build_runtime_context(app_item)

        if self._is_web_frontend(normalized_code) and normalized_code != self._get_active_web_server_code():
            return self._web_server_profile_mismatch_response(
                normalized_code,
                PROCESS_OPERATION_START,
                current_status,
                runtime_context,
            )

        switch_result = self._stop_other_web_server_before_start(normalized_code, dry_run, allow_real_execution)
        if switch_result is not None and not switch_result.get("success", False):
            return {
                "success": False,
                "operation": PROCESS_OPERATION_START,
                "message": PROCESS_MESSAGE_WEB_SERVER_SWITCH_STOP_FAILED,
                WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
                WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
                "switch_result": switch_result,
            }

        port_guard_result = self.web_server_port_guard_tool.validate_start(
            component_code,
            app_item,
            self.app_registry_repository.list_apps(),
            self.process_state_repository.list_processes(),
        )

        if not port_guard_result.get(WEB_SERVER_PORT_GUARD_ALLOWED_KEY, False):
            return self._port_guard_blocked_response(
                component_code,
                PROCESS_OPERATION_START,
                current_status,
                runtime_context,
                port_guard_result,
            )

        adapter = self.service_adapter_registry_tool.resolve_adapter(app_item, prefer_real=allow_real_execution)
        adapter_result = adapter.start(app_item, process_item, dry_run, allow_real_execution, runtime_context)

        if dry_run:
            return self._dry_run_response(component_code, PROCESS_OPERATION_START, current_status, runtime_context, adapter_result)

        if current_status == PROCESS_STATUS_RUNNING and not allow_real_execution:
            return self._state_response(
                component_code,
                PROCESS_OPERATION_START,
                PROCESS_MESSAGE_ALREADY_RUNNING,
                current_status,
                runtime_context,
                adapter_result=adapter_result,
            )

        if not adapter_result.get("success", False):
            return self._adapter_blocked_response(component_code, PROCESS_OPERATION_START, current_status, runtime_context, adapter_result)

        stored_process = self._store_process_state(app_item, str(adapter_result.get("status", PROCESS_STATUS_RUNNING)), runtime_context, adapter_result)

        return self._state_response(
            component_code,
            PROCESS_OPERATION_START,
            PROCESS_MESSAGE_STARTED,
            stored_process.get("status", PROCESS_STATUS_RUNNING),
            runtime_context,
            stored_process,
            adapter_result,
        )

    def stop_process(self, component_code: str, dry_run: bool, allow_real_execution: bool = False) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_STOP)

        current_status = self.process_state_repository.get_status(component_code)
        process_item = self.process_state_repository.get_process(component_code)
        runtime_context = self.process_guard_tool.build_runtime_context(app_item)
        adapter = self.service_adapter_registry_tool.resolve_adapter(app_item, prefer_real=allow_real_execution)
        adapter_result = adapter.stop(app_item, process_item, dry_run, allow_real_execution, runtime_context)

        if dry_run:
            return self._dry_run_response(component_code, PROCESS_OPERATION_STOP, current_status, runtime_context, adapter_result)

        if current_status == PROCESS_STATUS_STOPPED and not allow_real_execution:
            return self._state_response(
                component_code,
                PROCESS_OPERATION_STOP,
                PROCESS_MESSAGE_ALREADY_STOPPED,
                current_status,
                runtime_context,
                adapter_result=adapter_result,
            )

        if not adapter_result.get("success", False):
            return self._adapter_blocked_response(component_code, PROCESS_OPERATION_STOP, current_status, runtime_context, adapter_result)

        stored_process = self._store_process_state(app_item, str(adapter_result.get("status", PROCESS_STATUS_STOPPED)), runtime_context, adapter_result)

        return self._state_response(
            component_code,
            PROCESS_OPERATION_STOP,
            PROCESS_MESSAGE_STOPPED,
            stored_process.get("status", PROCESS_STATUS_STOPPED),
            runtime_context,
            stored_process,
            adapter_result,
        )

    def restart_process(self, component_code: str, dry_run: bool, allow_real_execution: bool = False) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_RESTART)

        if self._is_web_frontend(self._normalize_web_code(component_code)) and self._normalize_web_code(component_code) != self._get_active_web_server_code():
            runtime_context = self.process_guard_tool.build_runtime_context(app_item)
            return self._web_server_profile_mismatch_response(
                self._normalize_web_code(component_code),
                PROCESS_OPERATION_RESTART,
                self.process_state_repository.get_status(component_code),
                runtime_context,
            )

        if dry_run:
            runtime_context = self.process_guard_tool.build_runtime_context(app_item)
            return self._dry_run_response(
                component_code,
                PROCESS_OPERATION_RESTART,
                self.process_state_repository.get_status(component_code),
                runtime_context,
                {
                    "success": True,
                    "operation": PROCESS_OPERATION_RESTART,
                    "message": PROCESS_MESSAGE_DRY_RUN,
                    "state_action": "none",
                },
            )

        stop_result = self.stop_process(component_code, dry_run=False, allow_real_execution=allow_real_execution)
        if not stop_result.get("success", False):
            return {
                "success": False,
                "operation": PROCESS_OPERATION_RESTART,
                "message": "restart_stop_failed",
                "stop_result": stop_result,
            }

        start_result = self.start_process(component_code, dry_run=False, allow_real_execution=allow_real_execution)
        start_process_data = start_result.get("process", {}) if isinstance(start_result.get("process", {}), dict) else {}
        return {
            "success": bool(start_result.get("success", False)),
            "operation": PROCESS_OPERATION_RESTART,
            "status": start_process_data.get("status", PROCESS_STATUS_RUNNING),
            "message": PROCESS_MESSAGE_RESTARTED if start_result.get("success", False) else "restart_start_failed",
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "process": start_process_data,
            "stop_result": stop_result,
            "start_result": start_result,
        }

    def _real_profile_update_response(
        self,
        component_code: str,
        install_path: str,
        enabled: bool | None,
        dry_run: bool,
    ) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)
        if app_item is None:
            return self._app_not_found_response(component_code, PROCESS_OPERATION_REAL_PROFILE_APPLY)

        try:
            next_app_item = self._build_real_profile_update(app_item, install_path, enabled)
            runtime_context = self.process_guard_tool.build_runtime_context(next_app_item)
        except ValueError as error:
            return {
                "success": False,
                "operation": PROCESS_OPERATION_REAL_PROFILE_PLAN if dry_run else PROCESS_OPERATION_REAL_PROFILE_APPLY,
                "message": PROCESS_MESSAGE_REAL_PROFILE_INVALID_PATH,
                "error": str(error),
                "component_code": component_code,
            }

        if dry_run:
            return {
                "success": True,
                "operation": PROCESS_OPERATION_REAL_PROFILE_PLAN,
                "message": PROCESS_MESSAGE_REAL_PROFILE_DRY_RUN,
                "profile": self._build_real_profile_view(next_app_item, runtime_context),
                "current_profile": self._build_real_profile_view(app_item, self.process_guard_tool.build_runtime_context(app_item)),
                "will_write": False,
            }

        stored_app_item = self.app_registry_repository.upsert_app(next_app_item)
        stored_runtime_context = self.process_guard_tool.build_runtime_context(stored_app_item)
        return {
            "success": True,
            "operation": PROCESS_OPERATION_REAL_PROFILE_APPLY,
            "message": PROCESS_MESSAGE_REAL_PROFILE_UPDATED,
            "profile": self._build_real_profile_view(stored_app_item, stored_runtime_context),
            "will_write": True,
        }

    def _build_real_profile_update(
        self,
        app_item: dict[str, Any],
        install_path: str,
        enabled: bool | None,
    ) -> dict[str, Any]:
        next_app_item = deepcopy(app_item)
        real_process = deepcopy(next_app_item.get("real_process", {}))
        if not isinstance(real_process, dict):
            real_process = {}

        normalized_install_path = str(install_path or "").strip().replace("\\", "/")
        if normalized_install_path:
            resolved_path = self.process_guard_tool.safe_path_tool.resolve_inside_root(normalized_install_path)
            next_app_item["install_path"] = self._format_profile_path(resolved_path)

        if enabled is not None:
            real_process["enabled"] = bool(enabled)

        next_app_item["real_process"] = real_process
        return next_app_item

    def _build_real_profile_view(self, app_item: dict[str, Any], runtime_context: dict[str, Any]) -> dict[str, Any]:
        real_process = app_item.get("real_process", {})
        if not isinstance(real_process, dict):
            real_process = {}

        return {
            "code": str(app_item.get("code", "")).strip(),
            "name": app_item.get("name"),
            "version": app_item.get("version"),
            "install_path": app_item.get("install_path"),
            "install_path_resolved": runtime_context.get("install_path"),
            "install_path_exists": runtime_context.get("install_path_exists"),
            "real_process_enabled": runtime_context.get("real_process_enabled"),
            "real_process_name": runtime_context.get("real_process_name"),
            "real_executable_path": runtime_context.get("real_executable_path"),
            "real_executable_exists": runtime_context.get("real_executable_exists"),
            "real_working_dir": runtime_context.get("real_working_dir"),
            "executable_candidates": real_process.get("executable_candidates", []),
            "start_args": real_process.get("start_args", []),
            "stop_args": real_process.get("stop_args", []),
            "status_args": real_process.get("status_args", []),
        }

    def _build_process_view(self, app_item: dict[str, Any], adapter_result: dict[str, Any] | None = None) -> dict[str, Any]:
        component_code = str(app_item.get("code", "")).strip()
        process_item = self.process_state_repository.get_process(component_code) or {}
        runtime_context = self.process_guard_tool.build_runtime_context(app_item)
        adapter = self.service_adapter_registry_tool.resolve_adapter(app_item)
        adapter_info = adapter.describe()
        adapter_status = None
        real_process_probe = None
        if isinstance(adapter_result, dict):
            adapter_status = adapter_result.get("status")
            adapter_context = adapter_result.get("runtime_context", {})
            if isinstance(adapter_context, dict):
                real_process_probe = adapter_context.get("real_process_probe")

        return {
            "code": component_code,
            "name": app_item.get("name"),
            "version": app_item.get("version"),
            "status": adapter_status or process_item.get("status", PROCESS_STATUS_STOPPED),
            "stored_status": process_item.get("status", PROCESS_STATUS_STOPPED),
            "mode": runtime_context.get("mode", PROCESS_MODE_SIMULATED),
            "adapter": adapter_info,
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "install_path": runtime_context.get("install_path"),
            "install_path_exists": runtime_context.get("install_path_exists"),
            "real_process_enabled": runtime_context.get("real_process_enabled"),
            "real_executable_path": runtime_context.get("real_executable_path"),
            "real_executable_exists": runtime_context.get("real_executable_exists"),
            "real_process_probe": real_process_probe,
            "last_started_at": process_item.get("last_started_at"),
            "last_stopped_at": process_item.get("last_stopped_at"),
            "updated_at": process_item.get("updated_at"),
        }

    def _store_process_state(
        self,
        app_item: dict[str, Any],
        status: str,
        runtime_context: dict[str, Any],
        adapter_result: dict[str, Any],
    ) -> dict[str, Any]:
        now_value = datetime.now(timezone.utc).isoformat()
        component_code = str(app_item.get("code", "")).strip()
        existing_process = self.process_state_repository.get_process(component_code) or {}
        adapter_info = adapter_result.get("adapter", {})

        process_data = {
            "code": component_code,
            "name": app_item.get("name"),
            "version": app_item.get("version"),
            "status": status,
            "mode": runtime_context.get("mode", PROCESS_MODE_SIMULATED),
            "adapter_key": adapter_info.get("key"),
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "install_path": runtime_context.get("install_path"),
            "real_process_enabled": runtime_context.get("real_process_enabled"),
            "real_executable_path": runtime_context.get("real_executable_path"),
            "adapter_status": adapter_result.get("status"),
            "adapter_message": adapter_result.get("message"),
        }

        adapter_context = adapter_result.get("runtime_context", {})
        if isinstance(adapter_context, dict):
            process_data["command_result"] = adapter_context.get("command_result")
            process_data["verification_probe"] = adapter_context.get("verification_probe")

        if status == PROCESS_STATUS_RUNNING:
            process_data["last_started_at"] = now_value
            process_data["last_stopped_at"] = existing_process.get("last_stopped_at")

        if status == PROCESS_STATUS_STOPPED:
            process_data["last_started_at"] = existing_process.get("last_started_at")
            process_data["last_stopped_at"] = now_value

        return self.process_state_repository.upsert_process(process_data)

    def _dry_run_response(
        self,
        component_code: str,
        operation: str,
        current_status: str,
        runtime_context: dict[str, Any],
        adapter_result: dict[str, Any],
    ) -> dict[str, Any]:
        return self._state_response(
            component_code,
            operation,
            PROCESS_MESSAGE_DRY_RUN,
            current_status,
            runtime_context,
            adapter_result=adapter_result,
        )

    def _port_guard_blocked_response(
        self,
        component_code: str,
        operation: str,
        current_status: str,
        runtime_context: dict[str, Any],
        port_guard_result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            **self._state_response(
                component_code,
                operation,
                str(port_guard_result.get(WEB_SERVER_PORT_GUARD_MESSAGE_KEY, "web_server_port_guard_blocked")),
                current_status,
                runtime_context,
            ),
            "success": False,
            "port_guard": port_guard_result,
        }

    def _adapter_blocked_response(
        self,
        component_code: str,
        operation: str,
        current_status: str,
        runtime_context: dict[str, Any],
        adapter_result: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            **self._state_response(
                component_code,
                operation,
                str(adapter_result.get("message", "adapter_blocked")),
                current_status,
                runtime_context,
                adapter_result=adapter_result,
            ),
            "success": False,
        }

    def _web_server_profile_mismatch_response(
        self,
        component_code: str,
        operation: str,
        current_status: str,
        runtime_context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            **self._state_response(
                component_code,
                operation,
                PROCESS_MESSAGE_WEB_SERVER_PROFILE_MISMATCH,
                current_status,
                runtime_context,
            ),
            "success": False,
        }

    def _state_response(
        self,
        component_code: str,
        operation: str,
        message: str,
        status: str,
        runtime_context: dict[str, Any],
        stored_process: dict[str, Any] | None = None,
        adapter_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "success": True,
            "operation": operation,
            "message": message,
            WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
            "process": {
                "code": component_code,
                "status": status,
                "mode": runtime_context.get("mode", PROCESS_MODE_SIMULATED),
                "adapter": (adapter_result or {}).get("adapter"),
                WEB_SERVER_ACTIVE_PROFILE_KEY: self._get_active_web_server_code(),
                WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
                "install_path": runtime_context.get("install_path"),
                "install_path_exists": runtime_context.get("install_path_exists"),
                "real_process_enabled": runtime_context.get("real_process_enabled"),
                "real_executable_path": runtime_context.get("real_executable_path"),
                "real_executable_exists": runtime_context.get("real_executable_exists"),
                "stored": stored_process,
            },
            "adapter_result": adapter_result,
        }

    def _stop_other_web_server_before_start(
        self,
        component_code: str,
        dry_run: bool,
        allow_real_execution: bool,
    ) -> dict[str, Any] | None:
        if dry_run or not self._is_web_frontend(component_code):
            return None

        other_code = self._other_web_server_code(component_code)
        if not other_code:
            return None

        if self.process_state_repository.get_status(other_code) != PROCESS_STATUS_RUNNING:
            return None

        return self.stop_process(other_code, dry_run=False, allow_real_execution=allow_real_execution)

    def _get_active_web_server_code(self) -> str:
        current_profile = self.web_server_profile_registry_repository.get_current_profile()
        if current_profile is None:
            return WEB_SERVER_PROFILE_DEFAULT

        normalized_code = self._normalize_web_code(str(current_profile.get("server_code", WEB_SERVER_PROFILE_DEFAULT)))
        return normalized_code if self._is_web_frontend(normalized_code) else WEB_SERVER_PROFILE_DEFAULT

    def _other_web_server_code(self, component_code: str) -> str:
        if component_code == SERVICE_CODE_APACHE:
            return SERVICE_CODE_NGINX
        if component_code == SERVICE_CODE_NGINX:
            return SERVICE_CODE_APACHE
        return ""

    def _is_web_frontend(self, component_code: str) -> bool:
        return component_code in WEB_SERVER_FRONTEND_CODES

    def _normalize_web_code(self, component_code: str) -> str:
        normalized_code = str(component_code or "").strip().lower()
        if normalized_code == SERVICE_CODE_APACHE:
            return SERVICE_CODE_APACHE
        if normalized_code == SERVICE_CODE_NGINX:
            return SERVICE_CODE_NGINX
        return normalized_code

    def _format_profile_path(self, file_path: Path) -> str:
        try:
            relative_path = file_path.relative_to(self.process_guard_tool.safe_path_tool.root_path)
            return str(relative_path).replace("/", "\\")
        except ValueError:
            return str(file_path).replace("/", "\\")

    def _app_not_found_response(self, component_code: str, operation: str) -> dict[str, Any]:
        return {
            "success": False,
            "operation": operation,
            "error": PROCESS_MESSAGE_APP_NOT_FOUND,
            "component_code": component_code,
        }
