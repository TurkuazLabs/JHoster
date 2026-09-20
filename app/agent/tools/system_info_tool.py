# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\system_info_tool.py
# 📌 Amac: Isletim sistemi ve Python calisma ortami bilgilerini okur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Dis dunya ve sistem bilgisi adaptorudur
# Bagimli Oldugu Katman: Tool

import platform
import sys
from typing import Any

import psutil


class SystemInfoTool:
    def get_system_info(self) -> dict[str, Any]:
        virtual_memory = psutil.virtual_memory()

        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "python_version": sys.version.split()[0],
            "cpu_count": psutil.cpu_count(logical=True),
            "memory_total_mb": round(virtual_memory.total / 1024 / 1024),
        }
