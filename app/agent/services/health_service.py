# 📄 Dosya Yolu: E:\JHoster\app\agent\services\health_service.py
# 📌 Amac: JHoster agent saglik durumunu is kurallariyla hazirlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Health endpoint icin service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from repositories.state_repository import StateRepository
from tools.system_info_tool import SystemInfoTool


class HealthService:
    def __init__(
        self,
        state_repository: StateRepository,
        system_info_tool: SystemInfoTool,
    ) -> None:
        self.state_repository = state_repository
        self.system_info_tool = system_info_tool

    def get_health_status(self) -> dict[str, Any]:
        agent_state = self.state_repository.get_state()
        system_info = self.system_info_tool.get_system_info()

        return {
            "success": True,
            "status": agent_state.get("state"),
            "system": system_info,
        }
