# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\hosts_apply_controller.py
# 📌 Amac: JHoster hosts apply ve rollback HTTP endpointlerini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve hosts apply service katmanini cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter, Query

from config.constants import HOSTS_APPLY_ROUTE_PREFIX, HOSTS_APPLY_ROUTE_TAG, HOSTS_PUBLISH_DEFAULT_IP
from config.settings import AppSettings
from repositories.hosts_apply_registry_repository import HostsApplyRegistryRepository
from repositories.virtual_host_registry_repository import VirtualHostRegistryRepository
from services.hosts_apply_service import HostsApplyService
from tools.admin_privilege_tool import AdminPrivilegeTool
from tools.hosts_file_apply_tool import HostsFileApplyTool
from tools.project_path_tool import ProjectPathTool
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=HOSTS_APPLY_ROUTE_PREFIX, tags=[HOSTS_APPLY_ROUTE_TAG])

settings = AppSettings.load()
admin_privilege_tool = AdminPrivilegeTool()
hosts_apply_service = HostsApplyService(
    virtual_host_registry_repository=VirtualHostRegistryRepository(settings.storage_path),
    hosts_apply_registry_repository=HostsApplyRegistryRepository(settings.storage_path),
    project_path_tool=ProjectPathTool(settings.root_path),
    hosts_file_apply_tool=HostsFileApplyTool(settings.root_path, admin_privilege_tool),
)
api_response_view = ApiResponseView()


@router.get("")
def list_hosts_apply_records() -> dict:
    return api_response_view.render(hosts_apply_service.list_apply_records())


@router.get("/{project_code}")
def get_latest_hosts_apply(project_code: str) -> dict:
    return api_response_view.render(hosts_apply_service.get_latest_apply(project_code))


@router.get("/{project_code}/plan")
def plan_hosts_apply(
    project_code: str,
    ip: str = Query(default=HOSTS_PUBLISH_DEFAULT_IP),
    real_write: bool = Query(default=False),
) -> dict:
    return api_response_view.render(
        hosts_apply_service.plan_project_hosts_apply(
            project_code=project_code,
            ip_value=ip,
            real_write=real_write,
        )
    )


@router.post("/{project_code}/apply")
def apply_hosts_entry(
    project_code: str,
    ip: str = Query(default=HOSTS_PUBLISH_DEFAULT_IP),
    real_write: bool = Query(default=False),
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        hosts_apply_service.apply_project_hosts(
            project_code=project_code,
            ip_value=ip,
            real_write=real_write,
            dry_run=dry_run,
        )
    )


@router.get("/{project_code}/rollback-plan")
def plan_hosts_rollback(project_code: str) -> dict:
    return api_response_view.render(hosts_apply_service.plan_project_hosts_rollback(project_code))


@router.post("/{project_code}/rollback")
def rollback_hosts_entry(
    project_code: str,
    dry_run: bool = Query(default=True),
) -> dict:
    return api_response_view.render(
        hosts_apply_service.rollback_project_hosts(
            project_code=project_code,
            dry_run=dry_run,
        )
    )
