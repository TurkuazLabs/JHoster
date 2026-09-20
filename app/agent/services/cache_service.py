# 📄 Dosya Yolu: E:\JHoster\app\agent\services\cache_service.py
# 📌 Amac: JHoster cache dosyalarini is kurallariyla listeler
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Cache repository verisini API icin ozetleyen service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from repositories.cache_repository import CacheRepository


class CacheService:
    def __init__(self, cache_repository: CacheRepository) -> None:
        self.cache_repository = cache_repository

    def list_cache(self) -> dict[str, Any]:
        cache_items = self.cache_repository.list_cache_files()
        archive_items = self.cache_repository.list_archives()

        return {
            "success": True,
            "count": len(cache_items),
            "archive_count": len(archive_items),
            "cache": cache_items,
        }
