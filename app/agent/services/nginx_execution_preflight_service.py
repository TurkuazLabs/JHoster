# 📄 Dosya Yolu: E:\JHoster\app\agent\services\nginx_execution_preflight_service.py
# 📌 Amac: Nginx real execution preflight is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Publish kaydi, executable kaydi ve preflight tool arasindaki akisi koordine eder
# Bagimli Oldugu Katman: Service

from pathlib import Path
from typing import Any

from config.constants import (
    NGINX_EXECUTION_PREFLIGHT_ERROR_EXECUTABLE_NOT_FOUND,
    NGINX_EXECUTION_PREFLIGHT_ERROR_PUBLISH_NOT_FOUND,
    NGINX_EXECUTION_PREFLIGHT_ERROR_TARGET_NOT_FOUND,
    NGINX_EXECUTION_PREFLIGHT_STATUS_BLOCKED,
    NGINX_EXECUTION_PREFLIGHT_STATUS_READY,
)
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from repositories.nginx_execution_preflight_registry_repository import NginxExecutionPreflightRegistryRepository
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from tools.nginx_execution_preflight_tool import NginxExecutionPreflightTool
from tools.project_path_tool import ProjectPathTool


class NginxExecutionPreflightService:
    def __init__(
        self,
        root_path: Path,
        nginx_publish_registry_repository: NginxPublishRegistryRepository,
        nginx_executable_registry_repository: NginxExecutableRegistryRepository,
        nginx_execution_preflight_registry_repository: NginxExecutionPreflightRegistryRepository,
        project_path_tool: ProjectPathTool,
        nginx_execution_preflight_tool: NginxExecutionPreflightTool,
    ) -> None:
        self.root_path = root_path.resolve()
        self.nginx_publish_registry_repository = nginx_publish_registry_repository
        self.nginx_executable_registry_repository = nginx_executable_registry_repository
        self.nginx_execution_preflight_registry_repository = nginx_execution_preflight_registry_repository
        self.project_path_tool = project_path_tool
        self.nginx_execution_preflight_tool = nginx_execution_preflight_tool

    def list_preflight_records(self) -> dict[str, Any]:
        preflight_records = self.nginx_execution_preflight_registry_repository.list_preflight_records()

        return {
            "success": True,
            "count": len(preflight_records),
            "preflight_records": preflight_records,
        }

    def get_latest_preflight(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        preflight_item = self.nginx_execution_preflight_registry_repository.get_latest_preflight(normalized_code)

        if preflight_item is None:
            return {
                "success": False,
                "error": NGINX_EXECUTION_PREFLIGHT_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        return {
            "success": True,
            "preflight_record": preflight_item,
        }

    def plan_preflight(self, project_code: str) -> dict[str, Any]:
        return self.run_preflight(project_code=project_code, dry_run=True)

    def run_preflight(self, project_code: str, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        published_item = self.nginx_publish_registry_repository.get_latest_publish(normalized_code)

        if published_item is None:
            return {
                "success": False,
                "error": NGINX_EXECUTION_PREFLIGHT_ERROR_PUBLISH_NOT_FOUND,
                "project_code": normalized_code,
            }

        executable_record = self.nginx_executable_registry_repository.get_latest_detection()
        if executable_record is None:
            return {
                "success": False,
                "error": NGINX_EXECUTION_PREFLIGHT_ERROR_EXECUTABLE_NOT_FOUND,
                "project_code": normalized_code,
            }

        target_config_file = self._resolve_target_config_file(published_item)
        if not target_config_file.is_file():
            return {
                "success": False,
                "error": NGINX_EXECUTION_PREFLIGHT_ERROR_TARGET_NOT_FOUND,
                "project_code": normalized_code,
                "expected_file": str(target_config_file),
            }

        preflight_result = self.nginx_execution_preflight_tool.run_preflight(
            project_code=normalized_code,
            published_config_file=target_config_file,
            executable_record=executable_record,
            dry_run=dry_run,
        )

        if preflight_result.get("status") in [
            NGINX_EXECUTION_PREFLIGHT_STATUS_READY,
            NGINX_EXECUTION_PREFLIGHT_STATUS_BLOCKED,
        ]:
            stored_record = self.nginx_execution_preflight_registry_repository.append_preflight_record(
                self._build_preflight_record(
                    published_item=published_item,
                    executable_record=executable_record,
                    preflight_result=preflight_result,
                )
            )
            preflight_result["preflight_record"] = stored_record

        return preflight_result

    def _resolve_target_config_file(self, published_item: dict[str, Any]) -> Path:
        raw_target_file = str(published_item.get("target_file", "")).strip()
        normalized_target_file = raw_target_file.replace("\\", "/")
        target_file_path = Path(normalized_target_file)

        if target_file_path.is_absolute():
            return target_file_path.resolve()

        return (self.root_path / target_file_path).resolve()

    def _build_preflight_record(
        self,
        published_item: dict[str, Any],
        executable_record: dict[str, Any],
        preflight_result: dict[str, Any],
    ) -> dict[str, Any]:
        plan = preflight_result.get("plan", {})
        preflight_execution_result = preflight_result.get("preflight_result", {})

        return {
            "project_code": published_item.get("project_code"),
            "project_name": published_item.get("project_name"),
            "domain": published_item.get("domain"),
            "port": published_item.get("port"),
            "published_config_file": plan.get("published_config_file"),
            "main_config_file": plan.get("main_config_file"),
            "nginx_executable_file": plan.get("nginx_executable_file"),
            "nginx_executable_source": executable_record.get("source"),
            "preflight_mode": plan.get("preflight_mode"),
            "path_safe": plan.get("path_safe"),
            "real_execution_ready": plan.get("real_execution_ready"),
            "blocking_reasons": plan.get("blocking_reasons", []),
            "shell_execution": plan.get("shell_execution"),
            "real_nginx_execution": preflight_execution_result.get("real_nginx_execution", plan.get("real_nginx_execution")),
            "status": preflight_result.get("status"),
            "preflighted_from": "nginx_execution_preflight_service",
            "preflighted_at": preflight_result.get("preflighted_at"),
        }
