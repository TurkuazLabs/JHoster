# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\root_controller.py
# 📌 Amac: JHoster agent ana sayfa HTTP endpointini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve service/view katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, Response

from config.constants import FAVICON_ROUTE_PATH, ROOT_ROUTE_PATH, ROOT_ROUTE_TAG
from config.settings import AppSettings
from services.app_info_service import AppInfoService
from views.html_response_view import HtmlResponseView


router = APIRouter(tags=[ROOT_ROUTE_TAG])

settings = AppSettings.load()
app_info_service = AppInfoService(settings)
html_response_view = HtmlResponseView()


@router.get(ROOT_ROUTE_PATH, response_class=HTMLResponse)
def get_root_page() -> HTMLResponse:
    return html_response_view.render(app_info_service.get_root_page_data())


@router.get(FAVICON_ROUTE_PATH, include_in_schema=False)
def get_favicon() -> Response:
    return Response(status_code=204)
