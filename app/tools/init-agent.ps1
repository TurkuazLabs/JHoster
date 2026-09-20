# 📄 Dosya Yolu: E:\JHoster\tools\init-agent.ps1
# 📌 Amac: JHoster Python agent icin ilk klasor ve dosya iskeletini olusturur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent, config, controller, service, repo, tool ve start dosyalarini hazirlar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = "E:\JHoster"
$AgentPath = Join-Path $RootPath "agent"
$RunAgentPath = Join-Path $RootPath "run-agent.ps1"

$AgentFolders = @(
    "config",
    "controllers",
    "services",
    "repositories",
    "tools",
    "views",
    "language",
    "storage"
)

New-Item -ItemType Directory -Force -Path $RootPath | Out-Null
New-Item -ItemType Directory -Force -Path $AgentPath | Out-Null

foreach ($FolderName in $AgentFolders) {
    New-Item -ItemType Directory -Force -Path (Join-Path $AgentPath $FolderName) | Out-Null
}

function Write-JHosterFile {
    param (
        [string]$Path,
        [string]$Content
    )

    Set-Content -Path $Path -Value $Content -Encoding UTF8
}

foreach ($FolderName in @("config", "controllers", "services", "repositories", "tools", "views", "language")) {
    $InitPath = Join-Path $AgentPath "$FolderName\__init__.py"
    $InitContent = @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\$FolderName\__init__.py
# 📌 Amac: JHoster agent $FolderName paketini Python import sistemine tanitir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Paket tanimlama dosyasi
# Bagimli Oldugu Katman: Tool
"@
    Write-JHosterFile -Path $InitPath -Content $InitContent
}

Write-JHosterFile -Path (Join-Path $AgentPath "requirements.txt") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\requirements.txt
# 📌 Amac: JHoster agent Python paket bagimliliklarini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: FastAPI, Uvicorn, YAML ve sistem bilgisi bagimliliklari
# Bagimli Oldugu Katman: Tool

fastapi>=0.115.0,<1.0.0
uvicorn[standard]>=0.30.0,<1.0.0
PyYAML>=6.0.0,<7.0.0
psutil>=6.0.0,<8.0.0
"@

Write-JHosterFile -Path (Join-Path $AgentPath "config\agent.yml") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\config\agent.yml
# 📌 Amac: JHoster agent merkezi ayarlarini tutar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent adi, surumu, sunucu portu ve storage yolu ayarlari
# Bagimli Oldugu Katman: Config

app:
  name: JHoster Agent
  version: 0.1.0

server:
  host: 127.0.0.1
  port: 8751
  reload: true

paths:
  root: E:\JHoster
  storage: E:\JHoster\app\data\jhoster

security:
  local_only: true
"@

Write-JHosterFile -Path (Join-Path $AgentPath "config\settings.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\config\settings.py
# 📌 Amac: JHoster agent YAML ayarlarini Python nesnesine cevirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Merkezi config okuyucu
# Bagimli Oldugu Katman: Config

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


CONFIG_FILE_PATH = Path(__file__).resolve().parent / "agent.yml"


@dataclass(frozen=True)
class AppSettings:
    app_name: str
    app_version: str
    server_host: str
    server_port: int
    dev_reload: bool
    root_path: Path
    storage_path: Path
    local_only: bool

    @classmethod
    def load(cls) -> "AppSettings":
        config_data = cls._read_yaml(CONFIG_FILE_PATH)

        app_config = config_data.get("app", {})
        server_config = config_data.get("server", {})
        path_config = config_data.get("paths", {})
        security_config = config_data.get("security", {})

        return cls(
            app_name=str(app_config.get("name")),
            app_version=str(app_config.get("version")),
            server_host=str(server_config.get("host")),
            server_port=int(server_config.get("port")),
            dev_reload=bool(server_config.get("reload")),
            root_path=Path(str(path_config.get("root"))),
            storage_path=Path(str(path_config.get("storage"))),
            local_only=bool(security_config.get("local_only")),
        )

    @staticmethod
    def _read_yaml(file_path: Path) -> dict[str, Any]:
        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as config_file:
            loaded_data = yaml.safe_load(config_file) or {}

        return loaded_data
"@

Write-JHosterFile -Path (Join-Path $AgentPath "tools\system_info_tool.py") -Content @"
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
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "python_version": sys.version.split()[0],
            "cpu_count": psutil.cpu_count(logical=True),
            "memory_total_mb": round(psutil.virtual_memory().total / 1024 / 1024),
        }
"@

Write-JHosterFile -Path (Join-Path $AgentPath "repositories\state_repository.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\state_repository.py
# 📌 Amac: JHoster agent durum bilgisini storage icinde saklar ve okur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent state dosya repository katmani
# Bagimli Oldugu Katman: Repo

import json
from pathlib import Path
from typing import Any


STATE_FILE_NAME = "agent_state.json"
DEFAULT_AGENT_STATE = {
    "state": "ready"
}


class StateRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.state_file_path = self.storage_path / STATE_FILE_NAME

    def get_state(self) -> dict[str, Any]:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        if not self.state_file_path.exists():
            self._write_state(DEFAULT_AGENT_STATE)

        with self.state_file_path.open("r", encoding="utf-8") as state_file:
            return json.load(state_file)

    def _write_state(self, state_data: dict[str, Any]) -> None:
        with self.state_file_path.open("w", encoding="utf-8") as state_file:
            json.dump(state_data, state_file, indent=2)
"@

Write-JHosterFile -Path (Join-Path $AgentPath "bin\health_service.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\bin\health_service.py
# 📌 Amac: JHoster agent saglik durumunu is kurallariyla hazirlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Health endpoint icin service katmani
# Bagimli Oldugu Katman: Service

from typing import Any

from repositories.state_repository import StateRepository
from tools.system_info_tool import SystemInfoTool


class HealthService:
    def __init__(
        self,
        state_repository: StateRepository,
        system_info_tool: SystemInfoTool,
    ) -> None:
        self.state_repository = state_repository
        self.system_info_tool = system_info_tool

    def get_health_status(self) -> dict[str, Any]:
        agent_state = self.state_repository.get_state()
        system_info = self.system_info_tool.get_system_info()

        return {
            "success": True,
            "status": agent_state.get("state"),
            "system": system_info,
        }
"@

Write-JHosterFile -Path (Join-Path $AgentPath "controllers\health_controller.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\controllers\health_controller.py
# 📌 Amac: JHoster agent saglik kontrol HTTP endpointini tanimlar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller sadece request alir ve service cagirir
# Bagimli Oldugu Katman: Controller

from fastapi import APIRouter

from config.settings import AppSettings
from repositories.state_repository import StateRepository
from services.health_service import HealthService
from tools.system_info_tool import SystemInfoTool


router = APIRouter(prefix="/api/v1/health", tags=["health"])

settings = AppSettings.load()
health_service = HealthService(
    state_repository=StateRepository(settings.storage_path),
    system_info_tool=SystemInfoTool(),
)


@router.get("")
def get_health_status() -> dict:
    return health_service.get_health_status()
"@

Write-JHosterFile -Path (Join-Path $AgentPath "main.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\main.py
# 📌 Amac: JHoster agent FastAPI uygulamasini baslatilabilir hale getirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Controller route kayitlarini merkezi uygulamaya baglar
# Bagimli Oldugu Katman: Controller

from fastapi import FastAPI

from config.settings import AppSettings
from controllers.health_controller import router as health_router


settings = AppSettings.load()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(health_router)
"@

Write-JHosterFile -Path (Join-Path $AgentPath "serve.py") -Content @"
# 📄 Dosya Yolu: E:\JHoster\app\agent\serve.py
# 📌 Amac: JHoster agent sunucusunu merkezi YAML ayarlariyla calistirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Uvicorn sunucu baslatici
# Bagimli Oldugu Katman: Tool

import uvicorn

from config.settings import AppSettings


settings = AppSettings.load()

uvicorn.run(
    "main:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=settings.dev_reload,
)
"@

Write-JHosterFile -Path $RunAgentPath -Content @"
# 📄 Dosya Yolu: E:\JHoster\run-agent.ps1
# 📌 Amac: JHoster Python agent sanal ortamini hazirlar ve agent sunucusunu baslatir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: .venv kontrolu, paket kurulumu ve agent server baslatma
# Bagimli Oldugu Katman: Tool

`$ErrorActionPreference = "Stop"

`$RootPath = "E:\JHoster"
`$AgentPath = Join-Path `$RootPath "agent"
`$VenvPath = Join-Path `$AgentPath ".venv"
`$ActivatePath = Join-Path `$VenvPath "Scripts\Activate.ps1"
`$RequirementsPath = Join-Path `$AgentPath "requirements.txt"

Set-Location `$AgentPath

if (!(Test-Path `$VenvPath)) {
    Write-Host "JHoster agent .venv bulunamadi. Python 3.13 ile olusturuluyor..."
    py -3.13 -m venv .venv
}

& `$ActivatePath

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r `$RequirementsPath

python serve.py
"@

Write-Host ""
Write-Host "JHoster agent iskeleti hazirlandi."
Write-Host "Calistirmak icin:"
Write-Host "powershell -ExecutionPolicy Bypass -File E:\JHoster\run-agent.ps1"
Write-Host ""
