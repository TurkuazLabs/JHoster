# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apache_validate_controller.py
# 📌 Amac: JHoster Apache validate HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve Apache validate service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import APACHE_VALIDATE_ROUTE_PREFIX, APACHE_VALIDATE_ROUTE_TAG
from config.settings import AppSettings
from repositories.apache_publish_registry_repository import ApachePublishRegistryRepository
from repositories.apache_validate_registry_repository import ApacheValidateRegistryRepository
from services.apache_validate_service import ApacheValidateService
from tools.apache_config_validator_tool import ApacheConfigValidatorTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APACHE_VALIDATE_ROUTE_PREFIX, tags=[APACHE_VALIDATE_ROUTE_TAG])

settings = AppSettings.load()
apache_validate_service = ApacheValidateService(
    root_path=settings.root_path,
    apache_publish_registry_repository=ApachePublishRegistryRepository(settings.storage_path),
    apache_validate_registry_repository=ApacheValidateRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    apache_config_validator_tool=ApacheConfigValidatorTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_validation_records() -> dict:
    return api_response_view.render(apache_validate_service.list_validation_records())


@router.get("/{project_code}")
def get_latest_validation(project_code: str) -> dict:
    return api_response_view.render(apache_validate_service.get_latest_validation(project_code))


@router.get("/{project_code}/plan")
def plan_apache_validation(project_code: str) -> dict:
    return api_response_view.render(apache_validate_service.plan_project_validation(project_code))


@router.post("/{project_code}/validate")
def validate_apache_config(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        apache_validate_service.validate_project_config(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
