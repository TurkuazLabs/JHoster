# 📄 Dosya Yolu: E:\JHoster\app\agent\services\plan_gate_service.py
# 📌 Amac: Community ve paid plan limitlerini entitlement provider state'ine gore uygular
# 📌 Modul - Python
# Version: 3.80.0
# Aciklama: Local Community fallback veya private Pro provider state'ini feature bazli fail-closed plan gate kararina donusturur
# Bagimli Oldugu Katman: Service | Model | Repo

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
    LICENSE_FEATURE_UNLIMITED_SITES,
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
from models.entitlement_state import EntitlementState
from repositories.project_registry_repository import ProjectRegistryRepository
from services.entitlement_provider import EntitlementProvider


class PlanGateService:
    def __init__(
        self,
        entitlement_provider: EntitlementProvider,
        project_registry_repository: ProjectRegistryRepository,
    ) -> None:
        self.entitlement_provider = entitlement_provider
        self.project_registry_repository = project_registry_repository

    def can_create_project(self) -> dict[str, Any]:
        entitlement_state = self.entitlement_provider.get_entitlement_state()
        return self._build_project_gate(entitlement_state)

    def get_license_summary(self) -> dict[str, Any]:
        entitlement_state = self.entitlement_provider.get_entitlement_state()
        plan_gate = self._build_project_gate(entitlement_state)
        plan_key = self._resolve_effective_plan(entitlement_state)
        active_project_count = int(plan_gate.get("active_project_count", 0))
        max_active_projects = int(plan_gate.get("max_active_projects", LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS))

        return {
            **plan_gate,
            "plan_label": self._resolve_plan_label(plan_key),
            "usage_label": self._build_usage_label(active_project_count, max_active_projects),
            "upgrade_hint": LICENSE_UPGRADE_HINT,
            "feature_flags": self._build_feature_flags(entitlement_state),
            "feature_registry": self._build_feature_registry(entitlement_state),
            "entitlement_source": entitlement_state.source,
            "entitlement_valid": entitlement_state.valid,
        }

    def _build_project_gate(self, entitlement_state: EntitlementState) -> dict[str, Any]:
        plan_key = self._resolve_effective_plan(entitlement_state)
        active_project_count = self.project_registry_repository.count_active_projects()
        unlimited_sites = self._is_feature_enabled(
            entitlement_state,
            LICENSE_FEATURE_UNLIMITED_SITES,
        )

        if unlimited_sites:
            return self._build_result(
                True,
                plan_key,
                active_project_count,
                LICENSE_PRO_UNLIMITED_LIMIT,
                LICENSE_MESSAGE_CREATE_ALLOWED,
            )

        allowed = active_project_count < LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS
        message = LICENSE_MESSAGE_CREATE_ALLOWED if allowed else LICENSE_MESSAGE_COMMUNITY_SITE_LIMIT
        return self._build_result(
            allowed,
            plan_key,
            active_project_count,
            LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS,
            message,
        )

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

    def _resolve_effective_plan(self, entitlement_state: EntitlementState) -> str:
        if entitlement_state.valid and entitlement_state.plan_key == LICENSE_PLAN_PRO:
            return LICENSE_PLAN_PRO

        return LICENSE_DEFAULT_PLAN

    def _resolve_plan_label(self, plan_key: str) -> str:
        if plan_key == LICENSE_PLAN_PRO:
            return LICENSE_LABEL_PRO

        return LICENSE_LABEL_COMMUNITY

    def _build_usage_label(self, active_project_count: int, max_active_projects: int) -> str:
        if max_active_projects == LICENSE_PRO_UNLIMITED_LIMIT:
            return f"{active_project_count} / {LICENSE_USAGE_UNLIMITED_LABEL}"

        return f"{active_project_count} / {max_active_projects}"

    def _is_feature_enabled(
        self,
        entitlement_state: EntitlementState,
        feature_code: str,
    ) -> bool:
        return entitlement_state.valid and entitlement_state.has_feature(feature_code)

    def _build_feature_flags(self, entitlement_state: EntitlementState) -> dict[str, bool]:
        return {
            LICENSE_FEATURE_SITE_LIMIT: True,
            LICENSE_FEATURE_ADVANCED_SSL: self._is_feature_enabled(
                entitlement_state,
                LICENSE_FEATURE_ADVANCED_SSL,
            ),
            LICENSE_FEATURE_AUTOMATED_BACKUP: self._is_feature_enabled(
                entitlement_state,
                LICENSE_FEATURE_AUTOMATED_BACKUP,
            ),
            LICENSE_FEATURE_ADVANCED_DNS: self._is_feature_enabled(
                entitlement_state,
                LICENSE_FEATURE_ADVANCED_DNS,
            ),
            LICENSE_FEATURE_AI_OLLAMA: self._is_feature_enabled(
                entitlement_state,
                LICENSE_FEATURE_AI_OLLAMA,
            ),
        }

    def _build_feature_registry(self, entitlement_state: EntitlementState) -> list[dict[str, Any]]:
        feature_flags = self._build_feature_flags(entitlement_state)
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
