# 📄 Dosya Yolu: E:/JHoster/app/agent/controllers/hosts_auto_controller.py
# 📌 Amac: JHoster otomatik hosts senkron, inspect ve repair HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 3.69.0
# Aciklama: Controller sadece request alir ve HostsAutoService katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import HOSTS_AUTO_DEFAULT_IP, HOSTS_AUTO_ROUTE_PREFIX, HOSTS_AUTO_ROUTE_TAG
from config.settings import AppSettings
from repositories.hosts_auto_registry_repository import HostsAutoRegistryRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from services.hosts_auto_service import HostsAutoService
from tools.admin_privilege_tool import AdminPrivilegeTool
from tools.hosts_auto_file_tool import HostsAutoFileTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=HOSTS_AUTO_ROUTE_PREFIX, tags=[HOSTS_AUTO_ROUTE_TAG])

settings = AppSettings.load()
project_path_tool = ProjectPathTool(settings.root_path)
hosts_auto_service = HostsAutoService(
    project_registry_repository=ProjectRegistryRepository(settings.storage_path),
    hosts_auto_registry_repository=HostsAutoRegistryRepository(settings.storage_path),
    project_path_tool=project_path_tool,
    hosts_auto_file_tool=HostsAutoFileTool(settings.root_path, AdminPrivilegeTool()),
)
api_response_view = ApiResponseView()


@router.get("")
def list_hosts_auto_sync_records() -> dict:
    return api_response_view.render(hosts_auto_service.list_sync_records())


@router.get("/latest")
def get_latest_hosts_auto_sync() -> dict:
    return api_response_view.render(hosts_auto_service.get_latest_sync())


@router.get("/inspect")
def inspect_hosts_auto_sync(
    ip: str = Query(default=HOSTS_AUTO_DEFAULT_IP),
    real_write: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        hosts_auto_service.inspect_all(
            ip_value=ip,
            real_write=real_write,
        )
    )


@router.get("/plan")
def plan_hosts_auto_sync(
    ip: str = Query(default=HOSTS_AUTO_DEFAULT_IP),
    real_write: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        hosts_auto_service.plan_sync_all(
            ip_value=ip,
            real_write=real_write,
        )
    )


@router.get("/repair-plan")
def plan_hosts_auto_repair(
    ip: str = Query(default=HOSTS_AUTO_DEFAULT_IP),
    real_write: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        hosts_auto_service.plan_repair_all(
            ip_value=ip,
            real_write=real_write,
        )
    )


@router.post("/repair")
def repair_hosts_auto(
    ip: str = Query(default=HOSTS_AUTO_DEFAULT_IP),
    real_write: bool = Query(default=False),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        hosts_auto_service.repair_all(
            ip_value=ip,
            real_write=real_write,
            dry_run=dry_run,
        )
    )


@router.post("/sync")
def sync_hosts_auto(
    ip: str = Query(default=HOSTS_AUTO_DEFAULT_IP),
    real_write: bool = Query(default=False),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        hosts_auto_service.sync_all(
            ip_value=ip,
            real_write=real_write,
            dry_run=dry_run,
        )
    )
