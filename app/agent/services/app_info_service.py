# 📄 Dosya Yolu: E:\JHoster\app\agent\services\app_info_service.py
# 📌 Amac: JHoster agent ana sayfa ve uygulama bilgisini is kurallariyla hazirlar
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Root endpoint icin service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import COMPONENT_ROUTE_PREFIX, DOCS_ROUTE_PATH, HEALTH_ROUTE_PREFIX
from config.settings import AppSettings


class AppInfoService:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    def get_root_page_data(self) -> dict[str, Any]:
        base_url = f"http://{self.settings.server_host}:{self.settings.server_port}"

        return {
            "app_name": self.settings.app_name,
            "app_version": self.settings.app_version,
            "status": "running",
            "health_url": f"{base_url}{HEALTH_ROUTE_PREFIX}",
            "components_url": f"{base_url}{COMPONENT_ROUTE_PREFIX}",
            "docs_url": f"{base_url}{DOCS_ROUTE_PATH}",
        }
