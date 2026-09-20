# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\package_download_controller.py
# 📌 Amac: Otomatik paket indirme HTTP endpointlerini tanimlar
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve package download service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import PACKAGE_DOWNLOAD_ROUTE_PREFIX, PACKAGE_DOWNLOAD_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.package_download_repository import PackageDownloadRepository
from services.package_download_service import PackageDownloadService
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.http_download_tool import HttpDownloadTool
from tools.package_download_installer_tool import PackageDownloadInstallerTool
from tools.safe_path_tool import SafePathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=PACKAGE_DOWNLOAD_ROUTE_PREFIX, tags=[PACKAGE_DOWNLOAD_ROUTE_TAG])

settings = AppSettings.load()
package_download_service = PackageDownloadService(
    package_download_repository=PackageDownloadRepository(settings.storage_path),
    package_download_installer_tool=PackageDownloadInstallerTool(
        safe_path_tool=SafePathTool(settings.root_path),
        http_download_tool=HttpDownloadTool(),
        checksum_tool=ChecksumTool(),
        archive_extract_tool=ArchiveExtractTool(),
    ),
    execution_log_repository=ExecutionLogRepository(settings.storage_path),
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
    allow_external_downloads=settings.allow_external_downloads,
)
api_response_view = ApiResponseView()


@router.get("")
def list_packages() -> dict:
    return api_response_view.render(package_download_service.list_packages())


@router.get("/{package_code}")
def get_package_detail(package_code: str) -> dict:
    return api_response_view.render(package_download_service.get_package_detail(package_code))


@router.get("/{package_code}/plan")
def get_plan(package_code: str) -> dict:
    return api_response_view.render(package_download_service.get_plan(package_code))


@router.post("/{package_code}/download")
def download_package(package_code: str, dry_run: bool = Query(default=True)) -> dict:
    return api_response_view.render(package_download_service.download_package(package_code, dry_run))


@router.post("/{package_code}/install")
def install_package(package_code: str, dry_run: bool = Query(default=True)) -> dict:
    return api_response_view.render(package_download_service.install_package(package_code, dry_run))
