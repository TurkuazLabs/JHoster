# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\quick_app_controller.py
# 📌 Amac: Quick App ve stack secimli New Site HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 3.72.0
# Aciklama: Controller sadece request alir ve stack secimlerini Quick App service katmanina aktarir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import QUICK_APP_ROUTE_PREFIX, QUICK_APP_ROUTE_TAG
from config.settings import AppSettings
from repositories.hosts_auto_registry_repository import HostsAutoRegistryRepository
from repositories.license_state_repository import LicenseStateRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.quick_app_registry_repository import QuickAppRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from services.hosts_auto_service import HostsAutoService
from services.plan_gate_service import PlanGateService
from services.quick_app_service import QuickAppService
from tools.admin_privilege_tool import AdminPrivilegeTool
from tools.hosts_auto_file_tool import HostsAutoFileTool
from tools.project_path_tool import ProjectPathTool
from tools.quick_app_template_tool import QuickAppTemplateTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=QUICK_APP_ROUTE_PREFIX, tags=[QUICK_APP_ROUTE_TAG])

settings = AppSettings.load()
project_path_tool = ProjectPathTool(settings.root_path)
project_registry_repository = ProjectRegistryRepository(settings.storage_path)
plan_gate_service = PlanGateService(
    license_state_repository=LicenseStateRepository(settings.storage_path),
    project_registry_repository=project_registry_repository,
)
hosts_auto_service = HostsAutoService(
    project_registry_repository=project_registry_repository,
    hosts_auto_registry_repository=HostsAutoRegistryRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    hosts_auto_file_tool=HostsAutoFileTool(settings.root_path, AdminPrivilegeTool()),
)
quick_app_service = QuickAppService(
    quick_app_registry_repository=QuickAppRegistryRepository(settings.storage_path),
    project_registry_repository=project_registry_repository,
    runtime_version_repository=RuntimeVersionRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    quick_app_template_tool=QuickAppTemplateTool(settings.root_path, project_path_tool),
    plan_gate_service=plan_gate_service,
    hosts_auto_service=hosts_auto_service,
)
api_response_view = ApiResponseView()


@router.get("")
def list_quick_app_records() -> dict:
    return api_response_view.render(quick_app_service.list_records())


@router.get("/templates")
def list_quick_app_templates() -> dict:
    return api_response_view.render(quick_app_service.list_templates())


@router.get("/templates/{template_code}")
def get_quick_app_template(template_code: str) -> dict:
    return api_response_view.render(quick_app_service.get_template(template_code))


@router.get("/{project_code}")
def get_latest_quick_app_record(project_code: str) -> dict:
    return api_response_view.render(quick_app_service.get_latest_record(project_code))


@router.get("/{project_code}/plan")
def plan_quick_app(
    project_code: str,
    template_code: str = Query(default="php-empty"),
    project_name: str = Query(default="Demo Quick App"),
    domain: str = Query(default=""),
    port: int = Query(default=80),
    web_server: str = Query(default="apache"),
    include_mysql: bool = Query(default=True),
    include_php: bool = Query(default=True),
    include_mailpit: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        quick_app_service.plan_app(project_code, project_name, template_code, domain, port, web_server, include_mysql, include_php, include_mailpit)
    )


@router.post("/{project_code}/create")
def create_quick_app(
    project_code: str,
    template_code: str = Query(default="php-empty"),
    project_name: str = Query(default="Demo Quick App"),
    domain: str = Query(default=""),
    port: int = Query(default=80),
    dry_run: bool = Query(default=True),
    web_server: str = Query(default="apache"),
    include_mysql: bool = Query(default=True),
    include_php: bool = Query(default=True),
    include_mailpit: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        quick_app_service.create_app(project_code, project_name, template_code, domain, port, dry_run, web_server, include_mysql, include_php, include_mailpit)
    )
