# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-visible-dev-mode-ux-compile.ps1
# 📌 Amac: JHoster Desktop v3.58.1 gorunur Dev Mode UX patch icin Maven compile ve hizli UI kaynak kontrolu yapar
# 📌 Modul - PowerShell
# Version: 3.58.1
# Aciklama: NetBeans disindan Maven compile calistirir ve Dev Mode UI siniflarinin kaynakta bulundugunu kontrol eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

Write-Host "JHoster Desktop v3.58.1 Visible Dev Mode UX Compile Test"
Write-Host "Project: $ProjectRoot"

$ViewFile = Join-Path $ProjectRoot "src\main\java\com\jhoster\desktop\views\LauncherView.java"
$CssFile = Join-Path $ProjectRoot "src\main\resources\styles\jhoster-modern.css"

$ViewSource = Get-Content $ViewFile -Raw
$CssSource = Get-Content $CssFile -Raw

$RequiredViewTokens = @(
    "DEV MODE ACTIVE",
    "buildDeveloperSidebarGroup",
    "buildDeveloperModeBanner",
    "buildDeveloperSettingsContent",
    "STYLE_DEV_SIDEBAR_GROUP"
)

foreach ($Token in $RequiredViewTokens) {
    if (-not $ViewSource.Contains($Token)) {
        throw "Missing LauncherView token: $Token"
    }
}

$RequiredCssTokens = @(
    "jhoster-dev-sidebar-group",
    "jhoster-dev-sidebar-button",
    "jhoster-dev-banner",
    "jhoster-dev-notice-title"
)

foreach ($Token in $RequiredCssTokens) {
    if (-not $CssSource.Contains($Token)) {
        throw "Missing CSS token: $Token"
    }
}

mvn --no-transfer-progress process-classes

Write-Host "v3.58.1 visible Dev Mode UX compile test completed."
