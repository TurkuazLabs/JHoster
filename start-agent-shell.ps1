# 📄 Dosya Yolu: E:\JHoster\start-agent-shell.ps1
# 📌 Amac: JHoster agent sanal ortamini aktif eden terminal acar
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Agent klasorunde .venv aktif terminal baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = "E:\JHoster"
$AgentPath = Join-Path $RootPath "app\agent"
$ActivatePath = Join-Path $AgentPath ".venv\Scripts\Activate.ps1"

if (!(Test-Path $ActivatePath)) {
    Write-Host "JHoster agent .venv bulunamadi."
    Write-Host "Once su komutu calistir:"
    Write-Host "powershell -ExecutionPolicy Bypass -File E:\JHoster\install-agent-deps.ps1"
    exit 1
}

powershell -NoExit -ExecutionPolicy Bypass -Command "Set-Location '$AgentPath'; & '$ActivatePath'; python --version"
