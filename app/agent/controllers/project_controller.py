# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\project_controller.py
# 📌 Amac: JHoster user project HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Controller sadece request alir ve project service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import PROJECT_DEFAULT_RUNTIME_FAMILY, PROJECT_ROUTE_PREFIX, PROJECT_ROUTE_TAG
from config.settings import AppSettings
from repositories.hosts_auto_registry_repository import HostsAutoRegistryRepository
from repositories.license_state_repository import LicenseStateRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from services.hosts_auto_service import HostsAutoService
from services.plan_gate_service import PlanGateService
from services.project_service import ProjectService
from tools.admin_privilege_tool import AdminPrivilegeTool
from tools.hosts_auto_file_tool import HostsAutoFileTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=PROJECT_ROUTE_PREFIX, tags=[PROJECT_ROUTE_TAG])

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
project_service = ProjectService(
    project_registry_repository=project_registry_repository,
    runtime_version_repository=RuntimeVersionRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    plan_gate_service=plan_gate_service,
    hosts_auto_service=hosts_auto_service,
)
api_response_view = ApiResponseView()


@router.get("")
def list_projects() -> dict:
    return api_response_view.render(project_service.list_projects())


@router.post("")
def create_project(
    project_code: str = Query(...),
    project_name: str = Query(default="Demo Site"),
    runtime_family: str = Query(default=PROJECT_DEFAULT_RUNTIME_FAMILY),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        project_service.create_project(project_code, project_name, runtime_family, dry_run)
    )


@router.get("/{project_code}")
def get_project(project_code: str) -> dict:
    return api_response_view.render(project_service.get_project(project_code))
