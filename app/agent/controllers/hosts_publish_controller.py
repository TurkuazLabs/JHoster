# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\hosts_publish_controller.py
# 📌 Amac: JHoster hosts publish HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve hosts publish service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import HOSTS_PUBLISH_DEFAULT_IP, HOSTS_PUBLISH_ROUTE_PREFIX, HOSTS_PUBLISH_ROUTE_TAG
from config.settings import AppSettings
from repositories.hosts_publish_registry_repository import HostsPublishRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from services.hosts_publish_service import HostsPublishService
from tools.hosts_file_publisher_tool import HostsFilePublisherTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=HOSTS_PUBLISH_ROUTE_PREFIX, tags=[HOSTS_PUBLISH_ROUTE_TAG])

settings = AppSettings.load()
hosts_publish_service = HostsPublishService(
    virtual_host_registry_repository=VirtualHostRegistryRepository(settings.storage_path),
    hosts_publish_registry_repository=HostsPublishRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    hosts_file_publisher_tool=HostsFilePublisherTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_hosts_publish_records() -> dict:
    return api_response_view.render(hosts_publish_service.list_publish_records())


@router.get("/{project_code}")
def get_latest_hosts_publish(project_code: str) -> dict:
    return api_response_view.render(hosts_publish_service.get_latest_publish(project_code))


@router.get("/{project_code}/plan")
def plan_hosts_publish(
    project_code: str,
    ip: str = Query(default=HOSTS_PUBLISH_DEFAULT_IP),
) -> dict:
    return api_response_view.render(
        hosts_publish_service.plan_project_hosts_publish(
            project_code=project_code,
            ip_value=ip,
        )
    )


@router.post("/{project_code}/publish")
def publish_hosts_entry(
    project_code: str,
    ip: str = Query(default=HOSTS_PUBLISH_DEFAULT_IP),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        hosts_publish_service.publish_project_hosts(
            project_code=project_code,
            ip_value=ip,
            dry_run=dry_run,
        )
    )
