# 📄 Dosya Yolu: E:\JHoster\app\agent\services\entitlement_provider.py
# 📌 Amac: PlanGateService ile entitlement kaynagi arasindaki public provider kontratini tanimlar
# 📌 Modul - Python
# Version: 3.80.0
# Aciklama: Community fallback ve private Pro adapter tarafinin ayni contract uzerinden state saglamasini zorunlu kilar
# Bagimli Oldugu Katman: Service | Model

from typing import Protocol

from models.entitlement_state import EntitlementState


class EntitlementProvider(Protocol):
    def get_entitlement_state(self) -> EntitlementState:
        ...
