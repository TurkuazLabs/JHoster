# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\apache_real_validator_tool.py
# 📌 Amac: Tespit edilmis httpd.exe ile httpd -t real validate adapter planini ve izinli calistirmayi yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Shell kullanmadan executable, main config ve vhost path guvenligi kontrolu yapar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os
import subprocess

from config.constants import (
    APACHE_EXECUTABLE_FILE_NAME_WINDOWS,
    APACHE_PUBLISHED_DIRECTORY_NAME,
    APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS,
    APACHE_REAL_VALIDATE_ENV_MAIN_CONFIG,
    APACHE_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME,
    APACHE_REAL_VALIDATE_MESSAGE_DRY_RUN,
    APACHE_REAL_VALIDATE_MESSAGE_INVALID,
    APACHE_REAL_VALIDATE_MESSAGE_REJECTED,
    APACHE_REAL_VALIDATE_MESSAGE_SKIPPED,
    APACHE_REAL_VALIDATE_MESSAGE_VALID,
    APACHE_REAL_VALIDATE_MODE_REAL_ADAPTER,
    APACHE_REAL_VALIDATE_STATUS_INVALID,
    APACHE_REAL_VALIDATE_STATUS_PLANNED,
    APACHE_REAL_VALIDATE_STATUS_REJECTED,
    APACHE_REAL_VALIDATE_STATUS_SKIPPED,
    APACHE_REAL_VALIDATE_STATUS_VALID,
    APACHE_VHOST_EXTENSION,
    SNAPSHOT_DIRECTORY_NAME,
    VIRTUAL_HOSTS_DIRECTORY_NAME,
)


class ApacheRealValidatorTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.publish_root_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / VIRTUAL_HOSTS_DIRECTORY_NAME / APACHE_PUBLISHED_DIRECTORY_NAME
        ).resolve()
        self.default_main_config_path = (
            self.root_path / SNAPSHOT_DIRECTORY_NAME / "apache" / "conf" / APACHE_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME
        ).resolve()

    def build_real_validation_plan(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
        allow_real_execution: bool,
    ) -> dict[str, Any]:
        normalized_project_code = str(project_code).strip().lower()
        target_path = published_config_file.resolve()
        executable_path = self._resolve_path(str(executable_record.get("path_absolute") or executable_record.get("path") or ""))
        main_config_path = self._resolve_main_config_path()

        target_exists = target_path.is_file()
        target_is_safe = self._is_inside_path(target_path, self.publish_root_path)
        target_extension_is_safe = target_path.suffix == APACHE_VHOST_EXTENSION

        executable_exists = executable_path.is_file()
        executable_name_is_safe = executable_path.name.lower() == APACHE_EXECUTABLE_FILE_NAME_WINDOWS
        executable_is_safe = executable_name_is_safe and self._is_allowed_executable_path(
            executable_path=executable_path,
            executable_record=executable_record,
        )

        main_config_exists = main_config_path.is_file()
        main_config_name_is_safe = main_config_path.name.lower() == APACHE_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME
        main_config_is_safe = main_config_name_is_safe and self._is_allowed_config_path(main_config_path)

        path_safe = (
            target_exists
            and target_is_safe
            and target_extension_is_safe
            and executable_exists
            and executable_is_safe
            and main_config_exists
            and main_config_is_safe
        )

        command = [
            str(executable_path),
            "-t",
            "-f",
            str(main_config_path),
        ]

        return {
            "project_code": normalized_project_code,
            "published_config_file": self._to_relative(target_path),
            "published_config_file_absolute": str(target_path),
            "main_config_file": self._to_relative(main_config_path),
            "main_config_file_absolute": str(main_config_path),
            "apache_executable_file": str(executable_path),
            "apache_executable_file_absolute": str(executable_path),
            "target_exists": target_exists,
            "target_is_safe": target_is_safe,
            "target_extension_is_safe": target_extension_is_safe,
            "executable_exists": executable_exists,
            "executable_name_is_safe": executable_name_is_safe,
            "executable_is_safe": executable_is_safe,
            "main_config_exists": main_config_exists,
            "main_config_name_is_safe": main_config_name_is_safe,
            "main_config_is_safe": main_config_is_safe,
            "validation_mode": APACHE_REAL_VALIDATE_MODE_REAL_ADAPTER,
            "command_label": "httpd -t -f <main httpd.conf>",
            "command": command,
            "shell_execution": False,
            "real_apache_execution_requested": bool(allow_real_execution),
            "real_apache_execution": bool(allow_real_execution) and path_safe,
            "path_safe": path_safe,
            "safe": path_safe,
            "planned_at": self._now(),
        }

    def validate_with_real_adapter(
        self,
        project_code: str,
        published_config_file: Path,
        executable_record: dict[str, Any],
        dry_run: bool,
        allow_real_execution: bool,
    ) -> dict[str, Any]:
        plan = self.build_real_validation_plan(
            project_code=project_code,
            published_config_file=published_config_file,
            executable_record=executable_record,
            allow_real_execution=allow_real_execution,
        )

        if not plan["safe"]:
            return {
                "success": False,
                "status": APACHE_REAL_VALIDATE_STATUS_REJECTED,
                "message": APACHE_REAL_VALIDATE_MESSAGE_REJECTED,
                "plan": plan,
            }

        if dry_run:
            return {
                "success": True,
                "status": APACHE_REAL_VALIDATE_STATUS_PLANNED,
                "message": APACHE_REAL_VALIDATE_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        if not allow_real_execution:
            validated_at = self._now()
            return {
                "success": True,
                "status": APACHE_REAL_VALIDATE_STATUS_SKIPPED,
                "message": APACHE_REAL_VALIDATE_MESSAGE_SKIPPED,
                "plan": plan,
                "execution_result": {
                    "real_apache_execution": False,
                    "shell_execution": False,
                    "reason": "allow_real_execution is false",
                },
                "validated_at": validated_at,
            }

        execution_result = self._execute_validation(plan["command"])
        status = APACHE_REAL_VALIDATE_STATUS_VALID if execution_result.get("return_code") == 0 else APACHE_REAL_VALIDATE_STATUS_INVALID
        message = APACHE_REAL_VALIDATE_MESSAGE_VALID if status == APACHE_REAL_VALIDATE_STATUS_VALID else APACHE_REAL_VALIDATE_MESSAGE_INVALID

        return {
            "success": status == APACHE_REAL_VALIDATE_STATUS_VALID,
            "status": status,
            "message": message,
            "plan": plan,
            "execution_result": execution_result,
            "validated_at": self._now(),
        }

    def _execute_validation(self, command: list[str]) -> dict[str, Any]:
        try:
            completed_process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS,
                shell=False,
            )

            return {
                "real_apache_execution": True,
                "shell_execution": False,
                "return_code": completed_process.returncode,
                "stdout": completed_process.stdout.strip(),
                "stderr": completed_process.stderr.strip(),
                "timeout_seconds": APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS,
            }
        except subprocess.TimeoutExpired as exc:
            return {
                "real_apache_execution": True,
                "shell_execution": False,
                "return_code": -1,
                "stdout": str(exc.stdout or "").strip(),
                "stderr": "apache validate command timeout",
                "timeout_seconds": APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS,
            }
        except OSError as exc:
            return {
                "real_apache_execution": True,
                "shell_execution": False,
                "return_code": -1,
                "stdout": "",
                "stderr": str(exc),
                "timeout_seconds": APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS,
            }

    def _resolve_main_config_path(self) -> Path:
        env_main_config = os.getenv(APACHE_REAL_VALIDATE_ENV_MAIN_CONFIG, "").strip()
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

        return executable_path.name.lower() == APACHE_EXECUTABLE_FILE_NAME_WINDOWS

    def _is_allowed_config_path(self, config_path: Path) -> bool:
        if self._is_inside_path(config_path, self.root_path):
            return True

        return config_path.name.lower() == APACHE_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME

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
