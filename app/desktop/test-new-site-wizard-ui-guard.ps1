# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-new-site-wizard-ui-guard.ps1
# 📌 Amac: New Site wizard UI metin ve stil baglantilarini statik olarak kontrol eder
# 📌 Modul - PowerShell
# Version: 3.69.0
# Aciklama: JavaFX runtime olmadan LauncherView ve CSS icinde New Site wizard baglantilarini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "../..")
$ViewPath = Join-Path $RootPath "app/desktop/src/main/java/com/jhoster/desktop/views/LauncherView.java"
$CssPath = Join-Path $RootPath "app/desktop/src/main/resources/styles/jhoster-modern.css"

$view = Get-Content -Raw $ViewPath
$css = Get-Content -Raw $CssPath

$requiredViewTokens = @(
    'TAB_NEW_TEST_SITE',
    'buildSiteWizardPanel',
    'buildSiteWizardPreviewPanel',
    'buildSiteWizardStep',
    'bindSiteWizardPreviewFields',
    'siteWizardUrlPreviewValue',
    'jhoster-quick-app-card'
)

foreach ($token in $requiredViewTokens) {
    if (-not $view.Contains($token)) {
        throw "Missing LauncherView token: $token"
    }
}

$requiredCssTokens = @(
    '.jhoster-site-wizard-layout',
    '.jhoster-site-wizard-main',
    '.jhoster-site-wizard-preview',
    '.jhoster-site-wizard-step',
    '.jhoster-site-wizard-preview-card'
)

foreach ($token in $requiredCssTokens) {
    if (-not $css.Contains($token)) {
        throw "Missing CSS token: $token"
    }
}

Write-Host "New Site wizard UI guard OK"
