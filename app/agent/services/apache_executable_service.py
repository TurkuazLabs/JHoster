# 📄 Dosya Yolu: E:\JHoster\app\agent\services\apache_executable_service.py
# 📌 Amac: Apache executable tespit is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Detector tool ile registry repository arasindaki adapter tespit akisini koordine eder
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import APACHE_EXECUTABLE_STATUS_DETECTED
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from tools.apache_executable_detector_tool import ApacheExecutableDetectorTool


class ApacheExecutableService:
    def __init__(
        self,
        apache_executable_registry_repository: ApacheExecutableRegistryRepository,
        apache_executable_detector_tool: ApacheExecutableDetectorTool,
    ) -> None:
        self.apache_executable_registry_repository = apache_executable_registry_repository
        self.apache_executable_detector_tool = apache_executable_detector_tool

    def list_detection_records(self) -> dict[str, Any]:
        detection_records = self.apache_executable_registry_repository.list_detection_records()

        return {
            "success": True,
            "count": len(detection_records),
            "detection_records": detection_records,
        }

    def get_latest_detection(self) -> dict[str, Any]:
        detection_item = self.apache_executable_registry_repository.get_latest_detection()

        if detection_item is None:
            return {
                "success": False,
                "error": "apache_executable_detection_not_found",
            }

        return {
            "success": True,
            "detection_record": detection_item,
        }

    def plan_detection(self) -> dict[str, Any]:
        return self.detect_executable(dry_run=True)

    def detect_executable(self, dry_run: bool) -> dict[str, Any]:
        detection_result = self.apache_executable_detector_tool.detect(dry_run=dry_run)

        if detection_result.get("status") == APACHE_EXECUTABLE_STATUS_DETECTED:
            stored_record = self.apache_executable_registry_repository.append_detection_record(
                self._build_detection_record(detection_result)
            )
            detection_result["detection_record"] = stored_record

        return detection_result

    def _build_detection_record(self, detection_result: dict[str, Any]) -> dict[str, Any]:
        apache_executable = detection_result.get("apache_executable", {})
        plan = detection_result.get("plan", {})

        return {
            "status": detection_result.get("status"),
            "path": apache_executable.get("path"),
            "path_absolute": apache_executable.get("path_absolute"),
            "source": apache_executable.get("source"),
            "version_status": apache_executable.get("version_status"),
            "version_command_label": apache_executable.get("version_command_label"),
            "validate_command_label": apache_executable.get("validate_command_label"),
            "shell_execution": apache_executable.get("shell_execution"),
            "real_apache_execution": apache_executable.get("real_apache_execution"),
            "detection_mode": plan.get("detection_mode"),
            "detected_from": "apache_executable_service",
            "detected_at": detection_result.get("detected_at"),
        }
