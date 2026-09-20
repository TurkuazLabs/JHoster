# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apache_publish_controller.py
# 📌 Amac: JHoster Apache publish HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve Apache publish service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import APACHE_PUBLISH_ROUTE_PREFIX, APACHE_PUBLISH_ROUTE_TAG
from config.settings import AppSettings
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_vhost_registry_repository import ApacheVhostRegistryRepository
from services.apache_publish_service import ApachePublishService
from tools.apache_config_publisher_tool import ApacheConfigPublisherTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APACHE_PUBLISH_ROUTE_PREFIX, tags=[APACHE_PUBLISH_ROUTE_TAG])

settings = AppSettings.load()
apache_publish_service = ApachePublishService(
    root_path=settings.root_path,
    apache_vhost_registry_repository=ApacheVhostRegistryRepository(settings.storage_path),
    apache_publish_registry_repository=ApachePublishRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    apache_config_publisher_tool=ApacheConfigPublisherTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_published_configs() -> dict:
    return api_response_view.render(apache_publish_service.list_published_configs())


@router.get("/{project_code}")
def get_latest_publish(project_code: str) -> dict:
    return api_response_view.render(apache_publish_service.get_latest_publish(project_code))


@router.get("/{project_code}/plan")
def plan_apache_publish(
    project_code: str,
    target_dir: str = Query(default=""),
) -> dict:
    return api_response_view.render(apache_publish_service.plan_project_publish(project_code, target_dir))


@router.post("/{project_code}/publish")
def publish_apache_vhost(
    project_code: str,
    dry_run: bool = Query(default=True),
    target_dir: str = Query(default=""),
) -> dict:
    return api_response_view.render(
        apache_publish_service.publish_project_vhost(
            project_code=project_code,
            target_dir=target_dir,
            dry_run=dry_run,
        )
    )
