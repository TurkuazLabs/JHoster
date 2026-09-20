# 📄 Dosya Yolu: E:\JHoster\app\agent\services\folder_layout_service.py
# 📌 Amac: JHoster sade klasor standardi is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller isteklerini folder layout tool katmanina aktarir ve dry-run/apply sonucunu olusturur
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import (
    FOLDER_LAYOUT_MESSAGE_APPLIED,
    FOLDER_LAYOUT_MESSAGE_DRY_RUN,
    FOLDER_LAYOUT_MESSAGE_PLAN_READY,
    FOLDER_LAYOUT_MESSAGE_READY,
    FOLDER_LAYOUT_STATUS_APPLIED,
    FOLDER_LAYOUT_STATUS_PLANNED,
)
from tools.folder_layout_tool import FolderLayoutTool


class FolderLayoutService:
    def __init__(self, folder_layout_tool: FolderLayoutTool) -> None:
        self.folder_layout_tool = folder_layout_tool

    def get_standard(self) -> dict[str, Any]:
        standard = self.folder_layout_tool.get_standard()
        return {
            "success": True,
            "message": FOLDER_LAYOUT_MESSAGE_READY,
            **standard,
        }

    def plan_layout(self) -> dict[str, Any]:
        plan = self.folder_layout_tool.build_plan()
        return {
            "success": True,
            "status": FOLDER_LAYOUT_STATUS_PLANNED,
            "message": FOLDER_LAYOUT_MESSAGE_PLAN_READY,
            "plan": plan,
        }

    def apply_layout(self, dry_run: bool) -> dict[str, Any]:
        if dry_run:
            plan = self.folder_layout_tool.build_plan()
            return {
                "success": True,
                "status": FOLDER_LAYOUT_STATUS_PLANNED,
                "message": FOLDER_LAYOUT_MESSAGE_DRY_RUN,
                "plan": plan,
            }

        result = self.folder_layout_tool.apply()
        return {
            "success": True,
            "status": FOLDER_LAYOUT_STATUS_APPLIED,
            "message": FOLDER_LAYOUT_MESSAGE_APPLIED,
            **result,
        }
