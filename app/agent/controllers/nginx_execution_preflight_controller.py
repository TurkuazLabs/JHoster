# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_execution_preflight_controller.py
# 📌 Amac: JHoster Nginx real execution preflight HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx execution preflight service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_EXECUTION_PREFLIGHT_ROUTE_PREFIX, NGINX_EXECUTION_PREFLIGHT_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from repositories.nginx_execution_preflight_registry_repository import NginxExecutionPreflightRegistryRepository
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from services.nginx_execution_preflight_service import NginxExecutionPreflightService
from tools.nginx_execution_preflight_tool import NginxExecutionPreflightTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_EXECUTION_PREFLIGHT_ROUTE_PREFIX, tags=[NGINX_EXECUTION_PREFLIGHT_ROUTE_TAG])

settings = AppSettings.load()
nginx_execution_preflight_service = NginxExecutionPreflightService(
    root_path=settings.root_path,
    nginx_publish_registry_repository=NginxPublishRegistryRepository(settings.storage_path),
    nginx_executable_registry_repository=NginxExecutableRegistryRepository(settings.storage_path),
    nginx_execution_preflight_registry_repository=NginxExecutionPreflightRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    nginx_execution_preflight_tool=NginxExecutionPreflightTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_preflight_records() -> dict:
    return api_response_view.render(nginx_execution_preflight_service.list_preflight_records())


@router.get("/{project_code}")
def get_latest_preflight(project_code: str) -> dict:
    return api_response_view.render(nginx_execution_preflight_service.get_latest_preflight(project_code))


@router.get("/{project_code}/plan")
def plan_preflight(project_code: str) -> dict:
    return api_response_view.render(nginx_execution_preflight_service.plan_preflight(project_code))


@router.post("/{project_code}/preflight")
def run_preflight(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        nginx_execution_preflight_service.run_preflight(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
