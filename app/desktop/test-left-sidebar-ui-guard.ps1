# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-left-sidebar-ui-guard.ps1
# 📌 Amac: JHoster left sidebar UI statik guard testlerini calistirir
# 📌 Modul - PowerShell
# Version: 3.72.0
# Aciklama: Normal modda sol menu, New Site menusu ve tab/hero kaldirma kararini kontrol eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$viewPath = Join-Path $PSScriptRoot "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$content = Get-Content $viewPath -Raw

if ($content -notmatch "navNewSiteButton") {
    throw "navNewSiteButton bulunamadi"
}

if ($content -notmatch "buildSidebarModeContent") {
    throw "buildSidebarModeContent bulunamadi"
}

if ($content -notmatch "root.setLeft\(buildSidebar\(\)\)") {
    throw "Sol sidebar normal render akisi bulunamadi"
}

if ($content -match "TabPane") {
    throw "TabPane normal UI kararina aykiri"
}

if ($content -match "new Tab") {
    throw "new Tab normal UI kararina aykiri"
}

Write-Host "JHoster left sidebar UI guard passed."
