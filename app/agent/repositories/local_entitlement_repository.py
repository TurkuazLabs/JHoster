# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\local_entitlement_repository.py
# 📌 Amac: Legacy local license_state.json verisini guvenli Community/dev entitlement provider olarak sunar
# 📌 Modul - Python
# Version: 3.80.0
# Aciklama: Runtime varsayilaninda local dosyanin paid plan acmasini engeller; explicit test/dev modunda paid state okunabilir
# Bagimli Oldugu Katman: Repo | Model

from config.constants import (
    LICENSE_DEFAULT_PLAN,
    LICENSE_FEATURE_ADVANCED_DNS,
    LICENSE_FEATURE_ADVANCED_SSL,
    LICENSE_FEATURE_AI_OLLAMA,
    LICENSE_FEATURE_AUTOMATED_BACKUP,
    LICENSE_FEATURE_SITE_LIMIT,
    LICENSE_FEATURE_UNLIMITED_SITES,
    LICENSE_PLAN_PRO,
)
from models.entitlement_state import EntitlementState
from repositories.license_state_repository import LicenseStateRepository


class LocalEntitlementRepository:
    def __init__(
        self,
        license_state_repository: LicenseStateRepository,
        allow_paid_plans: bool = False,
    ) -> None:
        self.license_state_repository = license_state_repository
        self.allow_paid_plans = bool(allow_paid_plans)

    def get_entitlement_state(self) -> EntitlementState:
        local_state = self.license_state_repository.get_license_state()
        plan_key = str(local_state.get("plan_key", LICENSE_DEFAULT_PLAN)).strip().lower()

        if plan_key == LICENSE_PLAN_PRO and self.allow_paid_plans:
            configured_features = local_state.get("features")
            if isinstance(configured_features, list):
                paid_features = configured_features
            else:
                paid_features = [
                    LICENSE_FEATURE_SITE_LIMIT,
                    LICENSE_FEATURE_UNLIMITED_SITES,
                    LICENSE_FEATURE_ADVANCED_SSL,
                    LICENSE_FEATURE_AUTOMATED_BACKUP,
                    LICENSE_FEATURE_ADVANCED_DNS,
                    LICENSE_FEATURE_AI_OLLAMA,
                ]

            return EntitlementState.create(
                plan_key=LICENSE_PLAN_PRO,
                features=paid_features,
                source="local_dev",
                valid=True,
            )

        return EntitlementState.create(
            plan_key=LICENSE_DEFAULT_PLAN,
            features=[LICENSE_FEATURE_SITE_LIMIT],
            source="local_community_fallback",
            valid=True,
        )
