# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\process_controller.py
# 📌 Amac: JHoster process manager HTTP endpointlerini ve adapter baglantisini tanimlar
# 📌 Modul - FileType
# Version: 1.6.0
# Aciklama: Controller sadece request alir ve process service start, stop, restart, preflight, inspect, real profile, aktif web server mode, port guard ve status katmanlarini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import PROCESS_ROUTE_PREFIX, PROCESS_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.process_state_repository import ProcessStateRepository
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from services.process_service import ProcessService
from tools.process_guard_tool import ProcessGuardTool
from tools.safe_path_tool import SafePathTool
from tools.service_adapters.adapter_registry import ServiceAdapterRegistryTool
from tools.web_server_port_guard_tool import WebServerPortGuardTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=PROCESS_ROUTE_PREFIX, tags=[PROCESS_ROUTE_TAG])

settings = AppSettings.load()
process_service = ProcessService(
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
    process_state_repository=ProcessStateRepository(settings.storage_path),
    process_guard_tool=ProcessGuardTool(SafePathTool(settings.root_path)),
    service_adapter_registry_tool=ServiceAdapterRegistryTool(),
    web_server_port_guard_tool=WebServerPortGuardTool(),
    web_server_profile_registry_repository=WebServerProfileRegistryRepository(settings.storage_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_processes() -> dict:
    return api_response_view.render(process_service.list_processes())


@router.get("/{component_code}/status")
def get_process_status(
    component_code: str,
    prefer_real: bool = Query(default=False),
) -> dict:
    return api_response_view.render(process_service.get_process_status(component_code, prefer_real))


@router.get("/{component_code}/inspect")
def inspect_process(component_code: str) -> dict:
    return api_response_view.render(process_service.inspect_process(component_code))


@router.get("/{component_code}/preflight")
def preflight_process(component_code: str) -> dict:
    return api_response_view.render(process_service.preflight_process(component_code))


@router.get("/{component_code}/real-profile")
def get_real_process_profile(component_code: str) -> dict:
    return api_response_view.render(process_service.get_real_profile(component_code))


@router.get("/{component_code}/real-profile/plan")
def plan_real_process_profile(
    component_code: str,
    install_path: str = Query(default=""),
    enabled: bool | None = Query(default=None),
) -> dict:
    return api_response_view.render(process_service.plan_real_profile(component_code, install_path, enabled))


@router.post("/{component_code}/real-profile/apply")
def apply_real_process_profile(
    component_code: str,
    install_path: str = Query(default=""),
    enabled: bool | None = Query(default=None),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(process_service.apply_real_profile(component_code, install_path, enabled, dry_run))


@router.post("/{component_code}/start")
def start_process(
    component_code: str,
    dry_run: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
) -> dict:
    return api_response_view.render(process_service.start_process(component_code, dry_run, allow_real_execution))


@router.post("/{component_code}/stop")
def stop_process(
    component_code: str,
    dry_run: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
) -> dict:
    return api_response_view.render(process_service.stop_process(component_code, dry_run, allow_real_execution))


@router.post("/{component_code}/restart")
def restart_process(
    component_code: str,
    dry_run: bool = Query(default=True),
    allow_real_execution: bool = Query(default=False),
) -> dict:
    return api_response_view.render(process_service.restart_process(component_code, dry_run, allow_real_execution))
