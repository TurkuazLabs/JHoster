# 📄 Dosya Yolu: E:\JHoster\app\agent\services\stack_provisioning_service.py
# 📌 Amac: New Site stack secimini installer, web workflow ve database wizard planina donusturur
# 📌 Modul - Python
# Version: 3.77.0
# Aciklama: Quick App tarafindan secilen stack icin runtime/package hazirligi, web server profili ve MySQL wizard planini koordine eder
# Bagimli Oldugu Katman: Service

import re
from typing import Any

from config.constants import (
    INSTALLER_ROUTE_PREFIX,
    PACKAGE_DOWNLOAD_ROUTE_PREFIX,
    WEB_SERVER_PROFILE_ROUTE_PREFIX,
    WEB_SERVER_WORKFLOW_ROUTE_PREFIX,
)
from repositories.manifest_repository import ManifestRepository
from repositories.package_download_repository import PackageDownloadRepository
from repositories.stack_provisioning_config_repository import StackProvisioningConfigRepository
from tools.package_download_installer_tool import PackageDownloadInstallerTool
from tools.web_server_profile_tool import WebServerProfileTool


class StackProvisioningService:
    STATUS_READY = "ready"
    STATUS_ATTENTION = "attention"
    STATUS_SKIPPED = "skipped"
    INSTALLER_ACTIVE = "active"
    INSTALLER_AVAILABLE = "available"
    INSTALLER_UNAVAILABLE = "unavailable"
    INSTALLER_DISABLED = "disabled"
    STEP_RUNTIME = "runtime_installer"
    STEP_WEB_PACKAGE = "web_server_installer"
    STEP_MYSQL = "mysql_installer"
    STEP_PHP = "php_installer"
    STEP_MAILPIT = "mailpit_installer"
    STEP_PROFILE = "web_server_profile"
    STEP_WORKFLOW = "web_server_workflow"
    STEP_DATABASE = "database_wizard"

    def __init__(
        self,
        stack_config_repository: StackProvisioningConfigRepository,
        package_download_repository: PackageDownloadRepository,
        manifest_repository: ManifestRepository,
        package_download_installer_tool: PackageDownloadInstallerTool,
        web_server_profile_tool: WebServerProfileTool,
    ) -> None:
        self.stack_config_repository = stack_config_repository
        self.package_download_repository = package_download_repository
        self.manifest_repository = manifest_repository
        self.package_download_installer_tool = package_download_installer_tool
        self.web_server_profile_tool = web_server_profile_tool

    def build_plan(
        self,
        project_code: str,
        domain: str,
        port: int,
        runtime_family: str,
        stack_plan: dict[str, Any],
        active_runtime: dict[str, Any] | None,
    ) -> dict[str, Any]:
        config = self.stack_config_repository.get_config()
        web_server = str(stack_plan.get("web_server", "apache")).strip().lower() or "apache"
        package_map = self._get_mapping(config, "packages")
        runtime_component_map = self._get_mapping(config, "runtime_components")

        runtime_installer = self._build_runtime_installer(runtime_family, active_runtime, package_map, runtime_component_map)
        web_server_installer = self._build_package_installer(web_server, package_map.get(web_server))
        mysql_installer = self._build_optional_package_installer("mysql", bool(stack_plan.get("include_mysql", False)), package_map)
        php_installer = self._build_optional_package_installer("php", bool(stack_plan.get("include_php", False)), package_map, active_runtime if runtime_family == "php" else None)
        mailpit_installer = self._build_optional_package_installer("mailpit", bool(stack_plan.get("include_mailpit", False)), package_map)
        profile_plan = self.web_server_profile_tool.build_selection_plan(web_server)
        database_plan = self._build_database_plan(project_code, bool(stack_plan.get("include_mysql", False)), config)
        workflow_plan = self._build_workflow_plan(project_code, domain, port, web_server)

        installer_steps = [runtime_installer, web_server_installer, mysql_installer, php_installer, mailpit_installer]
        attention_required = any(self._requires_attention(step) for step in installer_steps) or not bool(profile_plan.get("safe", False))
        status = self.STATUS_ATTENTION if attention_required else self.STATUS_READY

        return {
            "success": True,
            "status": status,
            "project_code": project_code,
            "runtime_family": runtime_family,
            "web_server": web_server,
            "runtime_installer": runtime_installer,
            "service_installers": {
                "web_server": web_server_installer,
                "mysql": mysql_installer,
                "php": php_installer,
                "mailpit": mailpit_installer,
            },
            "web_server_profile": profile_plan,
            "web_server_workflow": workflow_plan,
            "database_wizard": database_plan,
            "ordered_steps": self._build_ordered_steps(runtime_installer, web_server_installer, mysql_installer, php_installer, mailpit_installer, profile_plan, workflow_plan, database_plan),
        }

    def _build_runtime_installer(
        self,
        runtime_family: str,
        active_runtime: dict[str, Any] | None,
        package_map: dict[str, str],
        runtime_component_map: dict[str, str],
    ) -> dict[str, Any]:
        normalized_family = str(runtime_family or "").strip().lower()
        if active_runtime is not None:
            return {
                "success": True,
                "status": self.INSTALLER_ACTIVE,
                "family": normalized_family,
                "required": False,
                "active_runtime": active_runtime,
            }

        package_code = package_map.get(normalized_family, "")
        if package_code:
            package_plan = self._build_package_installer(normalized_family, package_code)
            return {**package_plan, "required": True}

        component_code = runtime_component_map.get(normalized_family, "")
        manifest_item = self.manifest_repository.get_manifest_by_code(component_code) if component_code else None
        if manifest_item is not None:
            return {
                "success": True,
                "status": self.INSTALLER_AVAILABLE,
                "family": normalized_family,
                "required": True,
                "installer_type": "component_manifest",
                "component_code": component_code,
                "execute_route": f"{INSTALLER_ROUTE_PREFIX}/{component_code}/execute?dry_run=true",
            }

        return {
            "success": False,
            "status": self.INSTALLER_UNAVAILABLE,
            "family": normalized_family,
            "required": True,
            "reason": "runtime installer mapping not found",
        }

    def _build_optional_package_installer(
        self,
        family: str,
        enabled: bool,
        package_map: dict[str, str],
        active_runtime: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not enabled:
            return {
                "success": True,
                "status": self.STATUS_SKIPPED,
                "family": family,
                "required": False,
                "selected": False,
            }

        if active_runtime is not None:
            return {
                "success": True,
                "status": self.INSTALLER_ACTIVE,
                "family": family,
                "required": False,
                "selected": True,
                "active_runtime": active_runtime,
            }

        package_plan = self._build_package_installer(family, package_map.get(family, ""))
        return {**package_plan, "selected": True}

    def _build_package_installer(self, family: str, package_code: str | None) -> dict[str, Any]:
        normalized_code = str(package_code or "").strip()
        if not normalized_code:
            return {
                "success": False,
                "status": self.INSTALLER_UNAVAILABLE,
                "family": family,
                "required": True,
                "reason": "package mapping not found",
            }

        package = self.package_download_repository.get_package(normalized_code)
        if package is None:
            return {
                "success": False,
                "status": self.INSTALLER_UNAVAILABLE,
                "family": family,
                "package_code": normalized_code,
                "required": True,
                "reason": "package registry record not found",
            }

        plan = self.package_download_installer_tool.build_plan(package)
        enabled = bool(package.get("enabled", False))
        status = self.INSTALLER_AVAILABLE if enabled else self.INSTALLER_DISABLED
        return {
            "success": enabled,
            "status": status,
            "family": family,
            "required": True,
            "package_code": normalized_code,
            "package_plan": plan,
            "plan_route": f"{PACKAGE_DOWNLOAD_ROUTE_PREFIX}/{normalized_code}/plan",
            "download_route": f"{PACKAGE_DOWNLOAD_ROUTE_PREFIX}/{normalized_code}/download?dry_run=true",
            "install_route": f"{PACKAGE_DOWNLOAD_ROUTE_PREFIX}/{normalized_code}/install?dry_run=true",
        }

    def _build_database_plan(self, project_code: str, enabled: bool, config: dict[str, Any]) -> dict[str, Any]:
        if not enabled:
            return {
                "success": True,
                "status": self.STATUS_SKIPPED,
                "enabled": False,
                "label": "MySQL not selected",
            }

        database_config = config.get("database", {})
        database_config = database_config if isinstance(database_config, dict) else {}
        database_name = self._normalize_database_identifier(project_code)
        suffix = str(database_config.get("username_suffix", "_user"))
        username = self._normalize_database_identifier(f"{database_name}{suffix}")

        return {
            "success": True,
            "status": self.STATUS_READY,
            "enabled": True,
            "mode": "wizard_plan",
            "label": f"MySQL: {database_name}",
            "host": str(database_config.get("host", "127.0.0.1")),
            "port": int(database_config.get("port", 3306)),
            "database_name": database_name,
            "username": username,
            "charset": str(database_config.get("charset", "utf8mb4")),
            "collation": str(database_config.get("collation", "utf8mb4_unicode_ci")),
            "password_mode": str(database_config.get("password_mode", "prompt")),
            "password_required": True,
            "execute": False,
        }

    def _build_workflow_plan(self, project_code: str, domain: str, port: int, web_server: str) -> dict[str, Any]:
        return {
            "success": True,
            "status": self.STATUS_READY,
            "mode": "post_create_plan",
            "server_code": web_server,
            "project_code": project_code,
            "domain": str(domain or "").strip(),
            "port": int(port),
            "profile_plan_route": f"{WEB_SERVER_PROFILE_ROUTE_PREFIX}/{web_server}/plan",
            "profile_select_route": f"{WEB_SERVER_PROFILE_ROUTE_PREFIX}/{web_server}/select?dry_run=true",
            "workflow_plan_route": f"{WEB_SERVER_WORKFLOW_ROUTE_PREFIX}/{project_code}/plan",
            "workflow_run_route": f"{WEB_SERVER_WORKFLOW_ROUTE_PREFIX}/{project_code}/run?dry_run=true",
            "reload": True,
            "rollback_on_failure": True,
        }

    def _build_ordered_steps(
        self,
        runtime_installer: dict[str, Any],
        web_server_installer: dict[str, Any],
        mysql_installer: dict[str, Any],
        php_installer: dict[str, Any],
        mailpit_installer: dict[str, Any],
        profile_plan: dict[str, Any],
        workflow_plan: dict[str, Any],
        database_plan: dict[str, Any],
    ) -> list[dict[str, Any]]:
        return [
            {"step": self.STEP_RUNTIME, "status": runtime_installer.get("status")},
            {"step": self.STEP_WEB_PACKAGE, "status": web_server_installer.get("status")},
            {"step": self.STEP_MYSQL, "status": mysql_installer.get("status")},
            {"step": self.STEP_PHP, "status": php_installer.get("status")},
            {"step": self.STEP_MAILPIT, "status": mailpit_installer.get("status")},
            {"step": self.STEP_PROFILE, "status": self.STATUS_READY if profile_plan.get("safe", False) else self.STATUS_ATTENTION},
            {"step": self.STEP_WORKFLOW, "status": workflow_plan.get("status")},
            {"step": self.STEP_DATABASE, "status": database_plan.get("status")},
        ]

    def _requires_attention(self, step: dict[str, Any]) -> bool:
        if step.get("status") in {self.STATUS_SKIPPED, self.INSTALLER_ACTIVE, self.INSTALLER_AVAILABLE}:
            return False
        return bool(step.get("required", False) or step.get("selected", False))

    def _get_mapping(self, config: dict[str, Any], key: str) -> dict[str, str]:
        raw_mapping = config.get(key, {})
        if not isinstance(raw_mapping, dict):
            return {}
        return {str(item_key).strip().lower(): str(item_value).strip() for item_key, item_value in raw_mapping.items()}

    def _normalize_database_identifier(self, value: str) -> str:
        normalized = re.sub(r"[^a-zA-Z0-9_]", "_", str(value or "").strip().lower())
        normalized = re.sub(r"_+", "_", normalized).strip("_")
        return (normalized or "jhoster_site")[:64]
