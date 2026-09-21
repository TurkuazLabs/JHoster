# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\provisioning_apply_controller.py
# 📌 Amac: Kullanici onayli New Site provisioning apply HTTP endpointlerini tanimlar
# 📌 Modul - Python
# Version: 3.78.0
# Aciklama: Controller request body/query parsing yapar ve ProvisioningApplyService katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from config.constants import PROVISIONING_APPLY_ROUTE_PREFIX, PROVISIONING_APPLY_ROUTE_TAG
from config.settings import AppSettings
from controllers.package_download_controller import package_download_service
from controllers.quick_app_controller import quick_app_service
from controllers.runtime_version_controller import runtime_version_service
from controllers.web_server_profile_controller import web_server_profile_service
from controllers.web_server_workflow_controller import web_server_workflow_service
from repositories.app_registry_repository import AppRegistryRepository
from repositories.provisioning_apply_registry_repository import ProvisioningApplyRegistryRepository
from services.provisioning_apply_service import ProvisioningApplyService
from tools.mysql_database_tool import MysqlDatabaseTool
from views.api_response_view import ApiResponseView


class ProvisioningApplyRequest(BaseModel):
    project_name: str = "Demo Quick App"
    template_code: str = "php-empty"
    domain: str = ""
    port: int = Field(default=80, ge=1, le=65535)
    web_server: str = "apache"
    include_mysql: bool = True
    include_php: bool = True
    include_mailpit: bool = False
    dry_run: bool = True
    approved: bool = False
    allow_real_execution: bool = False
    target_dir: str = ""
    mysql_admin_user: str = "root"
    mysql_admin_password: str = ""


router = APIRouter(prefix=PROVISIONING_APPLY_ROUTE_PREFIX, tags=[PROVISIONING_APPLY_ROUTE_TAG])
settings = AppSettings.load()
provisioning_apply_service = ProvisioningApplyService(
    quick_app_service=quick_app_service,
    package_download_service=package_download_service,
    runtime_version_service=runtime_version_service,
    web_server_profile_service=web_server_profile_service,
    web_server_workflow_service=web_server_workflow_service,
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
    apply_registry_repository=ProvisioningApplyRegistryRepository(settings.storage_path),
    mysql_database_tool=MysqlDatabaseTool(settings.root_path, settings.allow_shell_commands),
)
api_response_view = ApiResponseView()


@router.get("")
def list_provisioning_apply_records() -> dict:
    return api_response_view.render(provisioning_apply_service.list_records())


@router.get("/{project_code}")
def get_latest_provisioning_apply_record(project_code: str) -> dict:
    return api_response_view.render(provisioning_apply_service.get_latest_record(project_code))


@router.get("/{project_code}/plan")
def plan_provisioning_apply(
    project_code: str,
    template_code: str = Query(default="php-empty"),
    project_name: str = Query(default="Demo Quick App"),
    domain: str = Query(default=""),
    port: int = Query(default=80, ge=1, le=65535),
    web_server: str = Query(default="apache"),
    include_mysql: bool = Query(default=True),
    include_php: bool = Query(default=True),
    include_mailpit: bool = Query(default=False),
    mysql_admin_user: str = Query(default="root"),
) -> dict:
    return api_response_view.render(
        provisioning_apply_service.plan_apply(
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
    )


@router.post("/{project_code}/apply")
def apply_provisioning(project_code: str, request: ProvisioningApplyRequest) -> dict:
    return api_response_view.render(
        provisioning_apply_service.apply(
            project_code=project_code,
            project_name=request.project_name,
            template_code=request.template_code,
            domain=request.domain,
            port=request.port,
            web_server=request.web_server,
            include_mysql=request.include_mysql,
            include_php=request.include_php,
            include_mailpit=request.include_mailpit,
            dry_run=request.dry_run,
            approved=request.approved,
            allow_real_execution=request.allow_real_execution,
            target_dir=request.target_dir,
            mysql_admin_user=request.mysql_admin_user,
            mysql_admin_password=request.mysql_admin_password,
        )
    )
