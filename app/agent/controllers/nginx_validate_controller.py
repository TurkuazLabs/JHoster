# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_validate_controller.py
# 📌 Amac: JHoster Nginx validate HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx validate service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_VALIDATE_ROUTE_PREFIX, NGINX_VALIDATE_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_publish_registry_repository import NginxPublishRegistryRepository
from repositories.nginx_validate_registry_repository import NginxValidateRegistryRepository
from services.nginx_validate_service import NginxValidateService
from tools.nginx_config_validator_tool import NginxConfigValidatorTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_VALIDATE_ROUTE_PREFIX, tags=[NGINX_VALIDATE_ROUTE_TAG])

settings = AppSettings.load()
nginx_validate_service = NginxValidateService(
    root_path=settings.root_path,
    nginx_publish_registry_repository=NginxPublishRegistryRepository(settings.storage_path),
    nginx_validate_registry_repository=NginxValidateRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    nginx_config_validator_tool=NginxConfigValidatorTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_validation_records() -> dict:
    return api_response_view.render(nginx_validate_service.list_validation_records())


@router.get("/{project_code}")
def get_latest_validation(project_code: str) -> dict:
    return api_response_view.render(nginx_validate_service.get_latest_validation(project_code))


@router.get("/{project_code}/plan")
def plan_nginx_validation(project_code: str) -> dict:
    return api_response_view.render(nginx_validate_service.plan_project_validation(project_code))


@router.post("/{project_code}/validate")
def validate_nginx_config(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        nginx_validate_service.validate_project_config(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
