# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\action_executor_tool.py
# 📌 Amac: Manifest action adimlarini guvenli sekilde planlar veya uygular
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Checksum, guvenli zip extract ve riskli download/shell bloklama tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import (
    ACTION_ALGORITHM_KEY,
    ACTION_CHECKSUM_KEY,
    ACTION_COMMAND_KEY,
    ACTION_CONTENT_KEY,
    ACTION_MAX_BYTES_KEY,
    ACTION_NAME_KEY,
    ACTION_SOURCE_KEY,
    ACTION_STATUS_BLOCKED,
    ACTION_STATUS_FAILED,
    ACTION_STATUS_OK,
    ACTION_STATUS_PLANNED,
    ACTION_STATUS_SKIPPED,
    ACTION_TARGET_KEY,
    ACTION_TYPE_CHECK,
    ACTION_TYPE_DOWNLOAD,
    ACTION_TYPE_ENSURE_DIRECTORY,
    ACTION_TYPE_EXTRACT,
    ACTION_TYPE_KEY,
    ACTION_TYPE_VERIFY_CHECKSUM,
    ACTION_TYPE_WRITE_FILE,
    CHECKSUM_ALGORITHM_SHA256,
)
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.safe_path_tool import SafePathTool


class ActionExecutorTool:
    def __init__(
        self,
        safe_path_tool: SafePathTool,
        checksum_tool: ChecksumTool,
        archive_extract_tool: ArchiveExtractTool,
        allow_shell_commands: bool,
        allow_external_downloads: bool,
        allow_safe_extract: bool,
    ) -> None:
        self.safe_path_tool = safe_path_tool
        self.checksum_tool = checksum_tool
        self.archive_extract_tool = archive_extract_tool
        self.allow_shell_commands = allow_shell_commands
        self.allow_external_downloads = allow_external_downloads
        self.allow_safe_extract = allow_safe_extract

    def execute_actions(self, actions: list[dict[str, Any]], dry_run: bool) -> list[dict[str, Any]]:
        execution_results: list[dict[str, Any]] = []

        for index, action in enumerate(actions, start=1):
            execution_results.append(self._execute_single_action(index, action, dry_run))

        return execution_results

    def _execute_single_action(self, index: int, action: dict[str, Any], dry_run: bool) -> dict[str, Any]:
        action_type = str(action.get(ACTION_TYPE_KEY, "")).strip()
        action_name = str(action.get(ACTION_NAME_KEY, f"action_{index}")).strip()

        base_result = {
            "index": index,
            "name": action_name,
            "type": action_type,
        }

        if dry_run:
            return {
                **base_result,
                "status": ACTION_STATUS_PLANNED,
                "message": "dry run only",
            }

        try:
            if action_type == ACTION_TYPE_CHECK:
                return self._execute_check(base_result, action)

            if action_type == ACTION_TYPE_ENSURE_DIRECTORY:
                return self._execute_ensure_directory(base_result, action)

            if action_type == ACTION_TYPE_WRITE_FILE:
                return self._execute_write_file(base_result, action)

            if action_type == ACTION_TYPE_VERIFY_CHECKSUM:
                return self._execute_verify_checksum(base_result, action)

            if action_type == ACTION_TYPE_EXTRACT:
                return self._execute_extract(base_result, action)

            if action_type == ACTION_TYPE_DOWNLOAD:
                return self._execute_download(base_result)

            return {
                **base_result,
                "status": ACTION_STATUS_SKIPPED,
                "message": "unsupported action type",
            }
        except Exception as error:
            return {
                **base_result,
                "status": ACTION_STATUS_FAILED,
                "message": str(error),
            }

    def _execute_check(self, base_result: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        command_value = str(action.get(ACTION_COMMAND_KEY, "")).strip()

        if command_value and not self.allow_shell_commands:
            return {
                **base_result,
                "status": ACTION_STATUS_BLOCKED,
                "message": "shell command blocked",
            }

        return {
            **base_result,
            "status": ACTION_STATUS_OK,
            "message": "check completed",
        }

    def _execute_ensure_directory(self, base_result: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        target_path = self.safe_path_tool.resolve_inside_root(action.get(ACTION_TARGET_KEY))
        target_path.mkdir(parents=True, exist_ok=True)

        return {
            **base_result,
            "status": ACTION_STATUS_OK,
            "message": "directory ready",
            "target": self._format_path(target_path),
        }

    def _execute_write_file(self, base_result: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        target_path = self.safe_path_tool.resolve_inside_root(action.get(ACTION_TARGET_KEY))
        content = str(action.get(ACTION_CONTENT_KEY, ""))
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(content, encoding="utf-8")

        return {
            **base_result,
            "status": ACTION_STATUS_OK,
            "message": "file written",
            "target": self._format_path(target_path),
        }

    def _execute_verify_checksum(self, base_result: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        source_path = self.safe_path_tool.resolve_inside_root(action.get(ACTION_SOURCE_KEY))
        algorithm = str(action.get(ACTION_ALGORITHM_KEY, CHECKSUM_ALGORITHM_SHA256)).strip().lower()
        expected_checksum = str(action.get(ACTION_CHECKSUM_KEY, "")).strip()

        if not expected_checksum:
            return {
                **base_result,
                "status": ACTION_STATUS_BLOCKED,
                "message": "checksum missing",
            }

        verification_result = self.checksum_tool.verify(source_path, expected_checksum, algorithm)

        if not verification_result["valid"]:
            return {
                **base_result,
                "status": ACTION_STATUS_FAILED,
                "message": "checksum mismatch",
                "source": self._format_path(source_path),
                "checksum": verification_result,
            }

        return {
            **base_result,
            "status": ACTION_STATUS_OK,
            "message": "checksum valid",
            "source": self._format_path(source_path),
            "checksum": verification_result,
        }

    def _execute_extract(self, base_result: dict[str, Any], action: dict[str, Any]) -> dict[str, Any]:
        if not self.allow_safe_extract:
            return {
                **base_result,
                "status": ACTION_STATUS_BLOCKED,
                "message": "safe extract disabled",
            }

        source_path = self.safe_path_tool.resolve_inside_root(action.get(ACTION_SOURCE_KEY))
        target_path = self.safe_path_tool.resolve_inside_root(action.get(ACTION_TARGET_KEY))
        algorithm = str(action.get(ACTION_ALGORITHM_KEY, CHECKSUM_ALGORITHM_SHA256)).strip().lower()
        expected_checksum = str(action.get(ACTION_CHECKSUM_KEY, "")).strip()
        max_bytes = int(action.get(ACTION_MAX_BYTES_KEY, 104857600))

        if not expected_checksum:
            return {
                **base_result,
                "status": ACTION_STATUS_BLOCKED,
                "message": "extract checksum required",
            }

        verification_result = self.checksum_tool.verify(source_path, expected_checksum, algorithm)
        if not verification_result["valid"]:
            return {
                **base_result,
                "status": ACTION_STATUS_FAILED,
                "message": "checksum mismatch before extract",
                "source": self._format_path(source_path),
                "checksum": verification_result,
            }

        extract_result = self.archive_extract_tool.extract_zip(source_path, target_path, max_bytes)

        return {
            **base_result,
            "status": ACTION_STATUS_OK,
            "message": "archive extracted",
            "extract": extract_result,
        }

    def _execute_download(self, base_result: dict[str, Any]) -> dict[str, Any]:
        if not self.allow_external_downloads:
            return {
                **base_result,
                "status": ACTION_STATUS_BLOCKED,
                "message": "external download blocked",
            }

        return {
            **base_result,
            "status": ACTION_STATUS_SKIPPED,
            "message": "download action is disabled here; use package download service",
        }

    def _format_path(self, file_path: Path) -> str:
        return str(file_path).replace("/", "\\")
