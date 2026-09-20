# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\cache_controller.py
# 📌 Amac: JHoster cache HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve cache service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import CACHE_ROUTE_PREFIX, CACHE_ROUTE_TAG
from config.settings import AppSettings
from repositories.cache_repository import CacheRepository
from services.cache_service import CacheService
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=CACHE_ROUTE_PREFIX, tags=[CACHE_ROUTE_TAG])

settings = AppSettings.load()
cache_service = CacheService(
    cache_repository=CacheRepository(settings.cache_path, settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_cache() -> dict:
    return api_response_view.render(cache_service.list_cache())
