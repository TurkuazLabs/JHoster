# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\virtual_host_controller.py
# 📌 Amac: JHoster virtual host HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve virtual host service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import (
    VIRTUAL_HOST_DEFAULT_PORT,
    VIRTUAL_HOST_ROUTE_PREFIX,
    VIRTUAL_HOST_ROUTE_TAG,
)
from config.settings import AppSettings
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from services.virtual_host_service import VirtualHostService
from tools.project_path_tool import ProjectPathTool
from tools.virtual_host_config_tool import VirtualHostConfigTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=VIRTUAL_HOST_ROUTE_PREFIX, tags=[VIRTUAL_HOST_ROUTE_TAG])

settings = AppSettings.load()
virtual_host_service = VirtualHostService(
    project_registry_repository=ProjectRegistryRepository(settings.storage_path),
    virtual_host_registry_repository=VirtualHostRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    virtual_host_config_tool=VirtualHostConfigTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_virtual_hosts() -> dict:
    return api_response_view.render(virtual_host_service.list_virtual_hosts())


@router.get("/{project_code}")
def get_virtual_host(project_code: str) -> dict:
    return api_response_view.render(virtual_host_service.get_virtual_host(project_code))


@router.get("/{project_code}/plan")
def plan_virtual_host(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=VIRTUAL_HOST_DEFAULT_PORT),
) -> dict:
    return api_response_view.render(virtual_host_service.plan_virtual_host(project_code, domain, port))


@router.post("/{project_code}/generate")
def generate_virtual_host(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=VIRTUAL_HOST_DEFAULT_PORT),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        virtual_host_service.generate_virtual_host(project_code, domain, port, dry_run)
    )
