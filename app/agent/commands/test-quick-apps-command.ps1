# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-quick-apps-command.ps1
# 📌 Amac: Quick App smoke test komutunu kolay calistirir
# 📌 Modul - PowerShell
# Version: 3.42.0
# Aciklama: agent/test-quick-apps.ps1 dosyasini proje kokunden tetikler
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentDir = Split-Path -Parent $ScriptDir
& (Join-Path $AgentDir "test-quick-apps.ps1")
