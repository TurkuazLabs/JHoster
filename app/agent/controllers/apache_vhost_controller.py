# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apache_vhost_controller.py
# 📌 Amac: JHoster Apache virtual host HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve Apache vhost service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import APACHE_VHOST_ROUTE_PREFIX, APACHE_VHOST_ROUTE_TAG
from config.settings import AppSettings
from repositories.apache_vhost_registry_repository import ApacheVhostRegistryRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from services.apache_vhost_service import ApacheVhostService
from tools.apache_vhost_config_tool import ApacheVhostConfigTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APACHE_VHOST_ROUTE_PREFIX, tags=[APACHE_VHOST_ROUTE_TAG])

settings = AppSettings.load()
apache_vhost_service = ApacheVhostService(
    project_registry_repository=ProjectRegistryRepository(settings.storage_path),
    apache_vhost_registry_repository=ApacheVhostRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    apache_vhost_config_tool=ApacheVhostConfigTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_apache_virtual_hosts() -> dict:
    return api_response_view.render(apache_vhost_service.list_virtual_hosts())


@router.get("/{project_code}")
def get_apache_virtual_host(project_code: str) -> dict:
    return api_response_view.render(apache_vhost_service.get_virtual_host(project_code))


@router.get("/{project_code}/plan")
def plan_apache_virtual_host(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=80),
) -> dict:
    return api_response_view.render(
        apache_vhost_service.plan_virtual_host(
            project_code=project_code,
            domain=domain,
            port=port,
        )
    )


@router.post("/{project_code}/generate")
def generate_apache_virtual_host(
    project_code: str,
    domain: str = Query(default=""),
    port: int = Query(default=80),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        apache_vhost_service.generate_virtual_host(
            project_code=project_code,
            domain=domain,
            port=port,
            dry_run=dry_run,
        )
    )
