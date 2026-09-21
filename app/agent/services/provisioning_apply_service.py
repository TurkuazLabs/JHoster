# 📄 Dosya Yolu: E:\JHoster\app\agent\services\provisioning_apply_service.py
# 📌 Amac: New Site provisioning planini kullanici onayli gercek apply zincirine donusturur
# 📌 Modul - Python
# Version: 3.78.0
# Aciklama: Package hazirligi, runtime aktivasyonu, site create, web profile/workflow ve MySQL create adimlarini sirali koordine eder
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any
import uuid

from repositories.app_registry_repository import AppRegistryRepository
from repositories.provisioning_apply_registry_repository import ProvisioningApplyRegistryRepository
from services.package_download_service import PackageDownloadService
from services.quick_app_service import QuickAppService
from services.runtime_version_service import RuntimeVersionService
from services.web_server_profile_service import WebServerProfileService
from services.web_server_workflow_service import WebServerWorkflowService
from tools.mysql_database_tool import MysqlDatabaseTool


class ProvisioningApplyService:
    STATUS_PLANNED = "planned"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_REJECTED = "rejected"

    def __init__(
        self,
        quick_app_service: QuickAppService,
        package_download_service: PackageDownloadService,
        runtime_version_service: RuntimeVersionService,
        web_server_profile_service: WebServerProfileService,
        web_server_workflow_service: WebServerWorkflowService,
        app_registry_repository: AppRegistryRepository,
        apply_registry_repository: ProvisioningApplyRegistryRepository,
        mysql_database_tool: MysqlDatabaseTool,
    ) -> None:
        self.quick_app_service = quick_app_service
        self.package_download_service = package_download_service
        self.runtime_version_service = runtime_version_service
        self.web_server_profile_service = web_server_profile_service
        self.web_server_workflow_service = web_server_workflow_service
        self.app_registry_repository = app_registry_repository
        self.apply_registry_repository = apply_registry_repository
        self.mysql_database_tool = mysql_database_tool

    def list_records(self) -> dict[str, Any]:
        records = self.apply_registry_repository.list_records()
        return {"success": True, "count": len(records), "records": records}

    def get_latest_record(self, project_code: str) -> dict[str, Any]:
        record = self.apply_registry_repository.get_latest_record(project_code)
        return {"success": record is not None, "project_code": str(project_code).strip().lower(), "record": record}

    def plan_apply(
        self,
        project_code: str,
        project_name: str,
        template_code: str,
        domain: str,
        port: int,
        web_server: str,
        include_mysql: bool,
        include_php: bool,
        include_mailpit: bool,
        mysql_admin_user: str = "root",
    ) -> dict[str, Any]:
        quick_plan = self.quick_app_service.plan_app(
            project_code,
            project_name,
            template_code,
            domain,
            port,
            web_server,
            include_mysql,
            include_php,
            include_mailpit,
        )
        if not quick_plan.get("success", False):
            return {
                "success": False,
                "status": self.STATUS_FAILED,
                "error": quick_plan.get("error", "quick_app_plan_failed"),
                "quick_app_plan": quick_plan,
            }

        provisioning_plan = quick_plan.get("provisioning_plan", {})
        database_plan = provisioning_plan.get("database_wizard", {}) if isinstance(provisioning_plan, dict) else {}
        mysql_plan: dict[str, Any] | None = None
        if bool(database_plan.get("enabled", False)):
            mysql_plan = self.mysql_database_tool.build_plan(
                database_name=str(database_plan.get("database_name", "")),
                host=str(database_plan.get("host", "127.0.0.1")),
                port=int(database_plan.get("port", 3306)),
                admin_user=mysql_admin_user,
            )

        package_steps = self._build_package_steps(provisioning_plan)
        blockers = self._collect_plan_blockers(package_steps, mysql_plan)
        return {
            "success": True,
            "status": self.STATUS_PLANNED,
            "project_code": quick_plan.get("project_code"),
            "approved_required": True,
            "real_execution_default": False,
            "quick_app_plan": quick_plan,
            "provisioning_plan": provisioning_plan,
            "package_steps": package_steps,
            "mysql_preflight": mysql_plan,
            "blockers": blockers,
            "ready_for_apply": len(blockers) == 0,
            "ordered_steps": [
                "package_prepare",
                "runtime_activate",
                "quick_app_create",
                "web_server_profile_select",
                "web_server_workflow_run",
                "mysql_database_create",
            ],
        }

    def apply(
        self,
        project_code: str,
        project_name: str,
        template_code: str,
        domain: str,
        port: int,
        web_server: str,
        include_mysql: bool,
        include_php: bool,
        include_mailpit: bool,
        dry_run: bool,
        approved: bool,
        allow_real_execution: bool,
        target_dir: str,
        mysql_admin_user: str,
        mysql_admin_password: str,
    ) -> dict[str, Any]:
        plan = self.plan_apply(
            project_code,
            project_name,
            template_code,
            domain,
            port,
            web_server,
            include_mysql,
            include_php,
            include_mailpit,
            mysql_admin_user,
        )
        if not plan.get("success", False):
            return plan
        if dry_run:
            return plan
        if not approved:
            return {
                **plan,
                "success": False,
                "status": self.STATUS_REJECTED,
                "error": "provisioning_apply_approval_required",
            }

        database_plan = plan.get("provisioning_plan", {}).get("database_wizard", {})
        if bool(database_plan.get("enabled", False)) and not str(mysql_admin_password or ""):
            return {
                **plan,
                "success": False,
                "status": self.STATUS_REJECTED,
                "error": "mysql_admin_password_required",
            }
        if plan.get("blockers"):
            return {
                **plan,
                "success": False,
                "status": self.STATUS_REJECTED,
                "error": "provisioning_apply_preflight_blocked",
            }

        run_id = f"provisioning-{str(project_code).strip().lower()}-{uuid.uuid4().hex[:12]}"
        steps: list[dict[str, Any]] = []

        package_result = self._apply_packages(plan.get("package_steps", []))
        steps.append(self._step("package_prepare", package_result))
        if not package_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, package_result.get("error", "package_prepare_failed"))

        runtime_result = self._ensure_runtime_active(plan)
        steps.append(self._step("runtime_activate", runtime_result))
        if not runtime_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, runtime_result.get("error", "runtime_activate_failed"))

        create_result = self.quick_app_service.create_app(
            project_code,
            project_name,
            template_code,
            domain,
            port,
            False,
            web_server,
            include_mysql,
            include_php,
            include_mailpit,
        )
        steps.append(self._step("quick_app_create", create_result))
        if not create_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, create_result.get("error", "quick_app_create_failed"))

        profile_result = self.web_server_profile_service.select_profile(web_server, dry_run=False)
        steps.append(self._step("web_server_profile_select", profile_result))
        if not profile_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, profile_result.get("error", "profile_select_failed"))

        workflow_result = self.web_server_workflow_service.run_workflow(
            project_code=project_code,
            domain=domain,
            port=port,
            target_dir=target_dir,
            dry_run=False,
            reload=True,
            allow_real_execution=allow_real_execution,
            rollback_on_failure=True,
        )
        steps.append(self._step("web_server_workflow_run", workflow_result))
        if not workflow_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, workflow_result.get("error", "web_server_workflow_failed"))

        if bool(database_plan.get("enabled", False)):
            mysql_result = self.mysql_database_tool.create_database(
                database_name=str(database_plan.get("database_name", "")),
                host=str(database_plan.get("host", "127.0.0.1")),
                port=int(database_plan.get("port", 3306)),
                admin_user=mysql_admin_user,
                admin_password=mysql_admin_password,
                approved=True,
                dry_run=False,
            )
        else:
            mysql_result = {"success": True, "status": "skipped", "message": "mysql not selected"}
        steps.append(self._step("mysql_database_create", mysql_result))
        if not mysql_result.get("success", False):
            return self._finish(run_id, project_code, self.STATUS_FAILED, steps, mysql_result.get("error", "mysql_database_create_failed"))

        return self._finish(run_id, project_code, self.STATUS_COMPLETED, steps)

    def _build_package_steps(self, provisioning_plan: dict[str, Any]) -> list[dict[str, Any]]:
        if not isinstance(provisioning_plan, dict):
            return []
        raw_steps = [provisioning_plan.get("runtime_installer", {})]
        service_installers = provisioning_plan.get("service_installers", {})
        if isinstance(service_installers, dict):
            raw_steps.extend(service_installers.values())

        steps: list[dict[str, Any]] = []
        seen: set[str] = set()
        for item in raw_steps:
            if not isinstance(item, dict):
                continue
            family = str(item.get("family", "")).strip().lower()
            package_code = str(item.get("package_code", "")).strip()
            key = package_code or family
            if not key or key in seen:
                continue
            seen.add(key)
            steps.append({
                "family": family,
                "package_code": package_code,
                "status": item.get("status"),
                "required": bool(item.get("required", False)),
                "selected": bool(item.get("selected", item.get("required", False))),
                "already_installed": self._is_family_installed(family),
            })
        return steps

    def _collect_plan_blockers(self, package_steps: list[dict[str, Any]], mysql_plan: dict[str, Any] | None) -> list[str]:
        blockers: list[str] = []
        for step in package_steps:
            if step.get("already_installed", False):
                continue
            status = str(step.get("status", ""))
            if status in {"disabled", "unavailable"} and (step.get("required") or step.get("selected")):
                blockers.append(f"package_not_ready:{step.get('family') or step.get('package_code')}")
        if mysql_plan is not None:
            if not mysql_plan.get("identifier_valid", False):
                blockers.append("mysql_database_name_invalid")
            if not mysql_plan.get("shell_execution_allowed", False):
                blockers.append("mysql_shell_execution_disabled")
            if not mysql_plan.get("mysql_executable_found", False):
                mysql_package = next((step for step in package_steps if step.get("family") == "mysql"), None)
                package_can_prepare = bool(
                    mysql_package
                    and not mysql_package.get("already_installed", False)
                    and str(mysql_package.get("status", "")) == "available"
                )
                if not package_can_prepare:
                    blockers.append("mysql_executable_not_found")
        return blockers

    def _apply_packages(self, package_steps: list[dict[str, Any]]) -> dict[str, Any]:
        results: list[dict[str, Any]] = []
        for step in package_steps:
            if step.get("already_installed", False) or str(step.get("status", "")) in {"active", "skipped"}:
                results.append({**step, "success": True, "action": "reuse"})
                continue
            package_code = str(step.get("package_code", "")).strip()
            if not package_code:
                if step.get("required") or step.get("selected"):
                    return {"success": False, "error": "package_code_missing", "results": results}
                continue
            download = self.package_download_service.download_package(package_code, dry_run=False)
            results.append({"family": step.get("family"), "package_code": package_code, "action": "download", "result": download})
            if not download.get("success", False):
                return {"success": False, "error": download.get("error", "package_download_failed"), "results": results}
            install = self.package_download_service.install_package(package_code, dry_run=False)
            results.append({"family": step.get("family"), "package_code": package_code, "action": "install", "result": install})
            if not install.get("success", False):
                return {"success": False, "error": install.get("error", "package_install_failed"), "results": results}
        return {"success": True, "status": "completed", "results": results}

    def _ensure_runtime_active(self, plan: dict[str, Any]) -> dict[str, Any]:
        quick_plan = plan.get("quick_app_plan", {})
        runtime_family = str(quick_plan.get("runtime_family", "")).strip().lower()
        if not runtime_family:
            return {"success": True, "status": "skipped", "message": "runtime family not required"}
        current = self.runtime_version_service.get_active_version(runtime_family)
        if current.get("active") is not None:
            return {"success": True, "status": "active", "active": current.get("active")}

        family_app = self.app_registry_repository.get_app(runtime_family)
        if family_app is not None:
            activated = self.runtime_version_service.activate_runtime_version(runtime_family, dry_run=False)
            if activated.get("success", False):
                return activated

        for step in plan.get("package_steps", []):
            if str(step.get("family", "")).strip().lower() != runtime_family:
                continue
            package_code = str(step.get("package_code", "")).strip()
            if package_code:
                activated = self.runtime_version_service.activate_runtime_version(package_code, dry_run=False)
                if activated.get("success", False):
                    return activated
        return {"success": False, "error": "active_runtime_not_found_after_package_prepare", "family": runtime_family}

    def _is_family_installed(self, family: str) -> bool:
        normalized = str(family or "").strip().lower()
        if not normalized:
            return False
        app = self.app_registry_repository.get_app(normalized)
        return app is not None and str(app.get("status", "installed")).strip().lower() == "installed"

    def _step(self, name: str, result: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": name,
            "success": bool(result.get("success", False)),
            "status": result.get("status", "completed" if result.get("success", False) else "failed"),
            "result": self._sanitize_result(result),
        }

    def _finish(self, run_id: str, project_code: str, status: str, steps: list[dict[str, Any]], error: str = "") -> dict[str, Any]:
        payload = {
            "run_id": run_id,
            "project_code": str(project_code).strip().lower(),
            "status": status,
            "success": status == self.STATUS_COMPLETED,
            "steps": steps,
            "step_count": len(steps),
            "error": str(error or ""),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        stored = self.apply_registry_repository.append_record(payload)
        return {**payload, "record": stored}

    def _sanitize_result(self, result: dict[str, Any]) -> dict[str, Any]:
        sanitized = dict(result)
        for key in list(sanitized):
            if "password" in str(key).lower():
                sanitized.pop(key, None)
        return sanitized
