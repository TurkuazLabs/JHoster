# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-compact-dashboard-command.ps1
# 📌 Amac: Compact dashboard test scriptini komut klasorunden calistirir
# 📌 Modul - PowerShell
# Version: 3.45.0
# Aciklama: Desktop compact dashboard javac smoke test wrapper dosyasi
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $ScriptDir
& (Join-Path $DesktopDir "test-compact-dashboard-compile.ps1")
