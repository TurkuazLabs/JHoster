# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-settings-menu-command.ps1
# 📌 Amac: Desktop settings menu compile test dosyasini command klasorunden calistirir
# 📌 Modul - PowerShell
# Version: 3.55.1
# Aciklama: NetBeans disi hizli dogrulama icin test-settings-menu-compile.ps1 dosyasina delege eder
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptPath = Join-Path (Split-Path -Parent $PSScriptRoot) "test-settings-menu-compile.ps1"
powershell -ExecutionPolicy Bypass -File $scriptPath
