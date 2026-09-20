# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\folder_layout_controller.py
# 📌 Amac: JHoster folder layout HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve FolderLayoutService katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import FOLDER_LAYOUT_ROUTE_PREFIX, FOLDER_LAYOUT_ROUTE_TAG
from config.settings import AppSettings
from services.folder_layout_service import FolderLayoutService
from tools.folder_layout_tool import FolderLayoutTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=FOLDER_LAYOUT_ROUTE_PREFIX, tags=[FOLDER_LAYOUT_ROUTE_TAG])

settings = AppSettings.load()
folder_layout_service = FolderLayoutService(
    folder_layout_tool=FolderLayoutTool(settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def get_folder_layout() -> dict:
    return api_response_view.render(folder_layout_service.get_standard())


@router.get("/plan")
def plan_folder_layout() -> dict:
    return api_response_view.render(folder_layout_service.plan_layout())


@router.post("/apply")
def apply_folder_layout(dry_run: bool = True) -> dict:
    return api_response_view.render(folder_layout_service.apply_layout(dry_run))
