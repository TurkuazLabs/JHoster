# 📄 Dosya Yolu: E:\JHoster\install-agent-deps.ps1
# 📌 Amac: JHoster Python agent paket bagimliliklarini kurar ve gunceller
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: .venv kontrolu yapar, pip ve requirements paketlerini kurar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = "E:\JHoster"
$AgentPath = Join-Path $RootPath "app\agent"
$VenvPath = Join-Path $AgentPath ".venv"
$ActivatePath = Join-Path $VenvPath "Scripts\Activate.ps1"
$RequirementsPath = Join-Path $AgentPath "requirements.txt"

Set-Location $AgentPath

if (!(Test-Path $VenvPath)) {
    Write-Host "JHoster agent .venv bulunamadi. Python 3.13 ile olusturuluyor..."
    py -3.13 -m venv .venv
}

& $ActivatePath

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r $RequirementsPath

Write-Host ""
Write-Host "JHoster agent paket kurulumu tamamlandi."
