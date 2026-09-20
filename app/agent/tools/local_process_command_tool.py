# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\local_process_command_tool.py
# 📌 Amac: Guardli local process komutlarini shell kullanmadan calistirir
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Windows executable start/stop komutlarini argv listesi olarak dogrular, shell kullanmadan calistirir ve eksik stop komutlarini bloklar
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import os
import subprocess

from config.constants import (
    PROCESS_OPERATION_START,
    PROCESS_OPERATION_STOP,
    PROCESS_STATUS_RUNNING,
    PROCESS_STATUS_STOPPED,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_EXECUTED,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_UNSUPPORTED_OS,
    SERVICE_ADAPTER_MESSAGE_REAL_STOP_COMMAND_MISSING,
)


class LocalProcessCommandTool:
    def execute(self, command: list[str], working_dir: str, operation: str) -> dict[str, Any]:
        if not command:
            return {
                "success": False,
                "operation": operation,
                "message": "real process command is empty",
                "command": [],
                "working_dir": working_dir,
            }

        if operation == PROCESS_OPERATION_STOP and len(command) <= 1:
            return {
                "success": False,
                "operation": operation,
                "message": SERVICE_ADAPTER_MESSAGE_REAL_STOP_COMMAND_MISSING,
                "command": command,
                "working_dir": working_dir,
            }

        if os.name != "nt":
            return {
                "success": False,
                "operation": operation,
                "message": SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_UNSUPPORTED_OS,
                "command": command,
                "working_dir": working_dir,
            }

        executable_path = Path(command[0])
        if not executable_path.exists():
            return {
                "success": False,
                "operation": operation,
                "message": "real process executable does not exist",
                "command": command,
                "working_dir": working_dir,
            }

        cwd_path = Path(working_dir) if working_dir else executable_path.parent
        if not cwd_path.exists():
            cwd_path = executable_path.parent

        if operation == PROCESS_OPERATION_START:
            subprocess.Popen(
                command,
                cwd=str(cwd_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            )
            status = PROCESS_STATUS_RUNNING
            return_code = 0
        else:
            completed = subprocess.run(
                command,
                cwd=str(cwd_path),
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            )
            status = PROCESS_STATUS_STOPPED if completed.returncode == 0 else "unknown"
            return_code = completed.returncode
            if completed.returncode != 0:
                return {
                    "success": False,
                    "operation": operation,
                    "status": status,
                    "message": completed.stderr.strip() or completed.stdout.strip() or "real process command failed",
                    "return_code": completed.returncode,
                    "command": command,
                    "working_dir": str(cwd_path),
                }

        return {
            "success": True,
            "operation": operation,
            "status": status,
            "message": SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_EXECUTED,
            "return_code": return_code,
            "command": command,
            "working_dir": str(cwd_path),
        }
