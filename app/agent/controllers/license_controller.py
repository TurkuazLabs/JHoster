# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\license_controller.py
# 📌 Amac: JHoster lisans ve plan durumunu HTTP endpoint olarak sunar
# 📌 Modul - FileType
# Version: 3.65.0
# Aciklama: Controller sadece plan durumunu servis katmanindan alir ve API cevabina aktarir ve feature registry alanini sunar
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.constants import LICENSE_ROUTE_PREFIX, LICENSE_ROUTE_TAG
from config.settings import AppSettings
from repositories.license_state_repository import LicenseStateRepository
from repositories.project_registry_repository import ProjectRegistryRepository
from services.plan_gate_service import PlanGateService
from views.api_response_view import ApiResponseView


router = APIRouter(prefix=LICENSE_ROUTE_PREFIX, tags=[LICENSE_ROUTE_TAG])

settings = AppSettings.load()
project_registry_repository = ProjectRegistryRepository(settings.storage_path)
plan_gate_service = PlanGateService(
    license_state_repository=LicenseStateRepository(settings.storage_path),
    project_registry_repository=project_registry_repository,
)
api_response_view = ApiResponseView()


@router.get("")
def get_license_state() -> dict:
    license_summary = plan_gate_service.get_license_summary()
    return api_response_view.render(
        {
            "success": True,
            "plan_key": license_summary.get("plan_key"),
            "plan_label": license_summary.get("plan_label"),
            "active_project_count": license_summary.get("active_project_count"),
            "max_active_projects": license_summary.get("max_active_projects"),
            "usage_label": license_summary.get("usage_label"),
            "can_create_project": license_summary.get("allowed"),
            "message": license_summary.get("message"),
            "upgrade_hint": license_summary.get("upgrade_hint"),
            "feature_flags": license_summary.get("feature_flags"),
            "feature_registry": license_summary.get("feature_registry"),
        }
    )
