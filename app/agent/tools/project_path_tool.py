# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\project_path_tool.py
# 📌 Amac: JHoster www project klasor adlarini ve yollarini guvenli sekilde cozer
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Project code dogrulama, path traversal engelleme ve project klasor hazirligi yapar
# Bagimli Oldugu Katman: Tool

from pathlib import Path
import re

from config.constants import (
    PROJECT_CONFIG_FILE_NAME,
    PROJECT_INDEX_FILE_NAME,
    PROJECT_PUBLIC_DIRECTORY_NAME,
    PROJECT_STATUS_CREATED,
    USER_PROJECTS_DIRECTORY_NAME,
)


class ProjectPathTool:
    PROJECT_CODE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{1,62}[a-z0-9]$")

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()
        self.www_root_path = (self.root_path / USER_PROJECTS_DIRECTORY_NAME).resolve()

    def normalize_project_code(self, project_code: str) -> str:
        return str(project_code).strip().lower().replace(" ", "-")

    def is_valid_project_code(self, project_code: str) -> bool:
        normalized_code = self.normalize_project_code(project_code)
        return bool(self.PROJECT_CODE_PATTERN.match(normalized_code))

    def build_project_plan(self, project_code: str) -> dict:
        normalized_code = self.normalize_project_code(project_code)
        project_path = (self.www_root_path / normalized_code).resolve()
        public_path = (project_path / PROJECT_PUBLIC_DIRECTORY_NAME).resolve()

        return {
            "project_code": normalized_code,
            "project_path": self._to_relative(project_path),
            "document_root": self._to_relative(public_path),
            "config_file": self._to_relative(project_path / PROJECT_CONFIG_FILE_NAME),
            "index_file": self._to_relative(public_path / PROJECT_INDEX_FILE_NAME),
            "safe": self._is_inside_www_root(project_path) and self._is_inside_www_root(public_path),
        }

    def create_project_files(self, project_code: str, project_name: str, runtime_family: str, active_runtime: dict) -> dict:
        plan = self.build_project_plan(project_code)
        if not plan.get("safe", False):
            return {
                "success": False,
                "status": "blocked",
                "message": "project path is outside www",
                "plan": plan,
            }

        project_path = (self.www_root_path / plan["project_code"]).resolve()
        public_path = (project_path / PROJECT_PUBLIC_DIRECTORY_NAME).resolve()
        project_path.mkdir(parents=True, exist_ok=True)
        public_path.mkdir(parents=True, exist_ok=True)

        config_content = self._build_project_config(project_name, runtime_family, active_runtime)
        index_content = self._build_index_content(project_name, runtime_family)

        (project_path / PROJECT_CONFIG_FILE_NAME).write_text(config_content, encoding="utf-8")
        (public_path / PROJECT_INDEX_FILE_NAME).write_text(index_content, encoding="utf-8")

        return {
            "success": True,
            "status": PROJECT_STATUS_CREATED,
            "message": "project files created",
            "plan": plan,
            "files": 2,
        }

    def _is_inside_www_root(self, target_path: Path) -> bool:
        try:
            target_path.resolve().relative_to(self.www_root_path)
            return True
        except ValueError:
            return False

    def _to_relative(self, target_path: Path) -> str:
        try:
            return str(target_path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(target_path.resolve())

    def _build_project_config(self, project_name: str, runtime_family: str, active_runtime: dict) -> str:
        return (
            "project:\n"
            f"  name: {project_name}\n"
            f"  runtime_family: {runtime_family}\n"
            f"  runtime_component: {active_runtime.get('component_code')}\n"
            f"  runtime_version: {active_runtime.get('version')}\n"
        )

    def _build_index_content(self, project_name: str, runtime_family: str) -> str:
        return (
            "<!doctype html>\n"
            "<html lang=\"en\">\n"
            "<head>\n"
            "  <meta charset=\"utf-8\">\n"
            f"  <title>{project_name}</title>\n"
            "</head>\n"
            "<body>\n"
            f"  <h1>{project_name}</h1>\n"
            f"  <p>JHoster project ready. Runtime family: {runtime_family}</p>\n"
            "</body>\n"
            "</html>\n"
        )
