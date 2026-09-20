# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-laragon-ui-command.ps1
# 📌 Amac: JHoster Desktop Laragon style UI compile testini komut klasorunden baslatir
# 📌 Modul - PowerShell
# Version: 3.51.0
# Aciklama: Bir ust desktop klasorundeki test-laragon-ui-compile.ps1 dosyasini calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $CommandDir
$TestFile = Join-Path $DesktopDir "test-laragon-ui-compile.ps1"

powershell -ExecutionPolicy Bypass -File $TestFile
