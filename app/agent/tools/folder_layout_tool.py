# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\folder_layout_tool.py
# 📌 Amac: JHoster sade root layout klasorlerini planlar ve guvenli sekilde olusturur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: app, bin, data, etc, logs, tmp, www, backup ve cache klasor standardini uygular
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any

from config.constants import LEGACY_TOP_LEVEL_DIRECTORIES, SIMPLIFIED_ROOT_DIRECTORIES


class FolderLayoutTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()

    def get_standard(self) -> dict[str, Any]:
        return {
            "root_path": str(self.root_path),
            "root_directories": [self._directory_payload(directory_name) for directory_name in SIMPLIFIED_ROOT_DIRECTORIES],
            "legacy_directories": [self._legacy_directory_payload(directory_name) for directory_name in LEGACY_TOP_LEVEL_DIRECTORIES],
            "mapping": self._mapping(),
        }

    def build_plan(self) -> dict[str, Any]:
        standard = self.get_standard()
        missing_directories = [
            item for item in standard.get("root_directories", [])
            if not bool(item.get("exists", False))
        ]
        existing_legacy_directories = [
            item for item in standard.get("legacy_directories", [])
            if bool(item.get("exists", False))
        ]

        return {
            "root_path": str(self.root_path),
            "safe": True,
            "missing_count": len(missing_directories),
            "legacy_count": len(existing_legacy_directories),
            "missing_directories": missing_directories,
            "legacy_directories": existing_legacy_directories,
            "actions": self._build_actions(missing_directories),
            "mapping": standard.get("mapping", []),
        }

    def apply(self) -> dict[str, Any]:
        plan = self.build_plan()
        created_directories: list[str] = []
        for action in plan.get("actions", []):
            relative_path = str(action.get("path", "")).strip()
            if not relative_path:
                continue

            target_path = (self.root_path / relative_path).resolve()
            if not self._is_inside_root(target_path):
                continue

            target_path.mkdir(parents=True, exist_ok=True)
            created_directories.append(relative_path)

        return {
            "success": True,
            "created_count": len(created_directories),
            "created_directories": created_directories,
            "plan": plan,
        }

    def _directory_payload(self, directory_name: str) -> dict[str, Any]:
        target_path = (self.root_path / directory_name).resolve()
        return {
            "name": directory_name,
            "path": directory_name,
            "absolute_path": str(target_path),
            "exists": target_path.exists() and target_path.is_dir(),
            "purpose": self._purpose(directory_name),
        }

    def _legacy_directory_payload(self, directory_name: str) -> dict[str, Any]:
        target_path = (self.root_path / directory_name).resolve()
        return {
            "name": directory_name,
            "path": directory_name,
            "absolute_path": str(target_path),
            "exists": target_path.exists() and target_path.is_dir(),
            "suggested_target": self._legacy_target(directory_name),
        }

    def _build_actions(self, missing_directories: list[dict[str, Any]]) -> list[dict[str, str]]:
        return [
            {
                "type": "ensure_directory",
                "path": str(item.get("path", "")),
                "description": "Create missing standard root directory",
            }
            for item in missing_directories
        ]

    def _mapping(self) -> list[dict[str, str]]:
        return [
            {"from": "agent", "to": "app/agent", "mode": "source_move"},
            {"from": "desktop", "to": "app/desktop", "mode": "source_move"},
            {"from": "modules", "to": "app/modules", "mode": "source_move"},
            {"from": "templates", "to": "app/templates", "mode": "source_move"},
            {"from": "themes", "to": "app/themes", "mode": "source_move"},
            {"from": "docs", "to": "app/docs", "mode": "source_move"},
            {"from": "changelog", "to": "app/changelog", "mode": "source_move"},
            {"from": "www", "to": "www", "mode": "runtime_root"},
            {"from": "runtimes", "to": "bin", "mode": "versioned_portable"},
            {"from": "services", "to": "bin", "mode": "versioned_portable"},
            {"from": "packages", "to": "cache/packages", "mode": "cache"},
            {"from": "ssl", "to": "etc/ssl", "mode": "config"},
            {"from": "databases", "to": "data/mysql", "mode": "data"},
            {"from": "data/jhoster", "to": "data/jhoster", "mode": "state"},
        ]

    def _purpose(self, directory_name: str) -> str:
        purposes = {
            "app": "JHoster agent, desktop, docs, templates and internal resources",
            "bin": "Portable services, runtimes and tools with versioned folders",
            "data": "Persistent state and service data",
            "etc": "Generated and editable configuration files",
            "logs": "Agent, desktop and service logs",
            "tmp": "Temporary runtime files",
            "www": "Local web www and document roots",
            "backup": "Project, database and config backups",
            "cache": "Downloaded packages, manifests and installer cache",
        }
        return purposes.get(directory_name, "JHoster standard directory")

    def _legacy_target(self, directory_name: str) -> str:
        legacy_targets = {
            "apps": "bin or app/resources",
            "config": "etc/jhoster",
            "databases": "data/mysql or backup/mysql",
            "language": "app/language",
            "modules": "app/modules",
            "packages": "cache/packages",
            "www": "www",
            "readme": "app/readme",
            "runtimes": "bin",
            "scripts": "app/scripts",
            "services": "bin",
            "snapshot": "backup/snapshot",
            "ssl": "etc/ssl",
            "templates": "app/templates",
            "themes": "app/themes",
            "tools": "app/tools",
            "updater": "app/updater",
            "usr": "data/user",
        }
        return legacy_targets.get(directory_name, "app")

    def _is_inside_root(self, target_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(self.root_path)
            return True
        except ValueError:
            return False
