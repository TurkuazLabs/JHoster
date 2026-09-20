# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\component_controller.py
# 📌 Amac: JHoster component katalog HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import COMPONENT_ROUTE_PREFIX, COMPONENT_ROUTE_TAG
from config.settings import AppSettings
from repositories.manifest_repository import ManifestRepository
from services.component_service import ComponentService
from tools.manifest_validation_tool import ManifestValidationTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=COMPONENT_ROUTE_PREFIX, tags=[COMPONENT_ROUTE_TAG])

settings = AppSettings.load()
component_service = ComponentService(
    manifest_repository=ManifestRepository(settings.modules_path),
    manifest_validation_tool=ManifestValidationTool(),
)
api_response_view = ApiResponseView()


@router.get("")
def list_components() -> dict:
    return api_response_view.render(component_service.list_components())


@router.get("/{component_code}")
def get_component_detail(component_code: str) -> dict:
    return api_response_view.render(component_service.get_component_detail(component_code))


@router.get("/{component_code}/plan")
def get_component_plan(component_code: str) -> dict:
    return api_response_view.render(component_service.get_component_plan(component_code))
