# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\web_server_port_guard_tool.py
# 📌 Amac: Apache ve Nginx icin ortak 80/443 port cakisma korumasini hesaplar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Web server frontend servislerinin ayni public portlari birlikte sahiplenmesini engelleyen port guard tool katmani
# Bagimli Oldugu Katman: Tool

from typing import Any

from config.constants import (
    PROCESS_MESSAGE_WEB_SERVER_PORT_CONFLICT,
    PROCESS_STATUS_RUNNING,
    SERVICE_CODE_APACHE,
    SERVICE_CODE_NGINX,
    WEB_SERVER_FRONTEND_CODES,
    WEB_SERVER_HTTP_PORT_KEY,
    WEB_SERVER_HTTPS_PORT_KEY,
    WEB_SERVER_PORT_GUARD_ALLOWED_KEY,
    WEB_SERVER_PORT_GUARD_MESSAGE_KEY,
    WEB_SERVER_PORT_GUARD_POLICY_KEY,
    WEB_SERVER_PORT_GUARD_POLICY_VALUE,
    WEB_SERVER_PORT_GUARD_PUBLIC_PORTS_KEY,
    WEB_SERVER_PORT_GUARD_REQUESTED_PORTS_KEY,
    WEB_SERVER_PORT_GUARD_REQUESTED_SERVICE_KEY,
    WEB_SERVER_PORT_GUARD_RUNNING_PORTS_KEY,
    WEB_SERVER_PORT_GUARD_RUNNING_SERVICE_KEY,
    WEB_SERVER_PORT_GUARD_SHARED_PORTS_KEY,
    WEB_SERVER_PORT_GUARD_OK_MESSAGE,
    WEB_SERVER_PORTS_KEY,
    WEB_SERVER_PUBLIC_PORTS,
)


class WebServerPortGuardTool:
    def validate_start(
        self,
        component_code: str,
        requested_app: dict[str, Any],
        all_apps: list[dict[str, Any]],
        all_processes: list[dict[str, Any]],
    ) -> dict[str, Any]:
        requested_code = self._normalize_code(component_code)
        if requested_code not in WEB_SERVER_FRONTEND_CODES:
            return self._allowed_response(requested_code, [])

        requested_ports = self._extract_ports(requested_app)
        running_conflict = self._find_running_frontend_conflict(
            requested_code,
            requested_ports,
            all_apps,
            all_processes,
        )

        if running_conflict is None:
            return self._allowed_response(requested_code, requested_ports)

        return {
            WEB_SERVER_PORT_GUARD_ALLOWED_KEY: False,
            WEB_SERVER_PORT_GUARD_MESSAGE_KEY: PROCESS_MESSAGE_WEB_SERVER_PORT_CONFLICT,
            WEB_SERVER_PORT_GUARD_REQUESTED_SERVICE_KEY: requested_code,
            WEB_SERVER_PORT_GUARD_RUNNING_SERVICE_KEY: running_conflict.get(WEB_SERVER_PORT_GUARD_RUNNING_SERVICE_KEY),
            WEB_SERVER_PORT_GUARD_REQUESTED_PORTS_KEY: requested_ports,
            WEB_SERVER_PORT_GUARD_RUNNING_PORTS_KEY: running_conflict.get(WEB_SERVER_PORT_GUARD_RUNNING_PORTS_KEY, []),
            WEB_SERVER_PORT_GUARD_SHARED_PORTS_KEY: running_conflict.get(WEB_SERVER_PORT_GUARD_SHARED_PORTS_KEY, []),
            WEB_SERVER_PORT_GUARD_PUBLIC_PORTS_KEY: WEB_SERVER_PUBLIC_PORTS,
            WEB_SERVER_PORT_GUARD_POLICY_KEY: WEB_SERVER_PORT_GUARD_POLICY_VALUE,
        }

    def _find_running_frontend_conflict(
        self,
        requested_code: str,
        requested_ports: list[int],
        all_apps: list[dict[str, Any]],
        all_processes: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        requested_public_ports = self._public_ports(requested_ports)
        if not requested_public_ports:
            return None

        for process_item in all_processes:
            running_code = self._normalize_code(str(process_item.get("code", "")))
            if running_code == requested_code:
                continue

            if running_code not in WEB_SERVER_FRONTEND_CODES:
                continue

            if str(process_item.get("status", "")).strip() != PROCESS_STATUS_RUNNING:
                continue

            running_app = self._find_app(all_apps, running_code)
            running_ports = self._extract_ports(running_app)
            shared_ports = sorted(set(requested_public_ports).intersection(self._public_ports(running_ports)))
            if shared_ports:
                return {
                    WEB_SERVER_PORT_GUARD_RUNNING_SERVICE_KEY: running_code,
                    WEB_SERVER_PORT_GUARD_RUNNING_PORTS_KEY: running_ports,
                    WEB_SERVER_PORT_GUARD_SHARED_PORTS_KEY: shared_ports,
                }

        return None

    def _allowed_response(self, requested_code: str, requested_ports: list[int]) -> dict[str, Any]:
        return {
            WEB_SERVER_PORT_GUARD_ALLOWED_KEY: True,
            WEB_SERVER_PORT_GUARD_MESSAGE_KEY: WEB_SERVER_PORT_GUARD_OK_MESSAGE,
            WEB_SERVER_PORT_GUARD_REQUESTED_SERVICE_KEY: requested_code,
            WEB_SERVER_PORT_GUARD_REQUESTED_PORTS_KEY: requested_ports,
            WEB_SERVER_PORT_GUARD_PUBLIC_PORTS_KEY: WEB_SERVER_PUBLIC_PORTS,
            WEB_SERVER_PORT_GUARD_POLICY_KEY: WEB_SERVER_PORT_GUARD_POLICY_VALUE,
        }

    def _find_app(self, all_apps: list[dict[str, Any]], component_code: str) -> dict[str, Any]:
        for app_item in all_apps:
            if self._normalize_code(str(app_item.get("code", ""))) == component_code:
                return app_item
        return {}

    def _extract_ports(self, app_item: dict[str, Any]) -> list[int]:
        ports_value = app_item.get(WEB_SERVER_PORTS_KEY, {})
        ports: list[int] = []

        if isinstance(ports_value, dict):
            self._append_port(ports, ports_value.get(WEB_SERVER_HTTP_PORT_KEY))
            self._append_port(ports, ports_value.get(WEB_SERVER_HTTPS_PORT_KEY))
            for port_value in ports_value.values():
                self._append_port(ports, port_value)

        if isinstance(ports_value, list):
            for port_value in ports_value:
                self._append_port(ports, port_value)

        return sorted(set(ports))

    def _append_port(self, ports: list[int], port_value: Any) -> None:
        try:
            normalized_port = int(str(port_value).strip())
        except (TypeError, ValueError):
            return

        if normalized_port > 0:
            ports.append(normalized_port)

    def _public_ports(self, ports: list[int]) -> list[int]:
        return sorted(set(ports).intersection(WEB_SERVER_PUBLIC_PORTS))

    def _normalize_code(self, component_code: str) -> str:
        normalized_code = str(component_code or "").strip().lower()
        if normalized_code == SERVICE_CODE_APACHE:
            return SERVICE_CODE_APACHE
        if normalized_code == SERVICE_CODE_NGINX:
            return SERVICE_CODE_NGINX
        return normalized_code
