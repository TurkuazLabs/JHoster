# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\quick_app_controller.py
# 📌 Amac: Quick App ve stack secimli New Site HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 3.80.0
# Aciklama: Controller sadece request alir ve stack secimlerini provisioning destekli Quick App service katmanina aktarir
# Bagimli Oldugu Katman: Controller

from pathlib import Path

from fastapi import APIRouter, Query

from config.constants import QUICK_APP_ROUTE_PREFIX, QUICK_APP_ROUTE_TAG, STACK_PROVISIONING_CONFIG_FILE_NAME
from config.settings import AppSettings
from repositories.hosts_auto_registry_repository import HostsAutoRegistryRepository
from repositories.license_state_repository import LicenseStateRepository
from repositories.local_entitlement_repository import LocalEntitlementRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from repositories.quick_app_registry_repository import QuickAppRegistryRepository
from repositories.manifest_repository import ManifestRepository
from repositories.package_download_repository import PackageDownloadRepository
from repositories.stack_provisioning_config_repository import StackProvisioningConfigRepository
from repositories.runtime_version_repository import RuntimeVersionRepository
from services.hosts_auto_service import HostsAutoService
from services.plan_gate_service import PlanGateService
from services.quick_app_service import QuickAppService
from services.stack_provisioning_service import StackProvisioningService
from tools.admin_privilege_tool import AdminPrivilegeTool
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.http_download_tool import HttpDownloadTool
from tools.package_download_installer_tool import PackageDownloadInstallerTool
from tools.hosts_auto_file_tool import HostsAutoFileTool
from tools.project_path_tool import ProjectPathTool
from tools.quick_app_template_tool import QuickAppTemplateTool
from tools.safe_path_tool import SafePathTool
from tools.web_server_profile_tool import WebServerProfileTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=QUICK_APP_ROUTE_PREFIX, tags=[QUICK_APP_ROUTE_TAG])

settings = AppSettings.load()
project_path_tool = ProjectPathTool(settings.root_path)
project_registry_repository = ProjectRegistryRepository(settings.storage_path)
plan_gate_service = PlanGateService(
    entitlement_provider=LocalEntitlementRepository(
        license_state_repository=LicenseStateRepository(settings.storage_path),
    ),
    project_registry_repository=project_registry_repository,
)
hosts_auto_service = HostsAutoService(
    project_registry_repository=project_registry_repository,
    hosts_auto_registry_repository=HostsAutoRegistryRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    hosts_auto_file_tool=HostsAutoFileTool(settings.root_path, AdminPrivilegeTool()),
)
stack_provisioning_service = StackProvisioningService(
    stack_config_repository=StackProvisioningConfigRepository(
        Path(__file__).resolve().parents[1] / "config" / STACK_PROVISIONING_CONFIG_FILE_NAME
    ),
    package_download_repository=PackageDownloadRepository(settings.storage_path),
    manifest_repository=ManifestRepository(settings.modules_path),
    package_download_installer_tool=PackageDownloadInstallerTool(
        safe_path_tool=SafePathTool(settings.root_path),
        http_download_tool=HttpDownloadTool(),
        checksum_tool=ChecksumTool(),
        archive_extract_tool=ArchiveExtractTool(),
    ),
    web_server_profile_tool=WebServerProfileTool(settings.root_path),
)

quick_app_service = QuickAppService(
    quick_app_registry_repository=QuickAppRegistryRepository(settings.storage_path),
    project_registry_repository=project_registry_repository,
    runtime_version_repository=RuntimeVersionRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    quick_app_template_tool=QuickAppTemplateTool(settings.root_path, project_path_tool),
    plan_gate_service=plan_gate_service,
    hosts_auto_service=hosts_auto_service,
    stack_provisioning_service=stack_provisioning_service,
)
api_response_view = ApiResponseView()


@router.get("")
def list_quick_app_records() -> dict:
    return api_response_view.render(quick_app_service.list_records())


@router.get("/templates")
def list_quick_app_templates() -> dict:
    return api_response_view.render(quick_app_service.list_templates())


@router.get("/templates/{template_code}")
def get_quick_app_template(template_code: str) -> dict:
    return api_response_view.render(quick_app_service.get_template(template_code))


@router.get("/{project_code}")
def get_latest_quick_app_record(project_code: str) -> dict:
    return api_response_view.render(quick_app_service.get_latest_record(project_code))


@router.get("/{project_code}/plan")
def plan_quick_app(
    project_code: str,
    template_code: str = Query(default="php-empty"),
    project_name: str = Query(default="Demo Quick App"),
    domain: str = Query(default=""),
    port: int = Query(default=80),
    web_server: str = Query(default="apache"),
    include_mysql: bool = Query(default=True),
    include_php: bool = Query(default=True),
    include_mailpit: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        quick_app_service.plan_app(project_code, project_name, template_code, domain, port, web_server, include_mysql, include_php, include_mailpit)
    )


@router.post("/{project_code}/create")
def create_quick_app(
    project_code: str,
    template_code: str = Query(default="php-empty"),
    project_name: str = Query(default="Demo Quick App"),
    domain: str = Query(default=""),
    port: int = Query(default=80),
    dry_run: bool = Query(default=True),
    web_server: str = Query(default="apache"),
    include_mysql: bool = Query(default=True),
    include_php: bool = Query(default=True),
    include_mailpit: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        quick_app_service.create_app(project_code, project_name, template_code, domain, port, dry_run, web_server, include_mysql, include_php, include_mailpit)
    )
