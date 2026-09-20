# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-quick-app-command.ps1
# 📌 Amac: Desktop Quick App compile testini kolay calistirir
# 📌 Modul - PowerShell
# Version: 3.42.0
# Aciklama: desktop/test-quick-app-compile.ps1 dosyasini tetikler
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $ScriptDir
& (Join-Path $DesktopDir "test-quick-app-compile.ps1")
