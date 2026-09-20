# 📄 Dosya Yolu: E:\JHoster\app\agent\services\service_adapter_service.py
# 📌 Amac: Runtime service adapter katalogunu is kurallariyla sunar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Adapter liste ve detay islemlerini tool katmani uzerinden yonetir
# Bagimli Oldugu Katman: Service

from typing import Any

from tools.service_adapters.adapter_registry import ServiceAdapterRegistryTool


class ServiceAdapterService:
    def __init__(self, service_adapter_registry_tool: ServiceAdapterRegistryTool) -> None:
        self.service_adapter_registry_tool = service_adapter_registry_tool

    def list_adapters(self) -> dict[str, Any]:
        adapters = self.service_adapter_registry_tool.list_adapters()

        return {
            "success": True,
            "count": len(adapters),
            "adapters": adapters,
        }

    def get_adapter_detail(self, adapter_key: str) -> dict[str, Any]:
        adapter = self.service_adapter_registry_tool.get_adapter_detail(adapter_key)

        if adapter is None:
            return {
                "success": False,
                "error": "service_adapter_not_found",
                "adapter_key": adapter_key,
            }

        return {
            "success": True,
            "adapter": adapter,
        }
