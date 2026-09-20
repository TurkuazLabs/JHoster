# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\admin_privilege_tool.py
# 📌 Amac: Windows admin yetkisini guvenli sekilde kontrol eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Hosts apply gibi sistem dosyasi islemleri icin platform ve admin bilgisini saglar
# Bagimli Oldugu Katman: Tool

from typing import Any
import ctypes
import os
import platform


class AdminPrivilegeTool:
    def get_privilege_state(self) -> dict[str, Any]:
        is_windows = os.name == "nt"
        is_admin = self._is_windows_admin() if is_windows else False

        return {
            "platform_system": platform.system(),
            "os_name": os.name,
            "is_windows": is_windows,
            "is_admin": is_admin,
        }

    def _is_windows_admin(self) -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except (AttributeError, OSError):
            return False
