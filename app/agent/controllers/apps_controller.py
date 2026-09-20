# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apps_controller.py
# 📌 Amac: Kurulu app/component HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve app service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import APPS_ROUTE_PREFIX, APPS_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from services.app_service import AppService
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APPS_ROUTE_PREFIX, tags=[APPS_ROUTE_TAG])

settings = AppSettings.load()
app_service = AppService(
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_apps() -> dict:
    return api_response_view.render(app_service.list_apps())


@router.get("/{component_code}")
def get_app_detail(component_code: str) -> dict:
    return api_response_view.render(app_service.get_app_detail(component_code))
