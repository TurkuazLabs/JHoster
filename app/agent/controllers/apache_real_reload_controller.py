# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apache_real_reload_controller.py
# 📌 Amac: JHoster Apache real reload adapter HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve Apache real reload service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import APACHE_REAL_RELOAD_ROUTE_PREFIX, APACHE_REAL_RELOAD_ROUTE_TAG
from config.settings import AppSettings
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_real_reload_registry_repository import ApacheRealReloadRegistryRepository
from repositories.apache_real_validate_registry_repository import ApacheRealValidateRegistryRepository
from services.apache_real_reload_service import ApacheRealReloadService
from tools.apache_real_reloader_tool import ApacheRealReloaderTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APACHE_REAL_RELOAD_ROUTE_PREFIX, tags=[APACHE_REAL_RELOAD_ROUTE_TAG])

settings = AppSettings.load()
apache_real_reload_service = ApacheRealReloadService(
    root_path=settings.root_path,
    apache_publish_registry_repository=ApachePublishRegistryRepository(settings.storage_path),
    apache_executable_registry_repository=ApacheExecutableRegistryRepository(settings.storage_path),
    apache_real_validate_registry_repository=ApacheRealValidateRegistryRepository(settings.storage_path),
    apache_real_reload_registry_repository=ApacheRealReloadRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    apache_real_reloader_tool=ApacheRealReloaderTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_real_reload_records() -> dict:
    return api_response_view.render(apache_real_reload_service.list_real_reload_records())


@router.get("/{project_code}")
def get_latest_real_reload(project_code: str) -> dict:
    return api_response_view.render(apache_real_reload_service.get_latest_real_reload(project_code))


@router.get("/{project_code}/plan")
def plan_real_reload(project_code: str) -> dict:
    return api_response_view.render(apache_real_reload_service.plan_real_reload(project_code))


@router.post("/{project_code}/reload")
def reload_with_real_adapter(
    project_code: str,
    dry_run: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        apache_real_reload_service.reload_with_real_adapter(
            project_code=project_code,
            dry_run=dry_run,
            allow_real_execution=allow_real_execution,
        )
    )
