# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\apache_executable_controller.py
# 📌 Amac: JHoster Apache executable tespit HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve Apache executable service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import APACHE_EXECUTABLE_ROUTE_PREFIX, APACHE_EXECUTABLE_ROUTE_TAG
from config.settings import AppSettings
from repositories.apache_executable_registry_repository import ApacheExecutableRegistryRepository
from services.apache_executable_service import ApacheExecutableService
from tools.apache_executable_detector_tool import ApacheExecutableDetectorTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=APACHE_EXECUTABLE_ROUTE_PREFIX, tags=[APACHE_EXECUTABLE_ROUTE_TAG])

settings = AppSettings.load()
apache_executable_service = ApacheExecutableService(
    apache_executable_registry_repository=ApacheExecutableRegistryRepository(settings.storage_path),
    apache_executable_detector_tool=ApacheExecutableDetectorTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_detection_records() -> dict:
    return api_response_view.render(apache_executable_service.list_detection_records())


@router.get("/latest")
def get_latest_detection() -> dict:
    return api_response_view.render(apache_executable_service.get_latest_detection())


@router.get("/plan")
def plan_detection() -> dict:
    return api_response_view.render(apache_executable_service.plan_detection())


@router.post("/detect")
def detect_executable(
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        apache_executable_service.detect_executable(
            dry_run=dry_run,
        )
    )
