# 📄 Dosya Yolu: E:\JHoster\run-agent.ps1
# 📌 Amac: JHoster Python agent sanal ortamini acip agent sunucusunu baslatir
# 📌 Modul - FileType
# Version: 1.2.0
# Aciklama: Paket kurulumu yapmadan mevcut .venv ile FastAPI agent calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = "E:\JHoster"
$AgentPath = Join-Path $RootPath "app\agent"
$VenvPath = Join-Path $AgentPath ".venv"
$ActivatePath = Join-Path $VenvPath "Scripts\Activate.ps1"

if (!(Test-Path $ActivatePath)) {
    Write-Host "JHoster agent .venv bulunamadi."
    Write-Host "Once su komutu calistir:"
    Write-Host "powershell -ExecutionPolicy Bypass -File E:\JHoster\install-agent-deps.ps1"
    exit 1
}

Set-Location $AgentPath
& $ActivatePath
python serve.py
