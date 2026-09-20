# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-ui-completion-compile.ps1
# 📌 Amac: JHoster Desktop v3.56.0 UI completion ve Maven compile kontrolunu calistirir
# 📌 Modul - PowerShell
# Version: 3.56.0
# Aciklama: Dinamik sayfa gecisleri, settings menu ve desktop Maven compile kontrolu yapar
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$desktopRoot = "E:\JHoster\app\desktop"
Set-Location $desktopRoot

Write-Host "JHoster Desktop v3.56.0 UI completion compile test"
Write-Host "Path: $desktopRoot"

mvn --no-transfer-progress clean process-classes
