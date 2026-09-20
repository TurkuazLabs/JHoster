# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\service_adapters\adapter_registry.py
# 📌 Amac: Component runtime tipine gore uygun service adapter secimini yapar
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Simulated, planned ve guarded real local process adapter kayitlarini yonetir
# Bagimli Oldugu Katman: Tool

from typing import Any

from config.constants import (
    PACKAGE_CATEGORY_KEY,
    SERVICE_ADAPTER_MODE_APACHE,
    SERVICE_ADAPTER_MODE_MYSQL,
    SERVICE_ADAPTER_MODE_NGINX,
    SERVICE_ADAPTER_MODE_NODE,
    SERVICE_ADAPTER_MODE_PHP,
    SERVICE_ADAPTER_MODE_SIMULATED,
    SERVICE_ADAPTER_RUNTIME_KEY,
)
from tools.service_adapters.base_adapter import (
    BaseServiceAdapter,
    GuardedLocalProcessServiceAdapter,
    PlannedRuntimeServiceAdapter,
    SimulatedServiceAdapter,
)


class ServiceAdapterRegistryTool:
    def __init__(self) -> None:
        self.adapters = {
            SERVICE_ADAPTER_MODE_SIMULATED: SimulatedServiceAdapter(),
            SERVICE_ADAPTER_MODE_PHP: PlannedRuntimeServiceAdapter(
                SERVICE_ADAPTER_MODE_PHP,
                "PHP Runtime Adapter",
                "Prepared adapter for future PHP CGI/FPM process management.",
            ),
            SERVICE_ADAPTER_MODE_NGINX: PlannedRuntimeServiceAdapter(
                SERVICE_ADAPTER_MODE_NGINX,
                "Nginx Runtime Adapter",
                "Prepared adapter for future Nginx process management.",
            ),
            SERVICE_ADAPTER_MODE_APACHE: PlannedRuntimeServiceAdapter(
                SERVICE_ADAPTER_MODE_APACHE,
                "Apache Runtime Adapter",
                "Prepared adapter for future Apache process management.",
            ),
            SERVICE_ADAPTER_MODE_MYSQL: PlannedRuntimeServiceAdapter(
                SERVICE_ADAPTER_MODE_MYSQL,
                "MySQL Runtime Adapter",
                "Prepared adapter for future MySQL process management.",
            ),
            SERVICE_ADAPTER_MODE_NODE: PlannedRuntimeServiceAdapter(
                SERVICE_ADAPTER_MODE_NODE,
                "Node.js Runtime Adapter",
                "Prepared adapter for future Node.js process management.",
            ),
        }
        self.real_adapters = {
            SERVICE_ADAPTER_MODE_PHP: GuardedLocalProcessServiceAdapter(
                SERVICE_ADAPTER_MODE_PHP,
                "PHP Guarded Local Process Adapter",
                "Guarded adapter for PHP local executable management.",
            ),
            SERVICE_ADAPTER_MODE_NGINX: GuardedLocalProcessServiceAdapter(
                SERVICE_ADAPTER_MODE_NGINX,
                "Nginx Guarded Local Process Adapter",
                "Guarded adapter for Nginx local executable management.",
            ),
            SERVICE_ADAPTER_MODE_APACHE: GuardedLocalProcessServiceAdapter(
                SERVICE_ADAPTER_MODE_APACHE,
                "Apache Guarded Local Process Adapter",
                "Guarded adapter for Apache local executable management.",
            ),
            SERVICE_ADAPTER_MODE_MYSQL: GuardedLocalProcessServiceAdapter(
                SERVICE_ADAPTER_MODE_MYSQL,
                "MySQL Guarded Local Process Adapter",
                "Guarded adapter for MySQL local executable management.",
            ),
            SERVICE_ADAPTER_MODE_NODE: GuardedLocalProcessServiceAdapter(
                SERVICE_ADAPTER_MODE_NODE,
                "Node.js Guarded Local Process Adapter",
                "Guarded adapter for Node.js local executable management.",
            ),
        }
        self.category_map = {
            "php": SERVICE_ADAPTER_MODE_PHP,
            "nginx": SERVICE_ADAPTER_MODE_NGINX,
            "apache": SERVICE_ADAPTER_MODE_APACHE,
            "mysql": SERVICE_ADAPTER_MODE_MYSQL,
            "node": SERVICE_ADAPTER_MODE_NODE,
            "nodejs": SERVICE_ADAPTER_MODE_NODE,
        }

    def list_adapters(self) -> list[dict[str, Any]]:
        planned = [
            self.adapters[adapter_key].describe()
            for adapter_key in sorted(self.adapters.keys())
        ]
        real = [
            self.real_adapters[adapter_key].describe()
            for adapter_key in sorted(self.real_adapters.keys())
        ]
        return planned + real

    def get_adapter_detail(self, adapter_key: str) -> dict[str, Any] | None:
        normalized_key = str(adapter_key).strip()
        adapter = self.adapters.get(normalized_key)
        if adapter is None:
            adapter = self.real_adapters.get(normalized_key)

        if adapter is None:
            return None

        return adapter.describe()

    def resolve_adapter(self, app_item: dict[str, Any], prefer_real: bool = False) -> BaseServiceAdapter:
        adapter_key = self.resolve_adapter_key(app_item)
        if prefer_real:
            category_value = str(app_item.get(PACKAGE_CATEGORY_KEY, "")).strip().lower()
            real_adapter_key = self.category_map.get(category_value, adapter_key)
            if real_adapter_key in self.real_adapters:
                return self.real_adapters[real_adapter_key]
        return self.adapters.get(adapter_key, self.adapters[SERVICE_ADAPTER_MODE_SIMULATED])

    def resolve_adapter_key(self, app_item: dict[str, Any]) -> str:
        explicit_adapter = str(app_item.get(SERVICE_ADAPTER_RUNTIME_KEY, "")).strip().lower()
        if explicit_adapter in self.adapters:
            return explicit_adapter

        category_value = str(app_item.get(PACKAGE_CATEGORY_KEY, "")).strip().lower()
        mapped_adapter = self.category_map.get(category_value)
        if mapped_adapter:
            return mapped_adapter

        return SERVICE_ADAPTER_MODE_SIMULATED
