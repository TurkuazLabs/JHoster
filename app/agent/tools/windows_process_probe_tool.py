# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\windows_process_probe_tool.py
# 📌 Amac: Windows uzerinde process adina gore calisma durumunu guvenli sekilde denetler
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: tasklist komutunu shell kullanmadan calistirarak servis process denetimi yapar
# Bagimli Oldugu Katman: Tool

from typing import Any
import csv
import io
import os
import subprocess

from config.constants import (
    PROCESS_STATUS_RUNNING,
    PROCESS_STATUS_STOPPED,
    PROCESS_STATUS_UNKNOWN,
    SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_UNSUPPORTED_OS,
)


class WindowsProcessProbeTool:
    def inspect(self, process_name: str) -> dict[str, Any]:
        normalized_name = str(process_name or "").strip()
        if not normalized_name:
            return {
                "success": False,
                "status": PROCESS_STATUS_UNKNOWN,
                "running": False,
                "message": "process_name_missing",
                "process_name": normalized_name,
                "matches": [],
            }

        if os.name != "nt":
            return {
                "success": False,
                "status": PROCESS_STATUS_UNKNOWN,
                "running": False,
                "message": SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_UNSUPPORTED_OS,
                "process_name": normalized_name,
                "matches": [],
            }

        try:
            completed = subprocess.run(
                [
                    "tasklist",
                    "/FI",
                    f"IMAGENAME eq {normalized_name}",
                    "/FO",
                    "CSV",
                    "/NH",
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "status": PROCESS_STATUS_UNKNOWN,
                "running": False,
                "message": "process_probe_timeout",
                "process_name": normalized_name,
                "matches": [],
            }

        if completed.returncode != 0:
            return {
                "success": False,
                "status": PROCESS_STATUS_UNKNOWN,
                "running": False,
                "message": completed.stderr.strip() or completed.stdout.strip() or "process_probe_failed",
                "process_name": normalized_name,
                "matches": [],
                "return_code": completed.returncode,
            }

        matches = self._parse_tasklist_csv(completed.stdout, normalized_name)
        running = len(matches) > 0
        return {
            "success": True,
            "status": PROCESS_STATUS_RUNNING if running else PROCESS_STATUS_STOPPED,
            "running": running,
            "message": "process_probe_ready",
            "process_name": normalized_name,
            "matches": matches,
            "return_code": completed.returncode,
        }

    def _parse_tasklist_csv(self, output: str, process_name: str) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        normalized_name = process_name.lower()
        content = str(output or "").strip()
        if not content or "INFO:" in content.upper():
            return rows

        reader = csv.reader(io.StringIO(content))
        for row in reader:
            if len(row) < 2:
                continue
            image_name = str(row[0]).strip()
            if image_name.lower() != normalized_name:
                continue
            rows.append({
                "image_name": image_name,
                "pid": str(row[1]).strip(),
                "session_name": str(row[2]).strip() if len(row) > 2 else "",
                "session_number": str(row[3]).strip() if len(row) > 3 else "",
                "memory_usage": str(row[4]).strip() if len(row) > 4 else "",
            })
        return rows
