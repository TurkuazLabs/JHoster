# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\nginx_executable_controller.py
# 📌 Amac: JHoster Nginx executable tespit HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve nginx executable service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import NGINX_EXECUTABLE_ROUTE_PREFIX, NGINX_EXECUTABLE_ROUTE_TAG
from config.settings import AppSettings
from repositories.nginx_executable_registry_repository import NginxExecutableRegistryRepository
from services.nginx_executable_service import NginxExecutableService
from tools.nginx_executable_detector_tool import NginxExecutableDetectorTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=NGINX_EXECUTABLE_ROUTE_PREFIX, tags=[NGINX_EXECUTABLE_ROUTE_TAG])

settings = AppSettings.load()
nginx_executable_service = NginxExecutableService(
    nginx_executable_registry_repository=NginxExecutableRegistryRepository(settings.storage_path),
    nginx_executable_detector_tool=NginxExecutableDetectorTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_detection_records() -> dict:
    return api_response_view.render(nginx_executable_service.list_detection_records())


@router.get("/latest")
def get_latest_detection() -> dict:
    return api_response_view.render(nginx_executable_service.get_latest_detection())


@router.get("/plan")
def plan_detection() -> dict:
    return api_response_view.render(nginx_executable_service.plan_detection())


@router.post("/detect")
def detect_executable(
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        nginx_executable_service.detect_executable(
            dry_run=dry_run,
        )
    )
