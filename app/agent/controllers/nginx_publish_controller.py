# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_publish_controller.py
# 📌 Amac: JHoster Nginx publish HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx publish service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_PUBLISH_ROUTE_PREFIX, NGINX_PUBLISH_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from services.nginx_publish_service import NginxPublishService
from tools.nginx_config_publisher_tool import NginxConfigPublisherTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_PUBLISH_ROUTE_PREFIX, tags=[NGINX_PUBLISH_ROUTE_TAG])

settings = AppSettings.load()
nginx_publish_service = NginxPublishService(
    root_path=settings.root_path,
    virtual_host_registry_repository=VirtualHostRegistryRepository(settings.storage_path),
    nginx_publish_registry_repository=NginxPublishRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    nginx_config_publisher_tool=NginxConfigPublisherTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_published_configs() -> dict:
    return api_response_view.render(nginx_publish_service.list_published_configs())


@router.get("/{project_code}")
def get_latest_publish(project_code: str) -> dict:
    return api_response_view.render(nginx_publish_service.get_latest_publish(project_code))


@router.get("/{project_code}/plan")
def plan_nginx_publish(
    project_code: str,
    target_dir: str = Query(default=""),
) -> dict:
    return api_response_view.render(nginx_publish_service.plan_project_publish(project_code, target_dir))


@router.post("/{project_code}/publish")
def publish_nginx_vhost(
    project_code: str,
    dry_run: bool = Query(default=True),
    target_dir: str = Query(default=""),
) -> dict:
    return api_response_view.render(
        nginx_publish_service.publish_project_vhost(
            project_code=project_code,
            target_dir=target_dir,
            dry_run=dry_run,
        )
    )
