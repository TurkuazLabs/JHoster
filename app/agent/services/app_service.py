# 📄 Dosya Yolu: E:\JHoster\app\agent\services\app_service.py
# 📌 Amac: Kurulu JHoster app/component kayitlarini is kurallariyla sunar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: App registry listeleme ve detay service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from repositories.app_registry_repository import AppRegistryRepository


class AppService:
    def __init__(self, app_registry_repository: AppRegistryRepository) -> None:
        self.app_registry_repository = app_registry_repository

    def list_apps(self) -> dict[str, Any]:
        apps = self.app_registry_repository.list_apps()

        return {
            "success": True,
            "count": len(apps),
            "apps": apps,
        }

    def get_app_detail(self, component_code: str) -> dict[str, Any]:
        app_item = self.app_registry_repository.get_app(component_code)

        if app_item is None:
            return {
                "success": False,
                "error": "app_not_found",
                "component_code": component_code,
            }

        return {
            "success": True,
            "app": app_item,
        }
