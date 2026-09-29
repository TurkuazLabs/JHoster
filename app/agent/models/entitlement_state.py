# 📄 Dosya Yolu: E:\JHoster\app\agent\models\entitlement_state.py
# 📌 Amac: JHoster Community ile paid entitlement provider arasindaki normalize edilmis state modelini tanimlar
# 📌 Modul - Python
# Version: 3.80.0
# Aciklama: Plan, feature, source ve validity bilgisini immutable model olarak tasir
# Bagimli Oldugu Katman: Model

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class EntitlementState:
    plan_key: str
    features: frozenset[str]
    source: str
    valid: bool

    @classmethod
    def create(
        cls,
        plan_key: str,
        features: Iterable[str],
        source: str,
        valid: bool,
    ) -> "EntitlementState":
        normalized_plan = str(plan_key).strip().lower()
        normalized_features = frozenset(
            str(feature).strip().lower()
            for feature in features
            if str(feature).strip()
        )
        return cls(
            plan_key=normalized_plan,
            features=normalized_features,
            source=str(source).strip(),
            valid=bool(valid),
        )

    def has_feature(self, feature_code: str) -> bool:
        return str(feature_code).strip().lower() in self.features
