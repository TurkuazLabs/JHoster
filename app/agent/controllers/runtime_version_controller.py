# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\runtime_version_controller.py
# 📌 Amac: Runtime ve portable version HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 2.0.0
# Aciklama: Controller sadece request alir, portable scan, summary, latest activation ve aktif runtime service akisini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import RUNTIME_VERSION_ROUTE_PREFIX, RUNTIME_VERSION_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from services.runtime_version_service import RuntimeVersionService
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=RUNTIME_VERSION_ROUTE_PREFIX, tags=[RUNTIME_VERSION_ROUTE_TAG])

settings = AppSettings.load()
runtime_version_service = RuntimeVersionService(
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
    runtime_version_repository=RuntimeVersionRepository(settings.storage_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_runtime_versions() -> dict:
    return api_response_view.render(runtime_version_service.list_runtime_versions())


@router.get("/active")
def list_active_runtime_versions() -> dict:
    return api_response_view.render(runtime_version_service.list_active_versions())






@router.get("/portable-definitions")
def list_portable_family_definitions() -> dict:
    return api_response_view.render(runtime_version_service.list_portable_family_definitions())


@router.get("/portable-summary")
def get_portable_version_summary() -> dict:
    return api_response_view.render(runtime_version_service.portable_summary())

@router.get("/portable-scan")
def scan_portable_runtime_versions() -> dict:
    return api_response_view.render(runtime_version_service.scan_portable_versions())


@router.get("/{family}/portable-scan")
def scan_portable_runtime_family(family: str) -> dict:
    return api_response_view.render(runtime_version_service.scan_portable_family(family))


@router.post("/{family}/activate-portable")
def activate_portable_runtime_version(
    family: str,
    folder_name: str = Query(default=""),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(runtime_version_service.activate_portable_version(family, folder_name, dry_run))


@router.post("/{family}/activate-latest-portable")
def activate_latest_portable_runtime_version(
    family: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(runtime_version_service.activate_latest_portable_version(family, dry_run))

@router.get("/{family}/active")
def get_active_runtime_version(family: str) -> dict:
    return api_response_view.render(runtime_version_service.get_active_version(family))


@router.get("/{family}")
def get_runtime_family(family: str) -> dict:
    return api_response_view.render(runtime_version_service.get_runtime_family(family))


@router.post("/{component_code}/activate")
def activate_runtime_version(
    component_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(runtime_version_service.activate_runtime_version(component_code, dry_run))
