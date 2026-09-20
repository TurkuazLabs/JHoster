# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\project_registry_repository.py
# 📌 Amac: JHoster proje kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 3.63.0
# Aciklama: Proje registry listeleme, detay okuma ve upsert islemlerini data/jhoster altinda yonetir
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import PROJECT_REGISTRY_FILE_NAME, PROJECT_STATUS_ACTIVE


class ProjectRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / PROJECT_REGISTRY_FILE_NAME

    def list_projects(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        projects = registry_data.get("projects", [])

        if not isinstance(projects, list):
            return []

        return sorted(projects, key=lambda item: str(item.get("code", "")))

    def count_active_projects(self) -> int:
        active_count = 0

        for project_item in self.list_projects():
            project_status = str(project_item.get("status", PROJECT_STATUS_ACTIVE)).strip().lower()
            if project_status == PROJECT_STATUS_ACTIVE:
                active_count += 1

        return active_count

    def get_project(self, project_code: str) -> dict[str, Any] | None:
        normalized_code = str(project_code).strip().lower()

        for project_item in self.list_projects():
            if str(project_item.get("code")) == normalized_code:
                return project_item

        return None

    def upsert_project(self, project_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        projects = registry_data.get("projects", [])

        if not isinstance(projects, list):
            projects = []

        project_code = str(project_data.get("code", "")).strip().lower()
        if not project_code:
            raise ValueError("project code is required")

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            "status": PROJECT_STATUS_ACTIVE,
            "created_at": now_value,
            **project_data,
            "updated_at": now_value,
        }

        replaced = False
        for index, project_item in enumerate(projects):
            if str(project_item.get("code")) == project_code:
                stored_item = {
                    **project_item,
                    **project_data,
                    "updated_at": now_value,
                }
                projects[index] = stored_item
                replaced = True
                break

        if not replaced:
            projects.append(stored_item)

        registry_data["projects"] = projects
        self._write_registry(registry_data)
        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"projects": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"projects": []}

        if "projects" not in loaded_data and "www" in loaded_data:
            loaded_data["projects"] = loaded_data.get("www", [])
            loaded_data.pop("www", None)

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
