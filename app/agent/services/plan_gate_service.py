# 📄 Dosya Yolu: E:\JHoster\app\agent\services\plan_gate_service.py
# 📌 Amac: Community ve Pro plan limitlerini is kurali olarak uygular
# 📌 Modul - FileType
# Version: 3.65.0
# Aciklama: Proje/site olusturma haklarini lisans plani ve aktif proje sayisina gore kontrol eder ve lisans ozetini ve Pro feature registry bilgisini uretir
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import (
    LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS,
    LICENSE_DEFAULT_PLAN,
    LICENSE_FEATURE_ADVANCED_DNS,
    LICENSE_FEATURE_ADVANCED_SSL,
    LICENSE_FEATURE_AI_OLLAMA,
    LICENSE_FEATURE_AUTOMATED_BACKUP,
    LICENSE_FEATURE_SITE_LIMIT,
    LICENSE_FEATURE_STATUS_INCLUDED,
    LICENSE_FEATURE_STATUS_PRO_LOCKED,
    LICENSE_FEATURES,
    LICENSE_LABEL_COMMUNITY,
    LICENSE_LABEL_PRO,
    LICENSE_MESSAGE_COMMUNITY_SITE_LIMIT,
    LICENSE_MESSAGE_CREATE_ALLOWED,
    LICENSE_PLAN_PRO,
    LICENSE_PRO_UNLIMITED_LIMIT,
    LICENSE_UPGRADE_HINT,
    LICENSE_USAGE_UNLIMITED_LABEL,
)
from repositories.license_state_repository import LicenseStateRepository
from repositories.project_registry_repository import ProjectRegistryRepository


class PlanGateService:
    def __init__(
        self,
        license_state_repository: LicenseStateRepository,
        project_registry_repository: ProjectRegistryRepository,
    ) -> None:
        self.license_state_repository = license_state_repository
        self.project_registry_repository = project_registry_repository

    def can_create_project(self) -> dict[str, Any]:
        plan_key = self.license_state_repository.get_plan_key()
        active_project_count = self.project_registry_repository.count_active_projects()

        if plan_key == LICENSE_PLAN_PRO:
            return self._build_result(True, plan_key, active_project_count, LICENSE_PRO_UNLIMITED_LIMIT, LICENSE_MESSAGE_CREATE_ALLOWED)

        allowed = active_project_count < LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS
        message = LICENSE_MESSAGE_CREATE_ALLOWED if allowed else LICENSE_MESSAGE_COMMUNITY_SITE_LIMIT

        return self._build_result(allowed, plan_key, active_project_count, LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS, message)

    def get_license_summary(self) -> dict[str, Any]:
        plan_gate = self.can_create_project()
        plan_key = str(plan_gate.get("plan_key", LICENSE_DEFAULT_PLAN)).strip().lower()
        active_project_count = int(plan_gate.get("active_project_count", 0))
        max_active_projects = int(plan_gate.get("max_active_projects", LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS))

        return {
            **plan_gate,
            "plan_label": self._resolve_plan_label(plan_key),
            "usage_label": self._build_usage_label(active_project_count, max_active_projects),
            "upgrade_hint": LICENSE_UPGRADE_HINT,
            "feature_flags": self._build_feature_flags(plan_key),
            "feature_registry": self._build_feature_registry(plan_key),
        }

    def _build_result(
        self,
        allowed: bool,
        plan_key: str,
        active_project_count: int,
        max_active_projects: int,
        message: str,
    ) -> dict[str, Any]:
        return {
            "allowed": allowed,
            "plan_key": plan_key,
            "active_project_count": active_project_count,
            "max_active_projects": max_active_projects,
            "message": message,
        }

    def _resolve_plan_label(self, plan_key: str) -> str:
        if plan_key == LICENSE_PLAN_PRO:
            return LICENSE_LABEL_PRO

        return LICENSE_LABEL_COMMUNITY

    def _build_usage_label(self, active_project_count: int, max_active_projects: int) -> str:
        if max_active_projects == LICENSE_PRO_UNLIMITED_LIMIT:
            return f"{active_project_count} / {LICENSE_USAGE_UNLIMITED_LABEL}"

        return f"{active_project_count} / {max_active_projects}"

    def _build_feature_flags(self, plan_key: str) -> dict[str, bool]:
        pro_enabled = plan_key == LICENSE_PLAN_PRO
        return {
            LICENSE_FEATURE_SITE_LIMIT: True,
            LICENSE_FEATURE_ADVANCED_SSL: pro_enabled,
            LICENSE_FEATURE_AUTOMATED_BACKUP: pro_enabled,
            LICENSE_FEATURE_ADVANCED_DNS: pro_enabled,
            LICENSE_FEATURE_AI_OLLAMA: pro_enabled,
        }

    def _build_feature_registry(self, plan_key: str) -> list[dict[str, Any]]:
        feature_flags = self._build_feature_flags(plan_key)
        registry_items = []

        for feature in LICENSE_FEATURES:
            code = str(feature.get("code", ""))
            enabled = bool(feature_flags.get(code, False))
            registry_items.append(
                {
                    **feature,
                    "enabled": enabled,
                    "status_label": LICENSE_FEATURE_STATUS_INCLUDED if enabled else LICENSE_FEATURE_STATUS_PRO_LOCKED,
                }
            )

        return registry_items
