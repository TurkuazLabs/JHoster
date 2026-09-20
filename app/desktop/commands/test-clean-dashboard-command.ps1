# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-clean-dashboard-command.ps1
# 📌 Amac: JHoster Desktop clean dashboard compile testini komut klasorunden baslatir
# 📌 Modul - PowerShell
# Version: 3.53.1
# Aciklama: test-clean-dashboard-compile.ps1 dosyasini merkezi komut olarak calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $CommandDir
$TestFile = Join-Path $DesktopDir "test-clean-dashboard-compile.ps1"

& powershell -ExecutionPolicy Bypass -File $TestFile
