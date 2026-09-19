# 📄 Dosya Yolu: E:\JHoster\stop-agent.ps1
# 📌 Amac: JHoster agent 8751 portunu kullanan processleri kapatir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent portunu dinleyen eski Python/Uvicorn processlerini temizler
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "SilentlyContinue"

$AgentPort = 8751

$ProcessIds = Get-NetTCPConnection -LocalPort $AgentPort |
    Select-Object -ExpandProperty OwningProcess -Unique

if (!$ProcessIds) {
    Write-Host "JHoster agent zaten kapali."
    exit 0
}

foreach ($ProcessId in $ProcessIds) {
    Stop-Process -Id $ProcessId -Force
    Write-Host "Kapatildi: PID $ProcessId"
}

Write-Host "JHoster agent portu temizlendi: $AgentPort"
