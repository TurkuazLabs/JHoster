# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\process_guard_tool.py
# 📌 Amac: Process manager icin app runtime ve real executable yollarini guvenli sekilde dogrular
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Kurulu app path, real process config, executable candidate ve komut preflight context uretimi yapan tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import PROCESS_MODE_SIMULATED, PROCESS_MODE_REAL
from tools.safe_path_tool import SafePathTool


class ProcessGuardTool:
    def __init__(self, safe_path_tool: SafePathTool) -> None:
        self.safe_path_tool = safe_path_tool

    def build_runtime_context(self, app_item: dict[str, Any]) -> dict[str, Any]:
        install_path_value = str(app_item.get("install_path", "")).strip()
        normalized_install_path = install_path_value.replace("\\", "/")
        install_path = self.safe_path_tool.resolve_inside_root(normalized_install_path)
        real_process = app_item.get("real_process", {})
        if not isinstance(real_process, dict):
            real_process = {}

        executable_path = self._resolve_first_existing_candidate(install_path, real_process.get("executable_candidates", []))
        executable_exists = executable_path is not None and executable_path.exists()
        resolved_executable = executable_path or self._resolve_first_candidate(install_path, real_process.get("executable_candidates", []))
        working_dir = self._resolve_working_dir(install_path, real_process.get("working_dir", ""), resolved_executable)

        context = {
            "mode": PROCESS_MODE_SIMULATED,
            "install_path": self._format_path(install_path),
            "install_path_exists": install_path.exists(),
            "external_process": False,
            "real_process_enabled": bool(real_process.get("enabled", False)),
            "real_mode": PROCESS_MODE_REAL,
            "real_process_name": str(real_process.get("process_name", "")).strip(),
            "real_executable_path": self._format_path(resolved_executable) if resolved_executable else "",
            "real_executable_exists": executable_exists,
            "real_working_dir": self._format_path(working_dir) if working_dir else "",
        }
        context["real_start_command"] = self._build_command(resolved_executable, real_process.get("start_args", []))
        context["real_stop_command"] = self._build_command(resolved_executable, real_process.get("stop_args", []))
        context["real_status_command"] = self._build_command(resolved_executable, real_process.get("status_args", []))
        return context

    def _resolve_first_existing_candidate(self, install_path: Path, candidates: Any) -> Path | None:
        for candidate in self._candidate_values(candidates):
            candidate_path = self._resolve_candidate_path(install_path, candidate)
            if candidate_path.exists():
                return candidate_path
        return None

    def _resolve_first_candidate(self, install_path: Path, candidates: Any) -> Path | None:
        for candidate in self._candidate_values(candidates):
            return self._resolve_candidate_path(install_path, candidate)
        return None

    def _resolve_candidate_path(self, install_path: Path, candidate: str) -> Path:
        normalized_candidate = candidate.replace("\\", "/")
        if ":" in normalized_candidate or normalized_candidate.startswith("/"):
            return Path(candidate)
        return install_path / normalized_candidate

    def _resolve_working_dir(self, install_path: Path, working_dir_value: Any, executable_path: Path | None) -> Path | None:
        working_dir_text = str(working_dir_value or "").strip().replace("\\", "/")
        if working_dir_text:
            if ":" in working_dir_text or working_dir_text.startswith("/"):
                return Path(working_dir_text)
            return install_path / working_dir_text
        if executable_path is not None:
            return executable_path.parent
        return install_path

    def _build_command(self, executable_path: Path | None, args: Any) -> list[str]:
        if executable_path is None:
            return []
        return [self._format_path(executable_path), *self._argument_values(args)]

    def _candidate_values(self, candidates: Any) -> list[str]:
        if not isinstance(candidates, list):
            return []
        return [str(candidate).strip() for candidate in candidates if str(candidate).strip()]

    def _argument_values(self, args: Any) -> list[str]:
        if not isinstance(args, list):
            return []
        return [str(argument) for argument in args]

    def _format_path(self, file_path: Path) -> str:
        return str(file_path).replace("/", "\\")
