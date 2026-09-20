# 📄 Dosya Yolu: E:\JHoster\app\agent\services\web_server_profile_service.py
# 📌 Amac: JHoster web server profil secim is kurallarini yonetir
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Apache/Nginx aktif web server secimini ve ortak www document root ayarini merkezi profile donusturen service katmani
# Bagimli Oldugu Katman: Service

from datetime import datetime, timezone
from typing import Any

from config.constants import (
    WEB_SERVER_PROFILE_DEFAULT,
    WEB_SERVER_PROFILE_ERROR_NOT_FOUND,
    WEB_SERVER_PROFILE_ERROR_NOT_READY,
    WEB_SERVER_PROFILE_MESSAGE_DRY_RUN,
    WEB_SERVER_PROFILE_MESSAGE_REJECTED,
    WEB_SERVER_PROFILE_MESSAGE_SELECTED,
    WEB_SERVER_PROFILE_STATUS_PLANNED,
    WEB_SERVER_PROFILE_STATUS_REJECTED,
    WEB_SERVER_PROFILE_STATUS_SELECTED,
    WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY,
    WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
)
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from tools.web_server_profile_tool import WebServerProfileTool


class WebServerProfileService:
    def __init__(
        self,
        web_server_profile_registry_repository: WebServerProfileRegistryRepository,
        web_server_profile_tool: WebServerProfileTool,
    ) -> None:
        self.web_server_profile_registry_repository = web_server_profile_registry_repository
        self.web_server_profile_tool = web_server_profile_tool

    def list_profiles(self) -> dict[str, Any]:
        profiles = self.web_server_profile_tool.list_profiles()
        current_profile = self._get_current_or_default_record()

        return {
            "success": True,
            "count": len(profiles),
            "current": current_profile,
            "profiles": profiles,
        }

    def get_profile(self, server_code: str) -> dict[str, Any]:
        normalized_code = self.web_server_profile_tool.normalize_server_code(server_code)
        profile = self.web_server_profile_tool.get_profile(normalized_code)

        if profile is None:
            return {
                "success": False,
                "error": WEB_SERVER_PROFILE_ERROR_NOT_FOUND,
                "server_code": normalized_code,
            }

        return {
            "success": True,
            "profile": profile,
        }

    def get_current_profile(self) -> dict[str, Any]:
        return {
            "success": True,
            "current": self._get_current_or_default_record(),
        }

    def plan_select_profile(self, server_code: str) -> dict[str, Any]:
        plan = self.web_server_profile_tool.build_selection_plan(server_code)

        if not plan.get("profile_found", False):
            return {
                "success": False,
                "status": WEB_SERVER_PROFILE_STATUS_REJECTED,
                "error": WEB_SERVER_PROFILE_ERROR_NOT_FOUND,
                "message": WEB_SERVER_PROFILE_MESSAGE_REJECTED,
                "plan": plan,
            }

        if not plan.get("supported", False):
            return {
                "success": False,
                "status": WEB_SERVER_PROFILE_STATUS_REJECTED,
                "error": WEB_SERVER_PROFILE_ERROR_NOT_FOUND,
                "message": WEB_SERVER_PROFILE_MESSAGE_REJECTED,
                "plan": plan,
            }

        if not plan.get("ready", False):
            return {
                "success": False,
                "status": WEB_SERVER_PROFILE_STATUS_REJECTED,
                "error": WEB_SERVER_PROFILE_ERROR_NOT_READY,
                "message": WEB_SERVER_PROFILE_MESSAGE_REJECTED,
                "plan": plan,
            }

        if not plan.get("safe", False):
            return {
                "success": False,
                "status": WEB_SERVER_PROFILE_STATUS_REJECTED,
                "message": WEB_SERVER_PROFILE_MESSAGE_REJECTED,
                "plan": plan,
            }

        return {
            "success": True,
            "status": WEB_SERVER_PROFILE_STATUS_PLANNED,
            "message": WEB_SERVER_PROFILE_MESSAGE_DRY_RUN,
            "plan": plan,
        }

    def select_profile(self, server_code: str, dry_run: bool) -> dict[str, Any]:
        plan_result = self.plan_select_profile(server_code)

        if not plan_result.get("success", False):
            return plan_result

        plan = plan_result.get("plan", {})
        profile = plan.get("profile", {})
        now_value = datetime.now(timezone.utc).isoformat()
        selection_record = {
            "server_code": plan.get("server_code"),
            "server_name": profile.get("name"),
            "profile_status": profile.get("status"),
            "adapter_stage": profile.get("adapter_stage"),
            "default": profile.get("default", False),
            "status": WEB_SERVER_PROFILE_STATUS_SELECTED,
            "selected_from": "web_server_profile_service",
            "selected_at": now_value,
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
        }

        if dry_run:
            return {
                "success": True,
                "status": WEB_SERVER_PROFILE_STATUS_PLANNED,
                "message": WEB_SERVER_PROFILE_MESSAGE_DRY_RUN,
                "plan": plan,
                "selection": selection_record,
            }

        stored_record = self.web_server_profile_registry_repository.append_record(selection_record)

        return {
            "success": True,
            "status": WEB_SERVER_PROFILE_STATUS_SELECTED,
            "message": WEB_SERVER_PROFILE_MESSAGE_SELECTED,
            "plan": plan,
            "selection": stored_record,
        }

    def _get_current_or_default_record(self) -> dict[str, Any]:
        current_record = self.web_server_profile_registry_repository.get_current_profile()

        if current_record is not None:
            return current_record

        default_profile = self.web_server_profile_tool.get_profile(WEB_SERVER_PROFILE_DEFAULT) or {}

        return {
            "server_code": WEB_SERVER_PROFILE_DEFAULT,
            "server_name": default_profile.get("name", WEB_SERVER_PROFILE_DEFAULT),
            "profile_status": default_profile.get("status", "ready"),
            "adapter_stage": default_profile.get("adapter_stage"),
            "default": True,
            "status": WEB_SERVER_PROFILE_STATUS_SELECTED,
            "selected_from": "web_server_profile_service_default",
            WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY: WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE,
        }
