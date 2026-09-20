# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\quick_app_template_tool.py
# 📌 Amac: Quick App template ve stack secimli planlarini guvenli sekilde uretir
# 📌 Modul - FileType
# Version: 3.72.0
# Aciklama: PHP empty, Laravel, WordPress, OpenCart 3.x ve Node/Vite scaffold dosyalarini stack metadata ile www altinda olusturur
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import re

from config.constants import (
    PROJECT_CONFIG_FILE_NAME,
    PROJECT_PUBLIC_DIRECTORY_NAME,
    QUICK_APP_TEMPLATE_LARAVEL,
    QUICK_APP_TEMPLATE_NODE_VITE,
    QUICK_APP_TEMPLATE_OPENCART3,
    QUICK_APP_TEMPLATE_PHP_EMPTY,
    QUICK_APP_TEMPLATE_WORDPRESS,
    USER_PROJECTS_DIRECTORY_NAME,
)
from tools.project_path_tool import ProjectPathTool


class QuickAppTemplateTool:
    def __init__(self, root_path: Path, project_path_tool: ProjectPathTool) -> None:
        self.root_path = root_path.resolve()
        self.www_root_path = (self.root_path / USER_PROJECTS_DIRECTORY_NAME).resolve()
        self.project_path_tool = project_path_tool

    def list_templates(self) -> list[dict[str, Any]]:
        return [
            self._template_php_empty(),
            self._template_laravel(),
            self._template_wordpress(),
            self._template_opencart3(),
            self._template_node_vite(),
        ]

    def get_template(self, template_code: str) -> dict[str, Any] | None:
        normalized_code = str(template_code).strip().lower()
        for template_item in self.list_templates():
            if str(template_item.get("code")) == normalized_code:
                return template_item
        return None

    def build_plan(self, project_code: str, project_name: str, template_code: str, domain: str, port: int, stack_plan: dict[str, Any] | None = None) -> dict[str, Any]:
        normalized_code = self.project_path_tool.normalize_project_code(project_code)
        template_item = self.get_template(template_code)
        project_plan = self.project_path_tool.build_project_plan(normalized_code)

        file_items: list[dict[str, Any]] = []
        if template_item is not None:
            file_items = self._build_file_items(normalized_code, project_name, template_item, stack_plan)

        return {
            "project_code": normalized_code,
            "project_name": str(project_name).strip() or normalized_code,
            "template_code": str(template_code).strip().lower(),
            "template": template_item,
            "domain": str(domain).strip(),
            "port": int(port),
            "project_path": project_plan.get("project_path"),
            "document_root": project_plan.get("document_root"),
            "config_file": project_plan.get("config_file"),
            "safe": bool(project_plan.get("safe", False)),
            "files": file_items,
            "file_count": len(file_items),
            "mode": "scaffold_only",
            "stack_plan": stack_plan or {},
            "stack_label": str((stack_plan or {}).get("label", "")),
        }

    def create_scaffold(self, project_code: str, project_name: str, template_code: str, domain: str, port: int, stack_plan: dict[str, Any] | None = None) -> dict[str, Any]:
        plan = self.build_plan(project_code, project_name, template_code, domain, port, stack_plan)
        if not plan.get("safe", False):
            return {
                "success": False,
                "status": "blocked",
                "message": "quick app path is outside www",
                "plan": plan,
            }

        normalized_code = str(plan.get("project_code", ""))
        project_path = (self.www_root_path / normalized_code).resolve()
        if not self._is_inside_www_root(project_path):
            return {
                "success": False,
                "status": "blocked",
                "message": "quick app root is outside www",
                "plan": plan,
            }

        written_files: list[str] = []
        for file_item in plan.get("files", []):
            relative_path = str(file_item.get("path", "")).strip()
            content = str(file_item.get("content", ""))
            relative_parts = [part for part in re.split(r"[\\/]", relative_path) if part]
            target_path = (project_path / Path(*relative_parts)).resolve()
            if not self._is_inside_www_root(target_path):
                return {
                    "success": False,
                    "status": "blocked",
                    "message": "quick app file path is outside www",
                    "file": relative_path,
                    "plan": plan,
                }

            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding="utf-8")
            written_files.append(self._to_relative(target_path))

        return {
            "success": True,
            "status": "created",
            "message": "quick app scaffold created",
            "plan": plan,
            "written_files": written_files,
            "file_count": len(written_files),
        }

    def _build_file_items(self, project_code: str, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        template_code = str(template_item.get("code", ""))
        if template_code == QUICK_APP_TEMPLATE_PHP_EMPTY:
            return self._php_empty_files(project_name, template_item, stack_plan)
        if template_code == QUICK_APP_TEMPLATE_LARAVEL:
            return self._laravel_files(project_name, template_item, stack_plan)
        if template_code == QUICK_APP_TEMPLATE_WORDPRESS:
            return self._wordpress_files(project_name, template_item, stack_plan)
        if template_code == QUICK_APP_TEMPLATE_OPENCART3:
            return self._opencart3_files(project_name, template_item, stack_plan)
        if template_code == QUICK_APP_TEMPLATE_NODE_VITE:
            return self._node_vite_files(project_code, project_name, template_item, stack_plan)
        return []

    def _base_config_file(self, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> dict[str, str]:
        template_code = str(template_item.get("code", ""))
        runtime_family = str(template_item.get("runtime_family", ""))
        content = (
            "project:\n"
            f"  name: {project_name}\n"
            f"  template_code: {template_code}\n"
            f"  runtime_family: {runtime_family}\n"
            "  created_by: quick_app_service\n"
            "  mode: scaffold_only\n"
            + self._stack_config_yaml(stack_plan)
        )
        return {"path": PROJECT_CONFIG_FILE_NAME, "content": content}

    def _php_empty_files(self, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        return [
            self._base_config_file(project_name, template_item, stack_plan),
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/index.php",
                "content": "<?php\n\necho '<h1>" + self._escape_php(project_name) + "</h1>';\necho '<p>JHoster PHP empty site ready.</p>';\n",
            },
        ]

    def _laravel_files(self, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        return [
            self._base_config_file(project_name, template_item, stack_plan),
            {
                "path": "README.md",
                "content": "# " + project_name + "\n\nJHoster Laravel scaffold-only workspace. Attach Composer install flow from Package Center when available.\n",
            },
            {
                "path": "composer.json",
                "content": "{\n  \"name\": \"jhoster/laravel-scaffold\",\n  \"description\": \"JHoster Laravel scaffold-only workspace\",\n  \"type\": \"project\"\n}\n",
            },
            {
                "path": ".env.example",
                "content": "APP_NAME=JHosterLaravel\nAPP_ENV=local\nAPP_KEY=\nAPP_DEBUG=true\nAPP_URL=http://localhost\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/index.php",
                "content": "<?php\n\necho '<h1>JHoster Laravel scaffold</h1>';\necho '<p>Install Laravel core in the next installer step.</p>';\n",
            },
        ]

    def _wordpress_files(self, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        return [
            self._base_config_file(project_name, template_item, stack_plan),
            {
                "path": "README.md",
                "content": "# " + project_name + "\n\nJHoster WordPress scaffold-only workspace. Attach WordPress core package from Package Center when available.\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/index.php",
                "content": "<?php\n\necho '<h1>JHoster WordPress scaffold</h1>';\necho '<p>WordPress core is not downloaded in scaffold-only mode.</p>';\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/wp-config-sample.php",
                "content": "<?php\ndefine('DB_NAME', 'database_name_here');\ndefine('DB_USER', 'username_here');\ndefine('DB_PASSWORD', 'password_here');\ndefine('DB_HOST', 'localhost');\n",
            },
        ]

    def _opencart3_files(self, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        return [
            self._base_config_file(project_name, template_item, stack_plan),
            {
                "path": "README.md",
                "content": "# " + project_name + "\n\nJHoster OpenCart 3.x scaffold-only workspace. Use this for OpenCart 3.x module/dev www.\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/index.php",
                "content": "<?php\n\necho '<h1>JHoster OpenCart 3.x scaffold</h1>';\necho '<p>OpenCart core package will be attached by Quick Add later.</p>';\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/config.php",
                "content": "<?php\n// JHoster OpenCart 3.x scaffold-only config stub.\n",
            },
            {
                "path": f"{PROJECT_PUBLIC_DIRECTORY_NAME}/admin/config.php",
                "content": "<?php\n// JHoster OpenCart 3.x admin scaffold-only config stub.\n",
            },
        ]

    def _node_vite_files(self, project_code: str, project_name: str, template_item: dict[str, Any], stack_plan: dict[str, Any] | None) -> list[dict[str, str]]:
        package_name = project_code.replace("_", "-")
        return [
            self._base_config_file(project_name, template_item, stack_plan),
            {
                "path": "package.json",
                "content": "{\n  \"name\": \"" + package_name + "\",\n  \"version\": \"0.1.0\",\n  \"type\": \"module\",\n  \"scripts\": {\n    \"dev\": \"vite\",\n    \"build\": \"vite build\"\n  },\n  \"dependencies\": {},\n  \"devDependencies\": {}\n}\n",
            },
            {
                "path": "index.html",
                "content": "<!doctype html>\n<html lang=\"en\">\n<head><meta charset=\"utf-8\"><title>" + project_name + "</title></head>\n<body><div id=\"app\"></div><script type=\"module\" src=\"/src/main.js\"></script></body>\n</html>\n",
            },
            {
                "path": "src/main.js",
                "content": "document.querySelector('#app').innerHTML = '<h1>JHoster Vite scaffold ready</h1>';\n",
            },
        ]

    def _template_php_empty(self) -> dict[str, Any]:
        return self._template(QUICK_APP_TEMPLATE_PHP_EMPTY, "PHP Empty Site", "php", "Plain PHP public/index.php scaffold")

    def _template_laravel(self) -> dict[str, Any]:
        return self._template(QUICK_APP_TEMPLATE_LARAVEL, "Laravel Scaffold", "php", "Laravel-ready scaffold without Composer download")

    def _template_wordpress(self) -> dict[str, Any]:
        return self._template(QUICK_APP_TEMPLATE_WORDPRESS, "WordPress Scaffold", "php", "WordPress-ready scaffold without core download")

    def _template_opencart3(self) -> dict[str, Any]:
        return self._template(QUICK_APP_TEMPLATE_OPENCART3, "OpenCart 3.x Scaffold", "php", "OpenCart 3.x developer scaffold")

    def _template_node_vite(self) -> dict[str, Any]:
        return self._template(QUICK_APP_TEMPLATE_NODE_VITE, "Node Vite Scaffold", "node", "Node/Vite starter scaffold")

    def _template(self, code: str, name: str, runtime_family: str, description: str) -> dict[str, Any]:
        return {
            "code": code,
            "name": name,
            "runtime_family": runtime_family,
            "description": description,
            "mode": "scaffold_only",
            "requires_download": False,
        }

    def _stack_config_yaml(self, stack_plan: dict[str, Any] | None) -> str:
        safe_stack = stack_plan or {}
        return (
            "  stack:\n"
            f"    web_server: {safe_stack.get('web_server', 'apache')}\n"
            f"    mysql: {self._bool_yaml(safe_stack.get('include_mysql', True))}\n"
            f"    php: {self._bool_yaml(safe_stack.get('include_php', True))}\n"
            f"    mailpit: {self._bool_yaml(safe_stack.get('include_mailpit', False))}\n"
        )

    def _bool_yaml(self, value: Any) -> str:
        return "true" if bool(value) else "false"

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

    def _escape_php(self, value: str) -> str:
        return str(value).replace("'", "\\'")
