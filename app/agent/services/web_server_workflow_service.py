# 📄 Dosya Yolu: E:\JHoster\app\agent\services\web_server_workflow_service.py
# 📌 Amac: Active web server profiline gore unified generate, publish, validate, reload ve rollback akisini yonetir
# 📌 Modul - FileType
# Version: 1.3.0
# Aciklama: Nginx ve Apache servislerini tek workflow endpointi altinda sirali, geri alinabilir ve run_id ile izlenebilir sekilde koordine eder
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any
import uuid

from config.constants import (
    APACHE_REAL_VALIDATE_STATUS_VALID,
    NGINX_REAL_VALIDATE_STATUS_VALID,
    WEB_SERVER_CODE_APACHE,
    WEB_SERVER_CODE_NGINX,
    WEB_SERVER_PROFILE_DEFAULT,
    WEB_SERVER_PROFILE_STATUS_READY,
    WEB_SERVER_PROFILE_STATUS_SELECTED,
    WEB_SERVER_WORKFLOW_ERROR_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_STEP_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_RUN_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_LOCK_NOT_FOUND,
    WEB_SERVER_WORKFLOW_ERROR_UNSUPPORTED_PROFILE,
    WEB_SERVER_WORKFLOW_MESSAGE_COMPLETED,
    WEB_SERVER_WORKFLOW_MESSAGE_DRY_RUN,
    WEB_SERVER_WORKFLOW_MESSAGE_FAILED,
    WEB_SERVER_WORKFLOW_MESSAGE_RELOAD_SKIPPED,
    WEB_SERVER_WORKFLOW_REASON_APACHE_REAL_EXECUTION_REQUIRED,
    WEB_SERVER_WORKFLOW_RUN_ID_PREFIX,
    WEB_SERVER_WORKFLOW_SOURCE,
    WEB_SERVER_WORKFLOW_STATUS_COMPLETED,
    WEB_SERVER_WORKFLOW_STATUS_FAILED,
    WEB_SERVER_WORKFLOW_STATUS_PLANNED,
    WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
    WEB_SERVER_WORKFLOW_STEP_DEFERRED_MESSAGE,
    WEB_SERVER_WORKFLOW_STEP_GENERATE,
    WEB_SERVER_WORKFLOW_STEP_LOCK,
    WEB_SERVER_WORKFLOW_STEP_PROFILE,
    WEB_SERVER_WORKFLOW_STEP_PUBLISH,
    WEB_SERVER_WORKFLOW_STEP_REAL_VALIDATE,
    WEB_SERVER_WORKFLOW_STEP_RELOAD,
    WEB_SERVER_WORKFLOW_STEP_ROLLBACK,
    WEB_SERVER_WORKFLOW_STEP_VALIDATE,
)
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from repositories.web_server_workflow_lock_repository import WebServerWorkflowLockRepository
from repositories.web_server_workflow_registry_repository import WebServerWorkflowRegistryRepository
from services.apache_publish_service import ApachePublishService
from services.apache_real_reload_service import ApacheRealReloadService
from services.apache_real_validate_service import ApacheRealValidateService
from services.apache_validate_service import ApacheValidateService
from services.apache_vhost_service import ApacheVhostService
from services.nginx_publish_service import NginxPublishService
from services.nginx_real_reload_service import NginxRealReloadService
from services.nginx_real_validate_service import NginxRealValidateService
from services.nginx_reload_service import NginxReloadService
from services.nginx_validate_service import NginxValidateService
from services.virtual_host_service import VirtualHostService
from tools.project_path_tool import ProjectPathTool
from tools.web_server_profile_tool import WebServerProfileTool
from tools.web_server_workflow_rollback_tool import WebServerWorkflowRollbackTool


class WebServerWorkflowService:
    def __init__(
        self,
        web_server_profile_registry_repository: WebServerProfileRegistryRepository,
        web_server_workflow_registry_repository: WebServerWorkflowRegistryRepository,
        web_server_workflow_lock_repository: WebServerWorkflowLockRepository,
        web_server_profile_tool: WebServerProfileTool,
        project_path_tool: ProjectPathTool,
        web_server_workflow_rollback_tool: WebServerWorkflowRollbackTool,
        virtual_host_service: VirtualHostService,
        nginx_publish_service: NginxPublishService,
        nginx_validate_service: NginxValidateService,
        nginx_reload_service: NginxReloadService,
        nginx_real_validate_service: NginxRealValidateService,
        nginx_real_reload_service: NginxRealReloadService,
        apache_vhost_service: ApacheVhostService,
        apache_publish_service: ApachePublishService,
        apache_validate_service: ApacheValidateService,
        apache_real_validate_service: ApacheRealValidateService,
        apache_real_reload_service: ApacheRealReloadService,
    ) -> None:
        self.web_server_profile_registry_repository = web_server_profile_registry_repository
        self.web_server_workflow_registry_repository = web_server_workflow_registry_repository
        self.web_server_workflow_lock_repository = web_server_workflow_lock_repository
        self.web_server_profile_tool = web_server_profile_tool
        self.project_path_tool = project_path_tool
        self.web_server_workflow_rollback_tool = web_server_workflow_rollback_tool
        self.virtual_host_service = virtual_host_service
        self.nginx_publish_service = nginx_publish_service
        self.nginx_validate_service = nginx_validate_service
        self.nginx_reload_service = nginx_reload_service
        self.nginx_real_validate_service = nginx_real_validate_service
        self.nginx_real_reload_service = nginx_real_reload_service
        self.apache_vhost_service = apache_vhost_service
        self.apache_publish_service = apache_publish_service
        self.apache_validate_service = apache_validate_service
        self.apache_real_validate_service = apache_real_validate_service
        self.apache_real_reload_service = apache_real_reload_service

    def list_workflow_records(self) -> dict[str, Any]:
        workflow_records = self.web_server_workflow_registry_repository.list_records()

        return {
            "success": True,
            "count": len(workflow_records),
            "workflow_records": workflow_records,
        }

    def get_latest_workflow(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        workflow_record = self.web_server_workflow_registry_repository.get_latest_workflow(normalized_code)

        if workflow_record is None:
            return {
                "success": False,
                "project_code": normalized_code,
                "error": WEB_SERVER_WORKFLOW_ERROR_NOT_FOUND,
            }

        return {
            "success": True,
            "workflow_record": workflow_record,
        }

    def list_workflow_runs(self, project_code: str = "", status: str = "") -> dict[str, Any]:
        workflow_records = self.web_server_workflow_registry_repository.list_records()
        normalized_project_code = str(project_code).strip().lower()
        normalized_status = str(status).strip().lower()

        if normalized_project_code:
            workflow_records = [
                workflow_record
                for workflow_record in workflow_records
                if str(workflow_record.get("project_code", "")).strip().lower() == normalized_project_code
            ]

        if normalized_status:
            workflow_records = [
                workflow_record
                for workflow_record in workflow_records
                if str(workflow_record.get("status", "")).strip().lower() == normalized_status
            ]

        return {
            "success": True,
            "count": len(workflow_records),
            "project_code": normalized_project_code,
            "status_filter": normalized_status,
            "workflow_runs": workflow_records,
        }

    def list_project_workflow_runs(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        workflow_records = self.web_server_workflow_registry_repository.list_project_records(normalized_code)

        return {
            "success": True,
            "project_code": normalized_code,
            "count": len(workflow_records),
            "workflow_runs": workflow_records,
        }

    def get_workflow_run(self, run_id: str) -> dict[str, Any]:
        normalized_run_id = str(run_id).strip().lower()
        workflow_record = self.web_server_workflow_registry_repository.get_workflow_by_run_id(normalized_run_id)

        if workflow_record is None:
            return {
                "success": False,
                "run_id": normalized_run_id,
                "error": WEB_SERVER_WORKFLOW_ERROR_RUN_NOT_FOUND,
            }

        return {
            "success": True,
            "run_id": normalized_run_id,
            "workflow_run": workflow_record,
        }

    def list_workflow_locks(self) -> dict[str, Any]:
        workflow_locks = self.web_server_workflow_lock_repository.list_locks()

        return {
            "success": True,
            "count": len(workflow_locks),
            "workflow_locks": workflow_locks,
        }

    def get_project_workflow_lock(self, project_code: str) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        workflow_lock = self.web_server_workflow_lock_repository.get_project_lock(normalized_code)

        if workflow_lock is None:
            return {
                "success": False,
                "project_code": normalized_code,
                "error": WEB_SERVER_WORKFLOW_ERROR_LOCK_NOT_FOUND,
            }

        return {
            "success": True,
            "project_code": normalized_code,
            "workflow_lock": workflow_lock,
        }

    def unlock_project_workflow(self, project_code: str, run_id: str, force: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)

        return self.web_server_workflow_lock_repository.release_lock(
            project_code=normalized_code,
            run_id=run_id,
            force=force,
        )

    def plan_workflow(
        self,
        project_code: str,
        domain: str,
        port: int,
        target_dir: str,
        reload: bool,
        rollback_on_failure: bool,
    ) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        profile_record = self._get_current_profile_record()
        server_code = str(profile_record.get("server_code", WEB_SERVER_PROFILE_DEFAULT)).strip().lower()
        steps = [self._build_step(WEB_SERVER_WORKFLOW_STEP_PROFILE, True, profile_record)]

        if server_code not in [WEB_SERVER_CODE_NGINX, WEB_SERVER_CODE_APACHE]:
            return self._build_result(
                project_code=normalized_code,
                server_code=server_code,
                reload_requested=reload,
                allow_real_execution=False,
                rollback_on_failure=rollback_on_failure,
                status=WEB_SERVER_WORKFLOW_STATUS_FAILED,
                message=WEB_SERVER_WORKFLOW_MESSAGE_FAILED,
                steps=steps,
                error=WEB_SERVER_WORKFLOW_ERROR_UNSUPPORTED_PROFILE,
            )

        generate_result = self._generate_virtual_host(
            server_code=server_code,
            project_code=normalized_code,
            domain=domain,
            port=port,
            dry_run=True,
        )
        steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_GENERATE, generate_result.get("success", False), generate_result))

        if generate_result.get("success", False):
            steps.extend(self._build_deferred_steps(reload=reload, rollback_on_failure=rollback_on_failure))

        status = WEB_SERVER_WORKFLOW_STATUS_PLANNED if generate_result.get("success", False) else WEB_SERVER_WORKFLOW_STATUS_FAILED
        message = WEB_SERVER_WORKFLOW_MESSAGE_DRY_RUN if generate_result.get("success", False) else WEB_SERVER_WORKFLOW_MESSAGE_FAILED

        return self._build_result(
            project_code=normalized_code,
            server_code=server_code,
            reload_requested=reload,
            allow_real_execution=False,
            rollback_on_failure=rollback_on_failure,
            status=status,
            message=message,
            steps=steps,
            target_dir=target_dir,
        )

    def run_workflow(
        self,
        project_code: str,
        domain: str,
        port: int,
        target_dir: str,
        dry_run: bool,
        reload: bool,
        allow_real_execution: bool,
        rollback_on_failure: bool,
    ) -> dict[str, Any]:
        if dry_run:
            return self.plan_workflow(
                project_code=project_code,
                domain=domain,
                port=port,
                target_dir=target_dir,
                reload=reload,
                rollback_on_failure=rollback_on_failure,
            )

        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        profile_record = self._get_current_profile_record()
        server_code = str(profile_record.get("server_code", WEB_SERVER_PROFILE_DEFAULT)).strip().lower()
        workflow_run_id = self._build_run_id(normalized_code)
        steps = [self._build_step(WEB_SERVER_WORKFLOW_STEP_PROFILE, True, profile_record)]

        if server_code not in [WEB_SERVER_CODE_NGINX, WEB_SERVER_CODE_APACHE]:
            return self._finish_workflow(
                project_code=normalized_code,
                server_code=server_code,
                reload_requested=reload,
                allow_real_execution=allow_real_execution,
                rollback_on_failure=rollback_on_failure,
                status=WEB_SERVER_WORKFLOW_STATUS_FAILED,
                message=WEB_SERVER_WORKFLOW_MESSAGE_FAILED,
                steps=steps,
                target_dir=target_dir,
                error=WEB_SERVER_WORKFLOW_ERROR_UNSUPPORTED_PROFILE,
                run_id=workflow_run_id,
            )

        lock_result = self.web_server_workflow_lock_repository.acquire_lock(
            project_code=normalized_code,
            run_id=workflow_run_id,
            server_code=server_code,
        )
        steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_LOCK, lock_result.get("success", False), lock_result))

        if not lock_result.get("success", False):
            return self._finish_workflow(
                project_code=normalized_code,
                server_code=server_code,
                reload_requested=reload,
                allow_real_execution=allow_real_execution,
                rollback_on_failure=rollback_on_failure,
                status=WEB_SERVER_WORKFLOW_STATUS_FAILED,
                message=WEB_SERVER_WORKFLOW_MESSAGE_FAILED,
                steps=steps,
                target_dir=target_dir,
                error=str(lock_result.get("error", "")),
                run_id=workflow_run_id,
            )

        try:
            generate_result = self._generate_virtual_host(server_code, normalized_code, domain, port, dry_run=False)
            steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_GENERATE, generate_result.get("success", False), generate_result))
            if not generate_result.get("success", False):
                return self._finish_failed(
                    normalized_code,
                    server_code,
                    reload,
                    allow_real_execution,
                    rollback_on_failure,
                    steps,
                    target_dir,
                    workflow_run_id,
                )

            publish_result = self._publish_virtual_host(server_code, normalized_code, target_dir, dry_run=False)
            steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_PUBLISH, publish_result.get("success", False), publish_result))
            if not publish_result.get("success", False):
                return self._finish_failed(
                    normalized_code,
                    server_code,
                    reload,
                    allow_real_execution,
                    rollback_on_failure,
                    steps,
                    target_dir,
                    workflow_run_id,
                )

            validate_result = self._validate_config(server_code, normalized_code, dry_run=False)
            steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_VALIDATE, validate_result.get("success", False), validate_result))
            if not validate_result.get("success", False):
                self._append_rollback_step_if_requested(steps, server_code, publish_result, rollback_on_failure)
                return self._finish_failed(
                    normalized_code,
                    server_code,
                    reload,
                    allow_real_execution,
                    rollback_on_failure,
                    steps,
                    target_dir,
                    workflow_run_id,
                )

            if reload:
                self._append_reload_steps(
                    steps=steps,
                    server_code=server_code,
                    project_code=normalized_code,
                    allow_real_execution=allow_real_execution,
                )
                if self._has_failed_step_after_publish(steps):
                    self._append_rollback_step_if_requested(steps, server_code, publish_result, rollback_on_failure)

            has_failed_step = any(not bool(step.get("success")) for step in steps)
            final_status = WEB_SERVER_WORKFLOW_STATUS_FAILED if has_failed_step else WEB_SERVER_WORKFLOW_STATUS_COMPLETED
            final_message = WEB_SERVER_WORKFLOW_MESSAGE_FAILED if has_failed_step else WEB_SERVER_WORKFLOW_MESSAGE_COMPLETED

            return self._finish_workflow(
                project_code=normalized_code,
                server_code=server_code,
                reload_requested=reload,
                allow_real_execution=allow_real_execution,
                rollback_on_failure=rollback_on_failure,
                status=final_status,
                message=final_message,
                steps=steps,
                target_dir=target_dir,
                run_id=workflow_run_id,
            )
        finally:
            self.web_server_workflow_lock_repository.release_lock(
                project_code=normalized_code,
                run_id=workflow_run_id,
                force=False,
            )

    def rollback_latest_workflow(self, project_code: str, dry_run: bool) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        workflow_record = self.web_server_workflow_registry_repository.get_latest_workflow(normalized_code)

        if workflow_record is None:
            return {
                "success": False,
                "project_code": normalized_code,
                "error": WEB_SERVER_WORKFLOW_ERROR_NOT_FOUND,
            }

        publish_result = self._find_step_result(workflow_record, WEB_SERVER_WORKFLOW_STEP_PUBLISH)
        if not publish_result:
            return {
                "success": False,
                "project_code": normalized_code,
                "error": WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_STEP_NOT_FOUND,
            }

        server_code = str(workflow_record.get("web_server", WEB_SERVER_PROFILE_DEFAULT)).strip().lower()
        rollback_result = self.web_server_workflow_rollback_tool.rollback_publish_result(
            server_code=server_code,
            publish_result=publish_result,
            dry_run=dry_run,
        )
        steps = [self._build_step(WEB_SERVER_WORKFLOW_STEP_ROLLBACK, rollback_result.get("success", False), rollback_result)]
        status = WEB_SERVER_WORKFLOW_STATUS_PLANNED if dry_run else WEB_SERVER_WORKFLOW_STATUS_COMPLETED
        if not rollback_result.get("success", False):
            status = WEB_SERVER_WORKFLOW_STATUS_FAILED

        if dry_run:
            message = WEB_SERVER_WORKFLOW_MESSAGE_DRY_RUN
        elif rollback_result.get("success", False):
            message = WEB_SERVER_WORKFLOW_MESSAGE_COMPLETED
        else:
            message = WEB_SERVER_WORKFLOW_MESSAGE_FAILED

        if dry_run:
            return self._build_result(
                project_code=normalized_code,
                server_code=server_code,
                reload_requested=False,
                allow_real_execution=False,
                rollback_on_failure=False,
                status=status,
                message=message,
                steps=steps,
                target_dir=str(workflow_record.get("target_dir", "")),
            )

        return self._finish_workflow(
            project_code=normalized_code,
            server_code=server_code,
            reload_requested=False,
            allow_real_execution=False,
            rollback_on_failure=False,
            status=status,
            message=message,
            steps=steps,
            target_dir=str(workflow_record.get("target_dir", "")),
        )

    def _append_reload_steps(
        self,
        steps: list[dict[str, Any]],
        server_code: str,
        project_code: str,
        allow_real_execution: bool,
    ) -> None:
        if server_code == WEB_SERVER_CODE_NGINX and not allow_real_execution:
            reload_result = self.nginx_reload_service.reload_project_config(project_code=project_code, dry_run=False)
            steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_RELOAD, reload_result.get("success", False), reload_result))
            return

        if server_code == WEB_SERVER_CODE_APACHE and not allow_real_execution:
            steps.append(
                self._build_step(
                    WEB_SERVER_WORKFLOW_STEP_RELOAD,
                    True,
                    {
                        "success": True,
                        "status": WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
                        "message": WEB_SERVER_WORKFLOW_MESSAGE_RELOAD_SKIPPED,
                        "reason": WEB_SERVER_WORKFLOW_REASON_APACHE_REAL_EXECUTION_REQUIRED,
                    },
                )
            )
            return

        real_validate_result = self._real_validate_config(server_code, project_code, allow_real_execution)
        steps.append(
            self._build_step(
                WEB_SERVER_WORKFLOW_STEP_REAL_VALIDATE,
                real_validate_result.get("success", False),
                real_validate_result,
            )
        )

        if not real_validate_result.get("success", False):
            return

        validation_status = str(real_validate_result.get("status", "")).strip().lower()
        required_valid_status = (
            APACHE_REAL_VALIDATE_STATUS_VALID
            if server_code == WEB_SERVER_CODE_APACHE
            else NGINX_REAL_VALIDATE_STATUS_VALID
        )
        if validation_status != required_valid_status:
            steps.append(
                self._build_step(
                    WEB_SERVER_WORKFLOW_STEP_RELOAD,
                    False,
                    {
                        "success": False,
                        "status": WEB_SERVER_WORKFLOW_STATUS_SKIPPED,
                        "message": WEB_SERVER_WORKFLOW_MESSAGE_RELOAD_SKIPPED,
                        "validation_status": validation_status,
                    },
                )
            )
            return

        real_reload_result = self._real_reload_config(server_code, project_code, allow_real_execution)
        steps.append(
            self._build_step(
                WEB_SERVER_WORKFLOW_STEP_RELOAD,
                real_reload_result.get("success", False),
                real_reload_result,
            )
        )

    def _append_rollback_step_if_requested(
        self,
        steps: list[dict[str, Any]],
        server_code: str,
        publish_result: dict[str, Any],
        rollback_on_failure: bool,
    ) -> None:
        if not rollback_on_failure or self._has_step(steps, WEB_SERVER_WORKFLOW_STEP_ROLLBACK):
            return

        rollback_result = self.web_server_workflow_rollback_tool.rollback_publish_result(
            server_code=server_code,
            publish_result=publish_result,
            dry_run=False,
        )
        steps.append(self._build_step(WEB_SERVER_WORKFLOW_STEP_ROLLBACK, rollback_result.get("success", False), rollback_result))

    def _generate_virtual_host(
        self,
        server_code: str,
        project_code: str,
        domain: str,
        port: int,
        dry_run: bool,
    ) -> dict[str, Any]:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_vhost_service.generate_virtual_host(project_code, domain, port, dry_run)

        return self.virtual_host_service.generate_virtual_host(project_code, domain, port, dry_run)

    def _publish_virtual_host(
        self,
        server_code: str,
        project_code: str,
        target_dir: str,
        dry_run: bool,
    ) -> dict[str, Any]:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_publish_service.publish_project_vhost(project_code, target_dir, dry_run)

        return self.nginx_publish_service.publish_project_vhost(project_code, target_dir, dry_run)

    def _validate_config(self, server_code: str, project_code: str, dry_run: bool) -> dict[str, Any]:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_validate_service.validate_project_config(project_code, dry_run)

        return self.nginx_validate_service.validate_project_config(project_code, dry_run)

    def _real_validate_config(self, server_code: str, project_code: str, allow_real_execution: bool) -> dict[str, Any]:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_real_validate_service.validate_with_real_adapter(
                project_code=project_code,
                dry_run=False,
                allow_real_execution=allow_real_execution,
            )

        return self.nginx_real_validate_service.validate_with_real_adapter(
            project_code=project_code,
            dry_run=False,
            allow_real_execution=allow_real_execution,
        )

    def _real_reload_config(self, server_code: str, project_code: str, allow_real_execution: bool) -> dict[str, Any]:
        if server_code == WEB_SERVER_CODE_APACHE:
            return self.apache_real_reload_service.reload_with_real_adapter(
                project_code=project_code,
                dry_run=False,
                allow_real_execution=allow_real_execution,
            )

        return self.nginx_real_reload_service.reload_with_real_adapter(
            project_code=project_code,
            dry_run=False,
            allow_real_execution=allow_real_execution,
        )

    def _build_deferred_steps(self, reload: bool, rollback_on_failure: bool) -> list[dict[str, Any]]:
        step_names = [WEB_SERVER_WORKFLOW_STEP_PUBLISH, WEB_SERVER_WORKFLOW_STEP_VALIDATE]
        if reload:
            step_names.append(WEB_SERVER_WORKFLOW_STEP_RELOAD)
        if rollback_on_failure:
            step_names.append(WEB_SERVER_WORKFLOW_STEP_ROLLBACK)

        return [
            self._build_step(
                step_name,
                True,
                {
                    "success": True,
                    "status": WEB_SERVER_WORKFLOW_STATUS_PLANNED,
                    "message": WEB_SERVER_WORKFLOW_STEP_DEFERRED_MESSAGE,
                },
            )
            for step_name in step_names
        ]

    def _build_step(self, name: str, success: bool, result: dict[str, Any]) -> dict[str, Any]:
        return {
            "name": name,
            "success": bool(success),
            "status": result.get("status", WEB_SERVER_WORKFLOW_STATUS_COMPLETED if success else WEB_SERVER_WORKFLOW_STATUS_FAILED),
            "message": result.get("message", ""),
            "result": result,
        }

    def _finish_failed(
        self,
        project_code: str,
        server_code: str,
        reload_requested: bool,
        allow_real_execution: bool,
        rollback_on_failure: bool,
        steps: list[dict[str, Any]],
        target_dir: str,
        run_id: str = "",
    ) -> dict[str, Any]:
        return self._finish_workflow(
            project_code=project_code,
            server_code=server_code,
            reload_requested=reload_requested,
            allow_real_execution=allow_real_execution,
            rollback_on_failure=rollback_on_failure,
            status=WEB_SERVER_WORKFLOW_STATUS_FAILED,
            message=WEB_SERVER_WORKFLOW_MESSAGE_FAILED,
            steps=steps,
            target_dir=target_dir,
            run_id=run_id,
        )

    def _finish_workflow(
        self,
        project_code: str,
        server_code: str,
        reload_requested: bool,
        allow_real_execution: bool,
        rollback_on_failure: bool,
        status: str,
        message: str,
        steps: list[dict[str, Any]],
        target_dir: str,
        error: str = "",
        run_id: str = "",
    ) -> dict[str, Any]:
        workflow = self._build_result(
            project_code=project_code,
            server_code=server_code,
            reload_requested=reload_requested,
            allow_real_execution=allow_real_execution,
            rollback_on_failure=rollback_on_failure,
            status=status,
            message=message,
            steps=steps,
            target_dir=target_dir,
            error=error,
            run_id=run_id,
        )
        stored_record = self.web_server_workflow_registry_repository.append_record(workflow.get("workflow", {}))
        workflow["workflow_record"] = stored_record

        return workflow

    def _build_result(
        self,
        project_code: str,
        server_code: str,
        reload_requested: bool,
        allow_real_execution: bool,
        rollback_on_failure: bool,
        status: str,
        message: str,
        steps: list[dict[str, Any]],
        target_dir: str = "",
        error: str = "",
        run_id: str = "",
    ) -> dict[str, Any]:
        finished_at = datetime.now(timezone.utc).isoformat()
        workflow_run_id = run_id or self._build_run_id(project_code)
        normalized_steps = self._build_workflow_step_log(steps, finished_at)
        workflow = {
            "run_id": workflow_run_id,
            "project_code": project_code,
            "web_server": server_code,
            "status": status,
            "message": message,
            "reload_requested": reload_requested,
            "allow_real_execution": allow_real_execution,
            "rollback_on_failure": rollback_on_failure,
            "target_dir": target_dir,
            "steps": normalized_steps,
            "step_count": len(normalized_steps),
            "workflow_from": WEB_SERVER_WORKFLOW_SOURCE,
            "started_at": finished_at,
            "finished_at": finished_at,
        }

        if error:
            workflow["error"] = error

        return {
            "success": status in [WEB_SERVER_WORKFLOW_STATUS_PLANNED, WEB_SERVER_WORKFLOW_STATUS_COMPLETED],
            "status": status,
            "message": message,
            "run_id": workflow_run_id,
            "workflow": workflow,
        }

    def _build_run_id(self, project_code: str) -> str:
        normalized_code = str(project_code).strip().lower().replace("_", "-") or "unknown"
        return f"{WEB_SERVER_WORKFLOW_RUN_ID_PREFIX}-{normalized_code}-{uuid.uuid4().hex[:12]}"

    def _build_workflow_step_log(self, steps: list[dict[str, Any]], finished_at: str) -> list[dict[str, Any]]:
        step_log = []

        for step_index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                continue

            step_log.append(
                {
                    **step,
                    "step_index": step.get("step_index", step_index),
                    "recorded_at": step.get("recorded_at", finished_at),
                }
            )

        return step_log

    def _has_failed_step_after_publish(self, steps: list[dict[str, Any]]) -> bool:
        publish_seen = False

        for step in steps:
            if step.get("name") == WEB_SERVER_WORKFLOW_STEP_PUBLISH:
                publish_seen = True
                continue

            if publish_seen and step.get("name") != WEB_SERVER_WORKFLOW_STEP_ROLLBACK and not bool(step.get("success")):
                return True

        return False

    def _has_step(self, steps: list[dict[str, Any]], step_name: str) -> bool:
        return any(step.get("name") == step_name for step in steps)

    def _find_step_result(self, workflow_record: dict[str, Any], step_name: str) -> dict[str, Any] | None:
        steps = workflow_record.get("steps", [])

        if not isinstance(steps, list):
            return None

        for step in steps:
            if not isinstance(step, dict):
                continue
            if step.get("name") == step_name and isinstance(step.get("result"), dict):
                return step.get("result")

        return None

    def _get_current_profile_record(self) -> dict[str, Any]:
        current_record = self.web_server_profile_registry_repository.get_current_profile()

        if current_record is not None:
            return current_record

        default_profile = self.web_server_profile_tool.get_profile(WEB_SERVER_PROFILE_DEFAULT) or {}

        return {
            "server_code": WEB_SERVER_PROFILE_DEFAULT,
            "server_name": default_profile.get("name", WEB_SERVER_PROFILE_DEFAULT),
            "profile_status": default_profile.get("status", WEB_SERVER_PROFILE_STATUS_READY),
            "adapter_stage": default_profile.get("adapter_stage"),
            "default": True,
            "status": WEB_SERVER_PROFILE_STATUS_SELECTED,
            "selected_from": "web_server_workflow_service_default",
        }
