# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-modern-command-ui-guard.ps1
# 📌 Amac: JHoster modern command UI statik kontrol testini calistirir
# 📌 Modul - PowerShell
# Version: 3.72.0
# Aciklama: LauncherView ve CSS icinde modern command center tokenlarini ve tab menu kaldirma kararini dogrular
# Bagimli Oldugu Katman: View

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$viewFile = Join-Path $root "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$cssFile = Join-Path $root "src/main/resources/styles/jhoster-modern.css"

$view = Get-Content $viewFile -Raw
$css = Get-Content $cssFile -Raw

$requiredViewTokens = @(
    "buildModernCommandHeroPanel",
    "STYLE_MODERN_HERO_SHELL",
    "STYLE_MODERN_STATUS_RAIL",
    "buildSiteWizardPanel",
    "buildQuickAppStackSelectionPanel"
)

$requiredCssTokens = @(
    "jhoster-modern-hero-shell",
    "jhoster-modern-hero-card",
    "jhoster-modern-status-rail",
    "jhoster-modern-preset-card",
    "jhoster-stack-webserver-row"
)

foreach ($token in $requiredViewTokens) {
    if ($view -notlike "*$token*") {
        throw "Missing LauncherView token: $token"
    }
}

foreach ($token in $requiredCssTokens) {
    if ($css -notlike "*$token*") {
        throw "Missing CSS token: $token"
    }
}

if ($view -like "*new Tab*" -or $view -like "*TabPane*") {
    throw "Tab menu token detected in LauncherView normal UI."
}

Write-Host "JHoster modern command UI guard passed."
