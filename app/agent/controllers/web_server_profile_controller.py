# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\web_server_profile_controller.py
# 📌 Amac: JHoster web server profile HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve web server profile service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import WEB_SERVER_PROFILE_ROUTE_PREFIX, WEB_SERVER_PROFILE_ROUTE_TAG
from config.settings import AppSettings
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from services.web_server_profile_service import WebServerProfileService
from tools.web_server_profile_tool import WebServerProfileTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=WEB_SERVER_PROFILE_ROUTE_PREFIX, tags=[WEB_SERVER_PROFILE_ROUTE_TAG])

settings = AppSettings.load()
web_server_profile_service = WebServerProfileService(
    web_server_profile_registry_repository=WebServerProfileRegistryRepository(settings.storage_path),
    web_server_profile_tool=WebServerProfileTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_profiles() -> dict:
    return api_response_view.render(web_server_profile_service.list_profiles())


@router.get("/current")
def get_current_profile() -> dict:
    return api_response_view.render(web_server_profile_service.get_current_profile())


@router.get("/{server_code}")
def get_profile(server_code: str) -> dict:
    return api_response_view.render(web_server_profile_service.get_profile(server_code))


@router.get("/{server_code}/plan")
def plan_select_profile(server_code: str) -> dict:
    return api_response_view.render(web_server_profile_service.plan_select_profile(server_code))


@router.post("/{server_code}/select")
def select_profile(
    server_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        web_server_profile_service.select_profile(
            server_code=server_code,
            dry_run=dry_run,
        )
    )
