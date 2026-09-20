# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-process-real-lifecycle-command.ps1
# 📌 Amac: Process real lifecycle guard testini tek komutla calistirir
# 📌 Modul - PowerShell
# Version: 3.40.0
# Aciklama: Gelistirici icin process real lifecycle test scriptini command klasorunden baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentDir = Split-Path -Parent $CommandDir
$TestFile = Join-Path $AgentDir "test-process-real-lifecycle.ps1"

powershell -ExecutionPolicy Bypass -File $TestFile
