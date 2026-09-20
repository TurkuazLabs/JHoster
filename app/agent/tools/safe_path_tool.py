# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\safe_path_tool.py
# 📌 Amac: Executor icin dosya yollarini JHoster kok dizini icinde guvenli cozer
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Path traversal ve proje disi yazma riskini engelleyen tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
import os
import re


WINDOWS_ABSOLUTE_PATH_PATTERN = re.compile(r"^[A-Za-z]:[\\/]")


class SafePathTool:
    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()

    def resolve_inside_root(self, path_value: Any) -> Path:
        raw_path_value = str(path_value or "").strip()

        if not raw_path_value:
            raise ValueError("empty_path")

        if WINDOWS_ABSOLUTE_PATH_PATTERN.match(raw_path_value) and os.name != "nt":
            raise ValueError("windows_absolute_path_not_allowed_on_this_os")

        candidate_path = Path(raw_path_value)

        if not candidate_path.is_absolute():
            candidate_path = self.root_path / candidate_path

        resolved_path = candidate_path.resolve()

        if not self._is_inside_root(resolved_path):
            raise ValueError("path_outside_project_root")

        return resolved_path

    def _is_inside_root(self, file_path: Path) -> bool:
        try:
            file_path.relative_to(self.root_path)
            return True
        except ValueError:
            return False
