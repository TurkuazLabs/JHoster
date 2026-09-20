# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\local_package_controller.py
# 📌 Amac: Local package HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve local package service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import LOCAL_PACKAGE_ROUTE_PREFIX, LOCAL_PACKAGE_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.local_package_repository import LocalPackageRepository
from repositories.manifest_repository import ManifestRepository
from services.local_package_service import LocalPackageService
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.local_package_installer_tool import LocalPackageInstallerTool
from tools.manifest_validation_tool import ManifestValidationTool
from tools.safe_path_tool import SafePathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=LOCAL_PACKAGE_ROUTE_PREFIX, tags=[LOCAL_PACKAGE_ROUTE_TAG])

settings = AppSettings.load()
manifest_repository = ManifestRepository(settings.modules_path)
local_package_service = LocalPackageService(
    local_package_repository=LocalPackageRepository(manifest_repository),
    manifest_validation_tool=ManifestValidationTool(),
    local_package_installer_tool=LocalPackageInstallerTool(
        safe_path_tool=SafePathTool(settings.root_path),
        checksum_tool=ChecksumTool(),
        archive_extract_tool=ArchiveExtractTool(),
    ),
    execution_log_repository=ExecutionLogRepository(settings.storage_path),
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
)
api_response_view = ApiResponseView()


@router.get("")
def list_local_packages() -> dict:
    return api_response_view.render(local_package_service.list_local_packages())


@router.get("/{component_code}")
def get_local_package_detail(component_code: str) -> dict:
    return api_response_view.render(local_package_service.get_local_package_detail(component_code))


@router.get("/{component_code}/plan")
def get_local_package_plan(component_code: str) -> dict:
    return api_response_view.render(local_package_service.get_local_package_plan(component_code))


@router.post("/{component_code}/install")
def install_local_package(
    component_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(local_package_service.install_local_package(component_code, dry_run))
