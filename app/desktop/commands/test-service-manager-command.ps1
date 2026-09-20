# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-service-manager-command.ps1
# 📌 Amac: Desktop service manager compile testini komut klasorunden calistirir
# 📌 Modul - PowerShell
# Version: 1.1.0
# Aciklama: Gelistirici icin tek komutla service manager desktop testini baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $CommandDir
$TestFile = Join-Path $DesktopDir "test-service-manager-compile.ps1"

powershell -ExecutionPolicy Bypass -File $TestFile
