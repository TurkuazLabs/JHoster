# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-runtime-manager-command.ps1
# 📌 Amac: Desktop Runtime Manager compile test komutunu calistirir
# 📌 Modul - PowerShell
# Version: 3.41.0
# Aciklama: Runtime manager javac testini command klasorunden tek komutla tetikler
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $ScriptDir
& (Join-Path $DesktopDir "test-runtime-manager-compile.ps1")
