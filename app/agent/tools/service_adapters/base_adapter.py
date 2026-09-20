# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\service_adapters\base_adapter.py
# 📌 Amac: JHoster runtime service adapter sozlesmesini tanimlar
# 📌 Modul - FileType
# Version: 1.4.0
# Aciklama: Adapter yetenekleri, preflight, real status probe, start, stop ve verification sonuc formatini standartlastirir
# Bagimli Oldugu Katman: Tool

from typing import Any

from config.constants import (
    PROCESS_OPERATION_PREFLIGHT,
    PROCESS_OPERATION_START,
    PROCESS_OPERATION_STATUS,
    PROCESS_OPERATION_STOP,
    PROCESS_STATUS_RUNNING,
    PROCESS_STATUS_STOPPED,
    SERVICE_ADAPTER_CAPABILITY_DRY_RUN,
    SERVICE_ADAPTER_CAPABILITY_REAL_PROCESS,
    SERVICE_ADAPTER_CAPABILITY_SIMULATED_STATE,
    SERVICE_ADAPTER_MESSAGE_DRY_RUN,
    SERVICE_ADAPTER_MESSAGE_REAL_EXECUTION_REQUIRED,
    SERVICE_ADAPTER_MESSAGE_REAL_EXECUTABLE_MISSING,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_CONFIG_DISABLED,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_DISABLED,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_VERIFICATION_FAILED,
    SERVICE_ADAPTER_MODE_BLOCKED,
)
from tools.local_process_command_tool import LocalProcessCommandTool
from tools.windows_process_probe_tool import WindowsProcessProbeTool


class BaseServiceAdapter:
    adapter_key = SERVICE_ADAPTER_MODE_BLOCKED
    adapter_name = "Blocked Adapter"
    description = "Runtime adapter is not configured."
    capabilities: list[str] = [SERVICE_ADAPTER_CAPABILITY_DRY_RUN]
    real_process_enabled = False

    def describe(self) -> dict[str, Any]:
        return {
            "key": self.adapter_key,
            "name": self.adapter_name,
            "description": self.description,
            "capabilities": self.capabilities,
            "real_process_enabled": self.real_process_enabled,
        }

    def preflight(self, app_item: dict[str, Any], runtime_context: dict[str, Any]) -> dict[str, Any]:
        return self._result(
            operation=PROCESS_OPERATION_PREFLIGHT,
            status=self._preflight_status(runtime_context),
            message="adapter_preflight_ready",
            state_action="none",
            context=runtime_context,
        )

    def status(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return self._result(
            operation=PROCESS_OPERATION_STATUS,
            status=self._stored_status(process_item),
            message="adapter_status_ready",
            state_action="none",
            context=runtime_context,
        )


    def start(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_START, process_item)

        return self._blocked_result(PROCESS_OPERATION_START, process_item)

    def stop(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_STOP, process_item)

        return self._blocked_result(PROCESS_OPERATION_STOP, process_item)

    def _dry_run_result(self, operation: str, process_item: dict[str, Any] | None) -> dict[str, Any]:
        return self._result(
            operation=operation,
            status=self._stored_status(process_item),
            message=SERVICE_ADAPTER_MESSAGE_DRY_RUN,
            state_action="none",
        )

    def _blocked_result(self, operation: str, process_item: dict[str, Any] | None) -> dict[str, Any]:
        return self._result(
            operation=operation,
            status=self._stored_status(process_item),
            message=SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_DISABLED,
            state_action="none",
            success=False,
        )

    def _stored_status(self, process_item: dict[str, Any] | None) -> str:
        if not process_item:
            return PROCESS_STATUS_STOPPED

        return str(process_item.get("status", PROCESS_STATUS_STOPPED))

    def _preflight_status(self, runtime_context: dict[str, Any]) -> str:
        if runtime_context.get("real_process_enabled") and runtime_context.get("real_executable_exists"):
            return "ready"
        return "blocked"

    def _result(
        self,
        operation: str,
        status: str,
        message: str,
        state_action: str,
        success: bool = True,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        result = {
            "success": success,
            "operation": operation,
            "status": status,
            "message": message,
            "state_action": state_action,
            "adapter": self.describe(),
        }
        if context is not None:
            result["runtime_context"] = context
        return result


class SimulatedServiceAdapter(BaseServiceAdapter):
    adapter_key = "simulated"
    adapter_name = "Simulated State Adapter"
    description = "Stores runtime state without starting an OS process."
    capabilities = [SERVICE_ADAPTER_CAPABILITY_DRY_RUN, SERVICE_ADAPTER_CAPABILITY_SIMULATED_STATE]
    real_process_enabled = False

    def start(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_START, process_item)

        return self._result(
            operation=PROCESS_OPERATION_START,
            status=PROCESS_STATUS_RUNNING,
            message="simulated_process_should_mark_running",
            state_action="mark_running",
        )

    def stop(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_STOP, process_item)

        return self._result(
            operation=PROCESS_OPERATION_STOP,
            status=PROCESS_STATUS_STOPPED,
            message="simulated_process_should_mark_stopped",
            state_action="mark_stopped",
        )


class PlannedRuntimeServiceAdapter(BaseServiceAdapter):
    def __init__(self, adapter_key: str, adapter_name: str, description: str) -> None:
        self.adapter_key = adapter_key
        self.adapter_name = adapter_name
        self.description = description
        self.capabilities = [SERVICE_ADAPTER_CAPABILITY_DRY_RUN, SERVICE_ADAPTER_CAPABILITY_SIMULATED_STATE]
        self.real_process_enabled = False

    def start(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_START, process_item)

        return self._result(
            operation=PROCESS_OPERATION_START,
            status=PROCESS_STATUS_RUNNING,
            message="planned_runtime_should_mark_running",
            state_action="mark_running",
            context=runtime_context,
        )

    def stop(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_STOP, process_item)

        return self._result(
            operation=PROCESS_OPERATION_STOP,
            status=PROCESS_STATUS_STOPPED,
            message="planned_runtime_should_mark_stopped",
            state_action="mark_stopped",
            context=runtime_context,
        )


class GuardedLocalProcessServiceAdapter(BaseServiceAdapter):
    def __init__(self, adapter_key: str, adapter_name: str, description: str) -> None:
        self.adapter_key = adapter_key
        self.adapter_name = adapter_name
        self.description = description
        self.capabilities = [SERVICE_ADAPTER_CAPABILITY_DRY_RUN, SERVICE_ADAPTER_CAPABILITY_REAL_PROCESS]
        self.real_process_enabled = True
        self.local_process_command_tool = LocalProcessCommandTool()
        self.windows_process_probe_tool = WindowsProcessProbeTool()

    def preflight(self, app_item: dict[str, Any], runtime_context: dict[str, Any]) -> dict[str, Any]:
        context = runtime_context or {}
        probe_result = self.windows_process_probe_tool.inspect(str(context.get("real_process_name", "")))
        status = self._preflight_status(context)
        return self._result(
            operation=PROCESS_OPERATION_PREFLIGHT,
            status=status,
            message="adapter_preflight_ready",
            state_action="none",
            success=(status == "ready"),
            context={**context, "real_process_probe": probe_result},
        )

    def status(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = runtime_context or {}
        probe_result = self.windows_process_probe_tool.inspect(str(context.get("real_process_name", "")))
        probe_success = bool(probe_result.get("success", False))
        probe_status = str(probe_result.get("status", self._stored_status(process_item)))
        return self._result(
            operation=PROCESS_OPERATION_STATUS,
            status=probe_status if probe_success else self._stored_status(process_item),
            message="real_process_probe_ready" if probe_success else str(probe_result.get("message", "real_process_probe_failed")),
            state_action="none",
            success=probe_success,
            context={**context, "real_process_probe": probe_result},
        )

    def start(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_START, process_item)
        return self._execute_real(PROCESS_OPERATION_START, PROCESS_STATUS_RUNNING, allow_real_execution, runtime_context)

    def stop(
        self,
        app_item: dict[str, Any],
        process_item: dict[str, Any] | None,
        dry_run: bool,
        allow_real_execution: bool = False,
        runtime_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if dry_run:
            return self._dry_run_result(PROCESS_OPERATION_STOP, process_item)
        return self._execute_real(PROCESS_OPERATION_STOP, PROCESS_STATUS_STOPPED, allow_real_execution, runtime_context)

    def _execute_real(
        self,
        operation: str,
        expected_status: str,
        allow_real_execution: bool,
        runtime_context: dict[str, Any] | None,
    ) -> dict[str, Any]:
        context = runtime_context or {}
        if not allow_real_execution:
            return self._result(operation, "blocked", SERVICE_ADAPTER_MESSAGE_REAL_EXECUTION_REQUIRED, "none", False, context)

        if not context.get("real_process_enabled"):
            return self._result(operation, "blocked", SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_CONFIG_DISABLED, "none", False, context)

        if not context.get("real_executable_exists"):
            return self._result(operation, "blocked", SERVICE_ADAPTER_MESSAGE_REAL_EXECUTABLE_MISSING, "none", False, context)

        command_key = "real_start_command" if operation == PROCESS_OPERATION_START else "real_stop_command"
        command = context.get(command_key, [])
        if not isinstance(command, list):
            command = []

        tool_result = self.local_process_command_tool.execute(command, str(context.get("real_working_dir", "")), operation)
        if not tool_result.get("success", False):
            return self._result(
                operation,
                str(tool_result.get("status", "blocked")),
                str(tool_result.get("message", "real_process_failed")),
                "none",
                False,
                {**context, "command_result": tool_result},
            )

        verification_probe = self.windows_process_probe_tool.inspect(str(context.get("real_process_name", "")))
        verification_success = bool(verification_probe.get("success", False))
        verification_status = str(verification_probe.get("status", expected_status))
        verified = verification_success and verification_status == expected_status
        if verification_success and not verified:
            return self._result(
                operation,
                verification_status,
                SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_VERIFICATION_FAILED,
                "none",
                False,
                {**context, "command_result": tool_result, "verification_probe": verification_probe},
            )

        final_status = verification_status if verification_success else expected_status
        return self._result(
            operation,
            final_status,
            str(tool_result.get("message", "real_process_executed")),
            "mark_" + final_status,
            True,
            {**context, "command_result": tool_result, "verification_probe": verification_probe},
        )
