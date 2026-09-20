# 📄 Dosya Yolu: E:\JHoster\app\agent\services\component_service.py
# 📌 Amac: JHoster component manifestlerini is kurallariyla listeler ve detaylandirir
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Component katalog, runtime adapter detay ve kurulum plani service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from config.constants import SERVICE_ADAPTER_RUNTIME_KEY
from repositories.manifest_repository import ManifestRepository
from tools.manifest_validation_tool import ManifestValidationTool


class ComponentService:
    def __init__(
        self,
        manifest_repository: ManifestRepository,
        manifest_validation_tool: ManifestValidationTool,
    ) -> None:
        self.manifest_repository = manifest_repository
        self.manifest_validation_tool = manifest_validation_tool

    def list_components(self) -> dict[str, Any]:
        components = [
            self.manifest_validation_tool.normalize(manifest_item)
            for manifest_item in self.manifest_repository.get_all_manifests()
        ]
        sorted_components = sorted(components, key=lambda component: component["code"])

        return {
            "success": True,
            "count": len(sorted_components),
            "components": [self._to_summary(component) for component in sorted_components],
        }

    def get_component_detail(self, component_code: str) -> dict[str, Any]:
        component = self._find_component(component_code)

        if component is None:
            return self._not_found_response(component_code)

        return {
            "success": True,
            "component": component,
        }

    def get_component_plan(self, component_code: str) -> dict[str, Any]:
        component = self._find_component(component_code)

        if component is None:
            return self._not_found_response(component_code)

        return {
            "success": True,
            "component": self._to_summary(component),
            "installer": component.get("installer", {}),
            "plan": component.get("actions", []),
            "plan_only": True,
        }

    def _find_component(self, component_code: str) -> dict[str, Any] | None:
        manifest_item = self.manifest_repository.get_manifest_by_code(component_code)

        if manifest_item is None:
            return None

        return self.manifest_validation_tool.normalize(manifest_item)

    def _to_summary(self, component: dict[str, Any]) -> dict[str, Any]:
        return {
            "code": component.get("code"),
            "name": component.get("name"),
            "version": component.get("version"),
            "category": component.get("category"),
            "edition": component.get("edition"),
            "description": component.get("description"),
            "runtime_adapter": component.get(SERVICE_ADAPTER_RUNTIME_KEY),
            "actions_count": component.get("actions_count"),
            "valid": component.get("valid"),
        }

    def _not_found_response(self, component_code: str) -> dict[str, Any]:
        return {
            "success": False,
            "error": "component_not_found",
            "component_code": component_code,
        }
