# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\cache_repository.py
# 📌 Amac: JHoster cache klasorundeki paket dosyalarini listeler
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Cache dosya okuma, listeleme ve dosya meta bilgisi repository katmani
# Bagimli Oldugu Katman: Repo

from pathlib import Path
from typing import Any

from config.constants import ZIP_FILE_EXTENSION


class CacheRepository:
    def __init__(self, cache_path: Path, root_path: Path) -> None:
        self.cache_path = cache_path
        self.root_path = root_path.resolve()

    def list_cache_files(self) -> list[dict[str, Any]]:
        if not self.cache_path.exists():
            return []

        cache_items: list[dict[str, Any]] = []

        for file_path in sorted(self.cache_path.rglob("*")):
            if file_path.is_file():
                cache_items.append(self._to_cache_item(file_path))

        return cache_items

    def list_archives(self) -> list[dict[str, Any]]:
        return [
            cache_item
            for cache_item in self.list_cache_files()
            if str(cache_item.get("extension")) == ZIP_FILE_EXTENSION
        ]

    def _to_cache_item(self, file_path: Path) -> dict[str, Any]:
        stat_result = file_path.stat()

        return {
            "path": self._format_path(file_path),
            "relative_path": self._format_relative_path(file_path),
            "name": file_path.name,
            "extension": file_path.suffix.lower(),
            "size_bytes": stat_result.st_size,
        }

    def _format_relative_path(self, file_path: Path) -> str:
        try:
            relative_path = file_path.resolve().relative_to(self.root_path)
            return str(relative_path).replace("/", "\\")
        except ValueError:
            return self._format_path(file_path)

    def _format_path(self, file_path: Path) -> str:
        return str(file_path).replace("/", "\\")
