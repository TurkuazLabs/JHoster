# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\web_server_workflow_controller.py
# 📌 Amac: Unified web server workflow ve rollback ve lock HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.3.0
# Aciklama: Controller sadece request alir; workflow run listesi, lock listesi, run detayi, plan, run, rollback ve unlock isteklerini service katmanina aktarir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import (
    WEB_SERVER_WORKFLOW_ROUTE_PREFIX,
    WEB_SERVER_WORKFLOW_ROUTE_TAG,
    VIRTUAL_HOST_DEFAULT_PORT,
)
from config.settings import AppSettings
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_real_reload_registry_repository import ApacheRealReloadRegistryRepository
from repositories.apache_real_validate_registry_repository import ApacheRealValidateRegistryRepository
from repositories.apache_validate_registry_repository import ApacheValidateRegistryRepository
from repositories.apache_vhost_registry_repository import ApacheVhostRegistryRepository
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from repositories.nginx_real_reload_registry_repository import NginxRealReloadRegistryRepository
from repositories.nginx_real_validate_registry_repository import NginxRealValidateRegistryRepository
from repositories.nginx_reload_registry_repository import NginxReloadRegistryRepository
from repositories.nginx_validate_registry_repository import NginxValidateRegistryRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
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
from services.web_server_workflow_service import WebServerWorkflowService
from tools.apache_config_publisher_tool import ApacheConfigPublisherTool
from tools.apache_config_validator_tool import ApacheConfigValidatorTool
from tools.apache_real_reloader_tool import ApacheRealReloaderTool
from tools.apache_real_validator_tool import ApacheRealValidatorTool
from tools.apache_vhost_config_tool import ApacheVhostConfigTool
from tools.nginx_config_publisher_tool import NginxConfigPublisherTool
from tools.nginx_config_validator_tool import NginxConfigValidatorTool
from tools.nginx_real_reloader_tool import NginxRealReloaderTool
from tools.nginx_real_validator_tool import NginxRealValidatorTool
from tools.nginx_reload_tool import NginxReloadTool
from tools.project_path_tool import ProjectPathTool
from tools.virtual_host_config_tool import VirtualHostConfigTool
from tools.web_server_profile_tool import WebServerProfileTool
from tools.web_server_workflow_rollback_tool import WebServerWorkflowRollbackTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=WEB_SERVER_WORKFLOW_ROUTE_PREFIX, tags=[WEB_SERVER_WORKFLOW_ROUTE_TAG])

settings = AppSettings.load()
project_path_tool = ProjectPathTool(settings.root_path)
project_registry_repository = ProjectRegistryRepository(settings.storage_path)
virtual_host_registry_repository = VirtualHostRegistryRepository(settings.storage_path)
apache_vhost_registry_repository = ApacheVhostRegistryRepository(settings.storage_path)
nginx_publish_registry_repository = NginxPublishRegistryRepository(settings.storage_path)
nginx_validate_registry_repository = NginxValidateRegistryRepository(settings.storage_path)
apache_publish_registry_repository = ApachePublishRegistryRepository(settings.storage_path)
apache_validate_registry_repository = ApacheValidateRegistryRepository(settings.storage_path)

web_server_workflow_service = WebServerWorkflowService(
    web_server_profile_registry_repository=WebServerProfileRegistryRepository(settings.storage_path),
    web_server_workflow_registry_repository=WebServerWorkflowRegistryRepository(settings.storage_path),
    web_server_workflow_lock_repository=WebServerWorkflowLockRepository(settings.storage_path),
    web_server_profile_tool=WebServerProfileTool(settings.root_path),
    project_path_tool=project_path_tool,
    web_server_workflow_rollback_tool=WebServerWorkflowRollbackTool(settings.root_path),
    virtual_host_service=VirtualHostService(
        project_registry_repository=project_registry_repository,
        virtual_host_registry_repository=virtual_host_registry_repository,
        project_path_tool=project_path_tool,
        virtual_host_config_tool=VirtualHostConfigTool(settings.root_path),
    ),
    nginx_publish_service=NginxPublishService(
        root_path=settings.root_path,
        virtual_host_registry_repository=virtual_host_registry_repository,
        nginx_publish_registry_repository=nginx_publish_registry_repository,
        project_path_tool=project_path_tool,
        nginx_config_publisher_tool=NginxConfigPublisherTool(settings.root_path),
    ),
    nginx_validate_service=NginxValidateService(
        root_path=settings.root_path,
        nginx_publish_registry_repository=nginx_publish_registry_repository,
        nginx_validate_registry_repository=nginx_validate_registry_repository,
        project_path_tool=project_path_tool,
        nginx_config_validator_tool=NginxConfigValidatorTool(settings.root_path),
    ),
    nginx_reload_service=NginxReloadService(
        root_path=settings.root_path,
        nginx_validate_registry_repository=nginx_validate_registry_repository,
        nginx_reload_registry_repository=NginxReloadRegistryRepository(settings.storage_path),
        project_path_tool=project_path_tool,
        nginx_reload_tool=NginxReloadTool(settings.root_path),
    ),
    nginx_real_validate_service=NginxRealValidateService(
        root_path=settings.root_path,
        nginx_publish_registry_repository=nginx_publish_registry_repository,
        nginx_executable_registry_repository=NginxExecutableRegistryRepository(settings.storage_path),
        nginx_real_validate_registry_repository=NginxRealValidateRegistryRepository(settings.storage_path),
        project_path_tool=project_path_tool,
        nginx_real_validator_tool=NginxRealValidatorTool(settings.root_path),
    ),
    nginx_real_reload_service=NginxRealReloadService(
        root_path=settings.root_path,
        nginx_publish_registry_repository=nginx_publish_registry_repository,
        nginx_executable_registry_repository=NginxExecutableRegistryRepository(settings.storage_path),
        nginx_real_validate_registry_repository=NginxRealValidateRegistryRepository(settings.storage_path),
        nginx_real_reload_registry_repository=NginxRealReloadRegistryRepository(settings.storage_path),
        project_path_tool=project_path_tool,
        nginx_real_reloader_tool=NginxRealReloaderTool(settings.root_path),
    ),
    apache_vhost_service=ApacheVhostService(
        project_registry_repository=project_registry_repository,
        apache_vhost_registry_repository=apache_vhost_registry_repository,
        project_path_tool=project_path_tool,
        apache_vhost_config_tool=ApacheVhostConfigTool(settings.root_path),
    ),
    apache_publish_service=ApachePublishService(
        root_path=settings.root_path,
        apache_vhost_registry_repository=apache_vhost_registry_repository,
        apache_publish_registry_repository=apache_publish_registry_repository,
        project_path_tool=project_path_tool,
        apache_config_publisher_tool=ApacheConfigPublisherTool(settings.root_path),
    ),
    apache_validate_service=ApacheValidateService(
        root_path=settings.root_path,
        apache_publish_registry_repository=apache_publish_registry_repository,
        apache_validate_registry_repository=apache_validate_registry_repository,
        project_path_tool=project_path_tool,
        apache_config_validator_tool=ApacheConfigValidatorTool(settings.root_path),
    ),
    apache_real_validate_service=ApacheRealValidateService(
        root_path=settings.root_path,
        apache_publish_registry_repository=apache_publish_registry_repository,
        apache_executable_registry_repository=ApacheExecutableRegistryRepository(settings.storage_path),
        apache_real_validate_registry_repository=ApacheRealValidateRegistryRepository(settings.storage_path),
        project_path_tool=project_path_tool,
        apache_real_validator_tool=ApacheRealValidatorTool(settings.root_path),
    ),
    apache_real_reload_service=ApacheRealReloadService(
        root_path=settings.root_path,
        apache_publish_registry_repository=apache_publish_registry_repository,
        apache_executable_registry_repository=ApacheExecutableRegistryRepository(settings.storage_path),
        apache_real_validate_registry_repository=ApacheRealValidateRegistryRepository(settings.storage_path),
        apache_real_reload_registry_repository=ApacheRealReloadRegistryRepository(settings.storage_path),
        project_path_tool=project_path_tool,
        apache_real_reloader_tool=ApacheRealReloaderTool(settings.root_path),
    ),
)
api_response_view = ApiResponseView()


@router.get("")
def list_workflow_records() -> dict:
    return api_response_view.render(web_server_workflow_service.list_workflow_records())


@router.get("/runs")
def list_workflow_runs(
    project_code: str = Query(default=""),
    status: str = Query(default=""),
) -> dict:
    return api_response_view.render(
        web_server_workflow_service.list_workflow_runs(
            project_code=project_code,
            status=status,
        )
    )


@router.get("/runs/{run_id}")
def get_workflow_run(run_id: str) -> dict:
    return api_response_view.render(web_server_workflow_service.get_workflow_run(run_id))


@router.get("/locks")
def list_workflow_locks() -> dict:
    return api_response_view.render(web_server_workflow_service.list_workflow_locks())


@router.get("/{project_code}/runs")
def list_project_workflow_runs(project_code: str) -> dict:
    return api_response_view.render(web_server_workflow_service.list_project_workflow_runs(project_code))


@router.get("/{project_code}/lock")
def get_project_workflow_lock(project_code: str) -> dict:
    return api_response_view.render(web_server_workflow_service.get_project_workflow_lock(project_code))


@router.post("/{project_code}/unlock")
def unlock_project_workflow(
    project_code: str,
    run_id: str = Query(default=""),
    force: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        web_server_workflow_service.unlock_project_workflow(
            project_code=project_code,
            run_id=run_id,
            force=force,
        )
    )


@router.get("/{project_code}")
def get_latest_workflow(project_code: str) -> dict:
    return api_response_view.render(web_server_workflow_service.get_latest_workflow(project_code))


@router.get("/{project_code}/plan")
def plan_workflow(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=VIRTUAL_HOST_DEFAULT_PORT),
    target_dir: str = Query(default=""),
    reload: bool = Query(default=True),
    rollback_on_failure: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        web_server_workflow_service.plan_workflow(
            project_code=project_code,
            domain=domain,
            port=port,
            target_dir=target_dir,
            reload=reload,
            rollback_on_failure=rollback_on_failure,
        )
    )


@router.post("/{project_code}/run")
def run_workflow(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=VIRTUAL_HOST_DEFAULT_PORT),
    target_dir: str = Query(default=""),
    dry_run: bool = Query(default=True),
    reload: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
    rollback_on_failure: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        web_server_workflow_service.run_workflow(
            project_code=project_code,
            domain=domain,
            port=port,
            target_dir=target_dir,
            dry_run=dry_run,
            reload=reload,
            allow_real_execution=allow_real_execution,
            rollback_on_failure=rollback_on_failure,
        )
    )


@router.post("/{project_code}/rollback")
def rollback_latest_workflow(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        web_server_workflow_service.rollback_latest_workflow(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
