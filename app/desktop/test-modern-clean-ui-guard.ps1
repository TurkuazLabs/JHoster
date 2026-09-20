# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-modern-clean-ui-guard.ps1
# 📌 Amac: Modern clean UI icin calismayan sabit topbar elemanlarini ve sol menu gruplarini denetler
# 📌 Modul - PowerShell
# Version: 3.76.0
# Aciklama: Search/Alerts gibi calismayan UI elemanlari kaldirildi mi, status topbar ve sol menu gruplari var mi kontrol eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$viewPath = Join-Path $PSScriptRoot "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$cssPath = Join-Path $PSScriptRoot "src/main/resources/styles/jhoster-modern.css"
$view = Get-Content $viewPath -Raw
$css = Get-Content $cssPath -Raw

$requiredTokens = @(
    "Workspace Control",
    "jhoster-topbar-status-strip",
    "buildTopbarStatusPill",
    "buildSidebarGroup("CREATE"",
    "buildSidebarGroup("OPERATE"",
    "buildSidebarGroup("RESOURCES"",
    "buildSidebarGroup("OBSERVE""
)

foreach ($token in $requiredTokens) {
    if (-not $view.Contains($token)) {
        throw "Missing modern UI token: $token"
    }
}

$forbiddenTokens = @(
    "Alerts 3",
    "Search projects, tools, docs",
    "Ctrl + K"
)

foreach ($token in $forbiddenTokens) {
    if ($view.Contains($token)) {
        throw "Forbidden non-working UI token still exists: $token"
    }
}

if (-not $css.Contains("v3.76.0 modern cleanup")) {
    throw "Missing v3.76.0 CSS cleanup block"
}

Write-Host "Modern clean UI guard passed."
