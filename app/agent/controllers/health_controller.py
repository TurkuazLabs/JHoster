# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\health_controller.py
# 📌 Amac: JHoster agent saglik kontrol HTTP endpointini tanimlar
# 📌 Modul - FileType
# Version: 1.0.1
# Aciklama: Controller sadece request alir ve service cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import HEALTH_ROUTE_PREFIX, HEALTH_ROUTE_TAG
from config.settings import AppSettings
from repositories.state_repository import StateRepository
from services.health_service import HealthService
from tools.system_info_tool import SystemInfoTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=HEALTH_ROUTE_PREFIX, tags=[HEALTH_ROUTE_TAG])

settings = AppSettings.load()
health_service = HealthService(
    state_repository=StateRepository(settings.storage_path),
    system_info_tool=SystemInfoTool(),
)
api_response_view = ApiResponseView()


@router.get("")
def get_health_status() -> dict:
    return api_response_view.render(health_service.get_health_status())
