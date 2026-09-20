# 📄 Dosya Yolu: E:\JHoster\app\agent\serve.py
# 📌 Amac: JHoster agent sunucusunu merkezi YAML ayarlariyla calistirir
# 📌 Modul - FileType
# Version: 1.0.1
# Aciklama: Windows uyumlu Uvicorn sunucu baslatici
# Bagimli Oldugu Katman: Tool

from multiprocessing import freeze_support

import uvicorn

from config.constants import MAIN_APP_IMPORT_PATH
from config.settings import AppSettings


def run_server() -> None:
    settings = AppSettings.load()

    uvicorn.run(
        MAIN_APP_IMPORT_PATH,
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.dev_reload,
    )


if __name__ == "__main__":
    freeze_support()
    run_server()
