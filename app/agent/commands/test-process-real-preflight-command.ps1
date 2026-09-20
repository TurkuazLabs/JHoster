# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-process-real-preflight-command.ps1
# 📌 Amac: Process real preflight testini komut klasorunden calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Gelistirici icin tek komutla real execution preflight ve guard testini baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentDir = Split-Path -Parent $CommandDir
$TestFile = Join-Path $AgentDir "test-process-real-preflight.ps1"

powershell -ExecutionPolicy Bypass -File $TestFile
