# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\nginx_executable_detector_tool.py
# 📌 Amac: Nginx executable dosyasini guvenli sekilde tespit eder ve adapter planini uretir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Env, snapshot ve standart Windows path adaylarini shell calistirmadan tarar
# Bagimli Oldugu Katman: Tool

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import os

from config.constants import (
    NGINX_EXECUTABLE_ENV_PATH,
    NGINX_EXECUTABLE_FILE_NAME_WINDOWS,
    NGINX_EXECUTABLE_MESSAGE_DETECTED,
    NGINX_EXECUTABLE_MESSAGE_DRY_RUN,
    NGINX_EXECUTABLE_MESSAGE_NOT_FOUND,
    NGINX_EXECUTABLE_MODE_SAFE_SCAN,
    NGINX_EXECUTABLE_SOURCE_ENV,
    NGINX_EXECUTABLE_SOURCE_PROJECT,
    NGINX_EXECUTABLE_SOURCE_STANDARD,
    NGINX_EXECUTABLE_STANDARD_WINDOWS_PATHS,
    NGINX_EXECUTABLE_STATUS_DETECTED,
    NGINX_EXECUTABLE_STATUS_NOT_FOUND,
    NGINX_EXECUTABLE_STATUS_PLANNED,
    NGINX_EXECUTABLE_VALIDATE_COMMAND_LABEL,
    NGINX_EXECUTABLE_VERSION_COMMAND_LABEL,
    SNAPSHOT_DIRECTORY_NAME,
)


class NginxExecutableDetectorTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.snapshot_nginx_path = (
            self.root_path
            / SNAPSHOT_DIRECTORY_NAME
            / "nginx"
            / "bin"
            / NGINX_EXECUTABLE_FILE_NAME_WINDOWS
        ).resolve()

    def build_detection_plan(self) -> dict[str, Any]:
        candidates = self._build_candidates()
        detected_candidates = [candidate for candidate in candidates if candidate.get("exists") is True]
        selected_candidate = detected_candidates[0] if detected_candidates else None

        return {
            "detection_mode": NGINX_EXECUTABLE_MODE_SAFE_SCAN,
            "env_key": NGINX_EXECUTABLE_ENV_PATH,
            "candidates": candidates,
            "detected": selected_candidate is not None,
            "selected_candidate": selected_candidate,
            "version_command_label": NGINX_EXECUTABLE_VERSION_COMMAND_LABEL,
            "validate_command_label": NGINX_EXECUTABLE_VALIDATE_COMMAND_LABEL,
            "shell_execution": False,
            "real_nginx_execution": False,
            "safe": True,
            "planned_at": self._now(),
        }

    def detect(self, dry_run: bool) -> dict[str, Any]:
        plan = self.build_detection_plan()

        if dry_run:
            return {
                "success": True,
                "status": NGINX_EXECUTABLE_STATUS_PLANNED,
                "message": NGINX_EXECUTABLE_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        if not plan.get("detected", False):
            return {
                "success": False,
                "status": NGINX_EXECUTABLE_STATUS_NOT_FOUND,
                "message": NGINX_EXECUTABLE_MESSAGE_NOT_FOUND,
                "plan": plan,
                "detected_at": self._now(),
            }

        return {
            "success": True,
            "status": NGINX_EXECUTABLE_STATUS_DETECTED,
            "message": NGINX_EXECUTABLE_MESSAGE_DETECTED,
            "plan": plan,
            "detected_at": self._now(),
            "nginx_executable": self._build_detection_payload(plan),
        }

    def _build_candidates(self) -> list[dict[str, Any]]:
        candidates: list[dict[str, Any]] = []
        env_path = os.getenv(NGINX_EXECUTABLE_ENV_PATH, "").strip()

        if env_path:
            candidates.append(self._build_candidate(env_path, NGINX_EXECUTABLE_SOURCE_ENV))

        candidates.append(
            self._build_candidate(
                str(self.snapshot_nginx_path),
                NGINX_EXECUTABLE_SOURCE_PROJECT,
            )
        )

        for standard_path in NGINX_EXECUTABLE_STANDARD_WINDOWS_PATHS:
            candidates.append(self._build_candidate(standard_path, NGINX_EXECUTABLE_SOURCE_STANDARD))

        return candidates

    def _build_candidate(self, raw_path: str, source: str) -> dict[str, Any]:
        candidate_path = Path(raw_path)
        resolved_path = candidate_path.resolve() if not self._is_windows_absolute_on_non_windows(raw_path) else candidate_path
        file_name = candidate_path.name.lower()
        exists = candidate_path.is_file() if not self._is_windows_absolute_on_non_windows(raw_path) else False
        name_is_safe = file_name == NGINX_EXECUTABLE_FILE_NAME_WINDOWS
        project_path_safe = self._is_inside_path(resolved_path, self.root_path) if exists else source != NGINX_EXECUTABLE_SOURCE_PROJECT

        return {
            "source": source,
            "path": raw_path,
            "path_absolute": str(resolved_path),
            "exists": exists,
            "file_name": candidate_path.name,
            "name_is_safe": name_is_safe,
            "project_path_safe": project_path_safe,
            "safe": name_is_safe and project_path_safe,
        }

    def _build_detection_payload(self, plan: dict[str, Any]) -> dict[str, Any]:
        selected_candidate = plan.get("selected_candidate") or {}

        return {
            "path": selected_candidate.get("path"),
            "path_absolute": selected_candidate.get("path_absolute"),
            "source": selected_candidate.get("source"),
            "version_status": "not_executed",
            "version_command_label": plan.get("version_command_label"),
            "validate_command_label": plan.get("validate_command_label"),
            "shell_execution": False,
            "real_nginx_execution": False,
        }

    def _is_inside_path(self, target_path: Path, parent_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(parent_path.resolve())
            return True
        except ValueError:
            return False

    def _is_windows_absolute_on_non_windows(self, raw_path: str) -> bool:
        normalized_path = raw_path.strip()

        return os.name != "nt" and len(normalized_path) > 2 and normalized_path[1:3] in (":\\", ":/")

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()
