# 📄 Dosya Yolu: E:\JHoster\app\agent\test-entitlement-provider.py
# 📌 Amac: Community fallback ve paid entitlement provider gate davranisini regression olarak dogrulamak
# 📌 Modul - Python
# Version: 3.80.0
# Aciklama: Local plan bypass'ini, feature bazli Pro gate'i ve invalid entitlement fail-closed davranisini test eder
# Bagimli Oldugu Katman: Tool | Service | Repo | Model

from pathlib import Path
from tempfile import TemporaryDirectory
import json

from config.constants import (
    LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS,
    LICENSE_FEATURE_ADVANCED_SSL,
    LICENSE_FEATURE_UNLIMITED_SITES,
    LICENSE_PLAN_COMMUNITY,
    LICENSE_PLAN_PRO,
    LICENSE_PRO_UNLIMITED_LIMIT,
)
from models.entitlement_state import EntitlementState
from repositories.license_state_repository import LicenseStateRepository
from repositories.local_entitlement_repository import LocalEntitlementRepository
from services.plan_gate_service import PlanGateService


class StubProjectRegistry:
    def __init__(self, active_project_count: int) -> None:
        self.active_project_count = active_project_count

    def count_active_projects(self) -> int:
        return self.active_project_count


class StaticEntitlementProvider:
    def __init__(self, state: EntitlementState) -> None:
        self.state = state

    def get_entitlement_state(self) -> EntitlementState:
        return self.state


def assert_local_paid_plan_cannot_unlock_runtime() -> None:
    with TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir)
        license_path = storage_path / "license_state.json"
        license_path.write_text(
            json.dumps(
                {
                    "plan_key": LICENSE_PLAN_PRO,
                    "features": [
                        LICENSE_FEATURE_UNLIMITED_SITES,
                        LICENSE_FEATURE_ADVANCED_SSL,
                    ],
                }
            ),
            encoding="utf-8",
        )

        provider = LocalEntitlementRepository(
            license_state_repository=LicenseStateRepository(storage_path),
        )
        state = provider.get_entitlement_state()

        assert state.plan_key == LICENSE_PLAN_COMMUNITY
        assert not state.has_feature(LICENSE_FEATURE_UNLIMITED_SITES)
        assert not state.has_feature(LICENSE_FEATURE_ADVANCED_SSL)
        assert state.source == "local_community_fallback"


def assert_explicit_dev_provider_can_model_paid_state() -> None:
    with TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir)
        license_path = storage_path / "license_state.json"
        license_path.write_text(
            json.dumps(
                {
                    "plan_key": LICENSE_PLAN_PRO,
                    "features": [
                        LICENSE_FEATURE_UNLIMITED_SITES,
                        LICENSE_FEATURE_ADVANCED_SSL,
                    ],
                }
            ),
            encoding="utf-8",
        )

        provider = LocalEntitlementRepository(
            license_state_repository=LicenseStateRepository(storage_path),
            allow_paid_plans=True,
        )
        state = provider.get_entitlement_state()

        assert state.plan_key == LICENSE_PLAN_PRO
        assert state.has_feature(LICENSE_FEATURE_UNLIMITED_SITES)
        assert state.has_feature(LICENSE_FEATURE_ADVANCED_SSL)
        assert state.source == "local_dev"


def assert_paid_plan_requires_feature_for_unlimited_sites() -> None:
    provider = StaticEntitlementProvider(
        EntitlementState.create(
            plan_key=LICENSE_PLAN_PRO,
            features=[LICENSE_FEATURE_ADVANCED_SSL],
            source="test_paid_without_unlimited",
            valid=True,
        )
    )
    service = PlanGateService(
        entitlement_provider=provider,
        project_registry_repository=StubProjectRegistry(
            LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS
        ),
    )

    gate = service.can_create_project()
    assert gate["allowed"] is False
    assert gate["max_active_projects"] == LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS


def assert_unlimited_sites_feature_unlocks_limit() -> None:
    provider = StaticEntitlementProvider(
        EntitlementState.create(
            plan_key=LICENSE_PLAN_PRO,
            features=[
                LICENSE_FEATURE_UNLIMITED_SITES,
                LICENSE_FEATURE_ADVANCED_SSL,
            ],
            source="test_paid",
            valid=True,
        )
    )
    service = PlanGateService(
        entitlement_provider=provider,
        project_registry_repository=StubProjectRegistry(50),
    )

    summary = service.get_license_summary()
    assert summary["allowed"] is True
    assert summary["max_active_projects"] == LICENSE_PRO_UNLIMITED_LIMIT
    assert summary["feature_flags"][LICENSE_FEATURE_ADVANCED_SSL] is True
    assert summary["entitlement_valid"] is True
    assert summary["entitlement_source"] == "test_paid"


def assert_invalid_paid_state_fails_closed() -> None:
    provider = StaticEntitlementProvider(
        EntitlementState.create(
            plan_key=LICENSE_PLAN_PRO,
            features=[
                LICENSE_FEATURE_UNLIMITED_SITES,
                LICENSE_FEATURE_ADVANCED_SSL,
            ],
            source="test_invalid",
            valid=False,
        )
    )
    service = PlanGateService(
        entitlement_provider=provider,
        project_registry_repository=StubProjectRegistry(
            LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS
        ),
    )

    summary = service.get_license_summary()
    assert summary["plan_key"] == LICENSE_PLAN_COMMUNITY
    assert summary["allowed"] is False
    assert summary["max_active_projects"] == LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS
    assert summary["feature_flags"][LICENSE_FEATURE_ADVANCED_SSL] is False
    assert summary["entitlement_valid"] is False


def main() -> None:
    checks = [
        assert_local_paid_plan_cannot_unlock_runtime,
        assert_explicit_dev_provider_can_model_paid_state,
        assert_paid_plan_requires_feature_for_unlimited_sites,
        assert_unlimited_sites_feature_unlocks_limit,
        assert_invalid_paid_state_fails_closed,
    ]

    for check in checks:
        check()
        print(f"PASS: {check.__name__}")

    print(f"ENTITLEMENT_PROVIDER_TEST_OK: {len(checks)}/{len(checks)}")


if __name__ == "__main__":
    main()
