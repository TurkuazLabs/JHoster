# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\service_adapter_controller.py
# 📌 Amac: Runtime service adapter HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve service adapter service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import SERVICE_ADAPTER_ROUTE_PREFIX, SERVICE_ADAPTER_ROUTE_TAG
from services.service_adapter_service import ServiceAdapterService
from tools.service_adapters.adapter_registry import ServiceAdapterRegistryTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=SERVICE_ADAPTER_ROUTE_PREFIX, tags=[SERVICE_ADAPTER_ROUTE_TAG])

service_adapter_service = ServiceAdapterService(ServiceAdapterRegistryTool())
api_response_view = ApiResponseView()


@router.get("")
def list_adapters() -> dict:
    return api_response_view.render(service_adapter_service.list_adapters())


@router.get("/{adapter_key}")
def get_adapter_detail(adapter_key: str) -> dict:
    return api_response_view.render(service_adapter_service.get_adapter_detail(adapter_key))
