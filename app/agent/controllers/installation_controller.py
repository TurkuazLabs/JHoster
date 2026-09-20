# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\installation_controller.py
# 📌 Amac: JHoster component executor HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Controller sadece request alir, installation service ve registry baglantisini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import INSTALL_HISTORY_ROUTE_PATH, INSTALLER_ROUTE_PREFIX, INSTALLER_ROUTE_TAG
from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.manifest_repository import ManifestRepository
from services.installation_service import InstallationService
from tools.action_executor_tool import ActionExecutorTool
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.manifest_validation_tool import ManifestValidationTool
from tools.safe_path_tool import SafePathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=INSTALLER_ROUTE_PREFIX, tags=[INSTALLER_ROUTE_TAG])
history_router = APIRouter(tags=[INSTALLER_ROUTE_TAG])

settings = AppSettings.load()
installation_service = InstallationService(
    manifest_repository=ManifestRepository(settings.modules_path),
    manifest_validation_tool=ManifestValidationTool(),
    action_executor_tool=ActionExecutorTool(
        safe_path_tool=SafePathTool(settings.root_path),
        checksum_tool=ChecksumTool(),
        archive_extract_tool=ArchiveExtractTool(),
        allow_shell_commands=settings.allow_shell_commands,
        allow_external_downloads=settings.allow_external_downloads,
        allow_safe_extract=settings.allow_safe_extract,
    ),
    execution_log_repository=ExecutionLogRepository(settings.storage_path),
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
)
api_response_view = ApiResponseView()


@router.post("/{component_code}/execute")
def execute_component(
    component_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(installation_service.execute_component(component_code, dry_run))


@history_router.get(INSTALL_HISTORY_ROUTE_PATH)
def get_install_history() -> dict:
    return api_response_view.render(installation_service.get_history())
