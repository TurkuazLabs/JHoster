# 📄 Dosya Yolu: E:\JHoster\app\agent\services\nginx_executable_service.py
# 📌 Amac: Nginx executable tespit is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Detector tool ile registry repository arasindaki adapter tespit akisini koordine eder
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import NGINX_EXECUTABLE_STATUS_DETECTED
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from tools.nginx_executable_detector_tool import NginxExecutableDetectorTool


class NginxExecutableService:
    def __init__(
        self,
        nginx_executable_registry_repository: NginxExecutableRegistryRepository,
        nginx_executable_detector_tool: NginxExecutableDetectorTool,
    ) -> None:
        self.nginx_executable_registry_repository = nginx_executable_registry_repository
        self.nginx_executable_detector_tool = nginx_executable_detector_tool

    def list_detection_records(self) -> dict[str, Any]:
        detection_records = self.nginx_executable_registry_repository.list_detection_records()

        return {
            "success": True,
            "count": len(detection_records),
            "detection_records": detection_records,
        }

    def get_latest_detection(self) -> dict[str, Any]:
        detection_item = self.nginx_executable_registry_repository.get_latest_detection()

        if detection_item is None:
            return {
                "success": False,
                "error": "nginx_executable_detection_not_found",
            }

        return {
            "success": True,
            "detection_record": detection_item,
        }

    def plan_detection(self) -> dict[str, Any]:
        return self.detect_executable(dry_run=True)

    def detect_executable(self, dry_run: bool) -> dict[str, Any]:
        detection_result = self.nginx_executable_detector_tool.detect(dry_run=dry_run)

        if detection_result.get("status") == NGINX_EXECUTABLE_STATUS_DETECTED:
            stored_record = self.nginx_executable_registry_repository.append_detection_record(
                self._build_detection_record(detection_result)
            )
            detection_result["detection_record"] = stored_record

        return detection_result

    def _build_detection_record(self, detection_result: dict[str, Any]) -> dict[str, Any]:
        nginx_executable = detection_result.get("nginx_executable", {})
        plan = detection_result.get("plan", {})

        return {
            "status": detection_result.get("status"),
            "path": nginx_executable.get("path"),
            "path_absolute": nginx_executable.get("path_absolute"),
            "source": nginx_executable.get("source"),
            "version_status": nginx_executable.get("version_status"),
            "version_command_label": nginx_executable.get("version_command_label"),
            "validate_command_label": nginx_executable.get("validate_command_label"),
            "shell_execution": nginx_executable.get("shell_execution"),
            "real_nginx_execution": nginx_executable.get("real_nginx_execution"),
            "detection_mode": plan.get("detection_mode"),
            "detected_from": "nginx_executable_service",
            "detected_at": detection_result.get("detected_at"),
        }
