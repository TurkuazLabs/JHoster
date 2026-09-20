# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_reload_controller.py
# 📌 Amac: JHoster Nginx reload HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx reload service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_RELOAD_ROUTE_PREFIX, NGINX_RELOAD_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_reload_registry_repository import NginxReloadRegistryRepository
from repositories.nginx_validate_registry_repository import NginxValidateRegistryRepository
from services.nginx_reload_service import NginxReloadService
from tools.nginx_reload_tool import NginxReloadTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_RELOAD_ROUTE_PREFIX, tags=[NGINX_RELOAD_ROUTE_TAG])

settings = AppSettings.load()
nginx_reload_service = NginxReloadService(
    root_path=settings.root_path,
    nginx_validate_registry_repository=NginxValidateRegistryRepository(settings.storage_path),
    nginx_reload_registry_repository=NginxReloadRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    nginx_reload_tool=NginxReloadTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_reload_records() -> dict:
    return api_response_view.render(nginx_reload_service.list_reload_records())


@router.get("/{project_code}")
def get_latest_reload(project_code: str) -> dict:
    return api_response_view.render(nginx_reload_service.get_latest_reload(project_code))


@router.get("/{project_code}/plan")
def plan_nginx_reload(project_code: str) -> dict:
    return api_response_view.render(nginx_reload_service.plan_project_reload(project_code))


@router.post("/{project_code}/reload")
def reload_nginx_config(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        nginx_reload_service.reload_project_config(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
