# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\mysql_database_tool.py
# 📌 Amac: JHoster kokundeki mysql.exe ile guvenli database create islemi yapar
# 📌 Modul - Python
# Version: 3.78.0
# Aciklama: Shell kullanmadan executable discovery, dry-run plan ve CREATE DATABASE adapter islemlerini uygular
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import os
import re
import subprocess


class MysqlDatabaseTool:
    IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9_]{1,64}$")
    DEFAULT_TIMEOUT_SECONDS = 20

    def __init__(self, root_path: Path, allow_shell_commands: bool) -> None:
        self.root_path = root_path.resolve()
        self.allow_shell_commands = bool(allow_shell_commands)

    def build_plan(
        self,
        database_name: str,
        host: str,
        port: int,
        admin_user: str,
    ) -> dict[str, Any]:
        normalized_name = str(database_name or "").strip()
        executable = self._find_mysql_executable()
        valid_identifier = bool(self.IDENTIFIER_PATTERN.fullmatch(normalized_name))
        return {
            "success": valid_identifier,
            "status": "ready" if valid_identifier and executable is not None else "attention",
            "database_name": normalized_name,
            "host": str(host or "127.0.0.1").strip(),
            "port": int(port),
            "admin_user": str(admin_user or "root").strip() or "root",
            "identifier_valid": valid_identifier,
            "mysql_executable_found": executable is not None,
            "mysql_executable": self._to_relative(executable) if executable is not None else "",
            "shell_execution_allowed": self.allow_shell_commands,
            "password_required_for_apply": True,
        }

    def create_database(
        self,
        database_name: str,
        host: str,
        port: int,
        admin_user: str,
        admin_password: str,
        approved: bool,
        dry_run: bool,
    ) -> dict[str, Any]:
        plan = self.build_plan(database_name, host, port, admin_user)
        if dry_run:
            return {
                "success": bool(plan.get("identifier_valid", False)),
                "status": "planned",
                "message": "mysql database create dry run only",
                "plan": plan,
            }

        if not approved:
            return {"success": False, "status": "rejected", "error": "provisioning_apply_approval_required", "plan": plan}
        if not self.allow_shell_commands:
            return {"success": False, "status": "rejected", "error": "shell_commands_disabled", "plan": plan}
        if not plan.get("identifier_valid", False):
            return {"success": False, "status": "rejected", "error": "mysql_database_name_invalid", "plan": plan}
        executable = self._find_mysql_executable()
        if executable is None:
            return {"success": False, "status": "rejected", "error": "mysql_executable_not_found", "plan": plan}
        if not str(admin_password or ""):
            return {"success": False, "status": "rejected", "error": "mysql_admin_password_required", "plan": plan}

        sql = f"CREATE DATABASE IF NOT EXISTS `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        environment = os.environ.copy()
        environment["MYSQL_PWD"] = str(admin_password)
        command = [
            str(executable),
            "--protocol=tcp",
            "--host",
            str(host or "127.0.0.1"),
            "--port",
            str(int(port)),
            "--user",
            str(admin_user or "root"),
            "--batch",
            "--skip-column-names",
        ]
        completed = subprocess.run(
            command,
            input=sql,
            text=True,
            capture_output=True,
            timeout=self.DEFAULT_TIMEOUT_SECONDS,
            check=False,
            shell=False,
            env=environment,
            cwd=str(executable.parent),
        )
        stderr = str(completed.stderr or "").strip()
        return {
            "success": completed.returncode == 0,
            "status": "created" if completed.returncode == 0 else "failed",
            "message": "mysql database create completed" if completed.returncode == 0 else "mysql database create failed",
            "database_name": database_name,
            "return_code": completed.returncode,
            "error": stderr[:500] if completed.returncode != 0 else "",
            "mysql_executable": self._to_relative(executable),
        }

    def _find_mysql_executable(self) -> Path | None:
        candidates = [
            self.root_path / "bin" / "mysql" / "mysql.exe",
            self.root_path / "bin" / "mysql" / "bin" / "mysql.exe",
        ]
        mysql_root = self.root_path / "bin" / "mysql"
        if mysql_root.exists():
            candidates.extend(sorted(mysql_root.glob("**/mysql.exe")))

        seen: set[str] = set()
        for candidate in candidates:
            resolved = candidate.resolve()
            key = str(resolved).lower()
            if key in seen:
                continue
            seen.add(key)
            if not self._is_inside_root(resolved):
                continue
            if resolved.is_file():
                return resolved
        return None

    def _is_inside_root(self, path: Path) -> bool:
        try:
            path.relative_to(self.root_path)
            return True
        except ValueError:
            return False

    def _to_relative(self, path: Path) -> str:
        try:
            return str(path.resolve().relative_to(self.root_path)).replace("/", "\\")
        except ValueError:
            return str(path).replace("/", "\\")
