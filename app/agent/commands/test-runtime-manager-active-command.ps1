# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-runtime-manager-active-command.ps1
# 📌 Amac: Runtime Manager active endpoint smoke test komutunu calistirir
# 📌 Modul - PowerShell
# Version: 3.41.0
# Aciklama: Runtime active testini commands klasorunden tetikler
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentDir = Split-Path -Parent $ScriptDir
& (Join-Path $AgentDir "test-runtime-manager-active.ps1")
