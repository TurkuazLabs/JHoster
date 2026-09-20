# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\nginx_real_reloader_tool.py
# 📌 Amac: Tespit edilmis nginx.exe ile nginx -s reload real adapter planini ve izinli calistirmayi yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Shell kullanmadan executable, main config, validate kaydi ve vhost path guvenligi kontrolu yapar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os
import subprocess

from config.constants import (
    NGINX_EXECUTABLE_FILE_NAME_WINDOWS,
    NGINX_PUBLISHED_DIRECTORY_NAME,
    NGINX_REAL_RELOAD_COMMAND_LABEL,
    NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS,
    NGINX_REAL_RELOAD_ENV_MAIN_CONFIG,
    NGINX_REAL_RELOAD_MAIN_CONFIG_FILE_NAME,
    NGINX_REAL_RELOAD_MESSAGE_DRY_RUN,
    NGINX_REAL_RELOAD_MESSAGE_REJECTED,
    NGINX_REAL_RELOAD_MESSAGE_RELOADED,
    NGINX_REAL_RELOAD_MESSAGE_SKIPPED,
    NGINX_REAL_RELOAD_MODE_REAL_ADAPTER,
    NGINX_REAL_RELOAD_STATUS_PLANNED,
    NGINX_REAL_RELOAD_STATUS_REJECTED,
    NGINX_REAL_RELOAD_STATUS_RELOADED,
    NGINX_REAL_RELOAD_STATUS_SKIPPED,
    NGINX_REAL_VALIDATE_STATUS_VALID,
    NGINX_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class NginxRealReloaderTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / NGINX_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.default_main_config_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / "nginx" / "conf" / NGINX_REAL_RELOAD_MAIN_CONFIG_FILE_NAME
        ).resolve()

    def build_real_reload_plan(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
        validation_record: dict[str, Any],
        allow_real_execution: bool,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        target_path = published_config_file.resolve()
        executable_path = self._resolve_path(str(executable_record.get("path_absolute") or executable_record.get("path") or ""))
        main_config_path = self._resolve_main_config_path()
        validation_status = str(validation_record.get("status", "")).strip().lower()

        target_exists = target_path.is_file()
        target_is_safe = self._is_inside_path(target_path, self.publish_root_path)
        target_extension_is_safe = target_path.suffix == NGINX_VHOST_EXTENSION

        executable_exists = executable_path.is_file()
        executable_name_is_safe = executable_path.name.lower() == NGINX_EXECUTABLE_FILE_NAME_WINDOWS
        executable_is_safe = executable_name_is_safe and self._is_allowed_executable_path(
            executable_path=executable_path,
            executable_record=executable_record,
        )

        main_config_exists = main_config_path.is_file()
        main_config_name_is_safe = main_config_path.name.lower() == NGINX_REAL_RELOAD_MAIN_CONFIG_FILE_NAME
        main_config_is_safe = main_config_name_is_safe and self._is_inside_path(main_config_path, self.root_path)
        validation_allows_reload = validation_status == NGINX_REAL_VALIDATE_STATUS_VALID

        command = [str(executable_path), "-s", "reload", "-c", str(main_config_path)]
        path_safe = all(
            [
                target_exists,
                target_is_safe,
                target_extension_is_safe,
                executable_exists,
                executable_is_safe,
                main_config_exists,
                main_config_is_safe,
            ]
        )
        safe = path_safe and validation_allows_reload

        return {
            "project_code": normalized_project_code,
            "published_config_file": self._to_relative(target_path),
            "published_config_file_absolute": str(target_path),
            "main_config_file": self._to_relative(main_config_path),
            "main_config_file_absolute": str(main_config_path),
            "nginx_executable_file": str(executable_path),
            "nginx_executable_file_absolute": str(executable_path),
            "target_exists": target_exists,
            "target_is_safe": target_is_safe,
            "target_extension_is_safe": target_extension_is_safe,
            "executable_exists": executable_exists,
            "executable_name_is_safe": executable_name_is_safe,
            "executable_is_safe": executable_is_safe,
            "main_config_exists": main_config_exists,
            "main_config_name_is_safe": main_config_name_is_safe,
            "main_config_is_safe": main_config_is_safe,
            "validation_status": validation_status,
            "validation_allows_reload": validation_allows_reload,
            "reload_mode": NGINX_REAL_RELOAD_MODE_REAL_ADAPTER,
            "command_label": NGINX_REAL_RELOAD_COMMAND_LABEL,
            "command": command,
            "shell_execution": False,
            "real_nginx_execution_requested": allow_real_execution,
            "real_nginx_execution": False,
            "path_safe": path_safe,
            "safe": safe,
            "planned_at": self._now(),
        }

    def reload_with_real_adapter(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
        validation_record: dict[str, Any],
        dry_run: bool,
        allow_real_execution: bool,
    ) -> dict[str, Any]:
        plan = self.build_real_reload_plan(
            project_code=project_code,
            published_config_file=published_config_file,
            executable_record=executable_record,
            validation_record=validation_record,
            allow_real_execution=allow_real_execution,
        )

        if dry_run:
            return {
                "success": True,
                "status": NGINX_REAL_RELOAD_STATUS_PLANNED,
                "message": NGINX_REAL_RELOAD_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": NGINX_REAL_RELOAD_STATUS_REJECTED,
                "message": NGINX_REAL_RELOAD_MESSAGE_REJECTED,
                "plan": plan,
                "reload_result": {
                    "real_nginx_execution": False,
                    "shell_execution": False,
                    "reason": "real validation must be valid before real reload",
                },
                "reloaded_at": self._now(),
            }

        if not allow_real_execution:
            return {
                "success": True,
                "status": NGINX_REAL_RELOAD_STATUS_SKIPPED,
                "message": NGINX_REAL_RELOAD_MESSAGE_SKIPPED,
                "plan": plan,
                "reload_result": {
                    "real_nginx_execution": False,
                    "shell_execution": False,
                    "reason": "allow_real_execution is false",
                },
                "reloaded_at": self._now(),
            }

        execution_result = self._execute_nginx_reload(plan)
        passed = execution_result.get("return_code") == 0

        return {
            "success": passed,
            "status": NGINX_REAL_RELOAD_STATUS_RELOADED if passed else NGINX_REAL_RELOAD_STATUS_REJECTED,
            "message": NGINX_REAL_RELOAD_MESSAGE_RELOADED if passed else NGINX_REAL_RELOAD_MESSAGE_REJECTED,
            "plan": {
                **plan,
                "real_nginx_execution": True,
            },
            "reload_result": execution_result,
            "reloaded_at": self._now(),
        }

    def _execute_nginx_reload(self, plan: dict[str, Any]) -> dict[str, Any]:
        command = [str(item) for item in plan.get("command", [])]
        executable_dir = str(Path(command[0]).resolve().parent) if command else str(self.root_path)

        try:
            completed_process = subprocess.run(
                command,
                cwd=executable_dir,
                shell=False,
                text=True,
                capture_output=True,
                timeout=NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS,
                check=False,
            )

            return {
                "real_nginx_execution": True,
                "shell_execution": False,
                "return_code": completed_process.returncode,
                "stdout": completed_process.stdout.strip(),
                "stderr": completed_process.stderr.strip(),
                "timeout_seconds": NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS,
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "real_nginx_execution": True,
                "shell_execution": False,
                "return_code": -1,
                "stdout": str(exc.stdout or "").strip(),
                "stderr": "nginx reload command timeout",
                "timeout_seconds": NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS,
            }
        except OSError as exc:
            return {
                "real_nginx_execution": True,
                "shell_execution": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc),
                "timeout_seconds": NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS,
            }

    def _resolve_main_config_path(self) -> Path:
        env_main_config = os.getenv(NGINX_REAL_RELOAD_ENV_MAIN_CONFIG, "").strip()
        raw_path = env_main_config if env_main_config else str(self.default_main_config_path)

        return self._resolve_path(raw_path)

    def _resolve_path(self, raw_path: str) -> Path:
        if not raw_path.strip():
            return (self.root_path / "__missing_path__").resolve()

        path_value = Path(raw_path)

        if path_value.is_absolute():
            return path_value.resolve()

        return (self.root_path / path_value).resolve()

    def _is_allowed_executable_path(self, executable_path: Path, executable_record: dict[str, Any]) -> bool:
        source = str(executable_record.get("source", "")).strip().lower()

        if source == "project_snapshot":
            return self._is_inside_path(executable_path, self.root_path)

        return executable_path.name.lower() == NGINX_EXECUTABLE_FILE_NAME_WINDOWS

    def _is_inside_path(self, target_path: Path, parent_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(parent_path.resolve())
            return True
        except ValueError:
            return False

    def _to_relative(self, target_path: Path) -> str:
        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
