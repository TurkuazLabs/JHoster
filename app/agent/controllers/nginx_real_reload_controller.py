# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_real_reload_controller.py
# 📌 Amac: JHoster Nginx real reload adapter HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx real reload service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_REAL_RELOAD_ROUTE_PREFIX, NGINX_REAL_RELOAD_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from repositories.nginx_real_reload_registry_repository import NginxRealReloadRegistryRepository
from repositories.nginx_real_validate_registry_repository import NginxRealValidateRegistryRepository
from services.nginx_real_reload_service import NginxRealReloadService
from tools.nginx_real_reloader_tool import NginxRealReloaderTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_REAL_RELOAD_ROUTE_PREFIX, tags=[NGINX_REAL_RELOAD_ROUTE_TAG])

settings = AppSettings.load()
nginx_real_reload_service = NginxRealReloadService(
    root_path=settings.root_path,
    nginx_publish_registry_repository=NginxPublishRegistryRepository(settings.storage_path),
    nginx_executable_registry_repository=NginxExecutableRegistryRepository(settings.storage_path),
    nginx_real_validate_registry_repository=NginxRealValidateRegistryRepository(settings.storage_path),
    nginx_real_reload_registry_repository=NginxRealReloadRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    nginx_real_reloader_tool=NginxRealReloaderTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_real_reload_records() -> dict:
    return api_response_view.render(nginx_real_reload_service.list_real_reload_records())


@router.get("/{project_code}")
def get_latest_real_reload(project_code: str) -> dict:
    return api_response_view.render(nginx_real_reload_service.get_latest_real_reload(project_code))


@router.get("/{project_code}/plan")
def plan_real_reload(project_code: str) -> dict:
    return api_response_view.render(nginx_real_reload_service.plan_real_reload(project_code))


@router.post("/{project_code}/reload")
def reload_with_real_adapter(
    project_code: str,
    dry_run: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        nginx_real_reload_service.reload_with_real_adapter(
            project_code=project_code,
            dry_run=dry_run,
            allow_real_execution=allow_real_execution,
        )
    )
