# 📄 Dosya Yolu: E:\JHoster\app\agent\views\api_response_view.py
# 📌 Amac: JHoster agent API response ciktilarini standart hale getirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller response view katmani
# Bagimli Oldugu Katman: View

from typing import Any


class ApiResponseView:
    def render(self, response_data: dict[str, Any]) -> dict[str, Any]:
        return response_data
