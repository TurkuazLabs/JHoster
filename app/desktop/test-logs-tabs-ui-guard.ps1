# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-logs-tabs-ui-guard.ps1
# 📌 Amac: Logs sayfasindaki uygulama bazli tab menu korumasini test eder
# 📌 Modul - PowerShell
# Version: 3.75.0
# Aciklama: LauncherView icinde Logs tablari, klasor map ve servis log route kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$viewPath = Join-Path $PSScriptRoot "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$cssPath = Join-Path $PSScriptRoot "src/main/resources/styles/jhoster-modern.css"

if (-not (Test-Path $viewPath)) {
    throw "LauncherView.java bulunamadi: $viewPath"
}

if (-not (Test-Path $cssPath)) {
    throw "jhoster-modern.css bulunamadi: $cssPath"
}

$view = Get-Content $viewPath -Raw
$css = Get-Content $cssPath -Raw

$requiredTokens = @(
    "applicationLogsTabPane",
    "buildApplicationLogTabPane(true)",
    "buildLogTab(\"Desktop\", logArea)",
    "buildLogTab(\"Agent\", agentLogArea)",
    "buildLogTab(\"Apache\", apacheLogArea)",
    "buildLogTab(\"Nginx\", nginxLogArea)",
    "buildLogTab(\"MySQL\", mysqlLogArea)",
    "buildLogTab(\"PHP\", phpLogArea)",
    "buildLogTab(\"Mailpit\", mailpitLogArea)",
    "buildLogTab(\"System\", systemLogArea)",
    "case \"Apache\" -> \"logs/apache\"",
    "case \"Nginx\" -> \"logs/nginx\""
)

foreach ($token in $requiredTokens) {
    if (-not $view.Contains($token)) {
        throw "Eksik LauncherView token: $token"
    }
}

$cssTokens = @(
    ".jhoster-application-log-tabs",
    ".jhoster-application-log-area",
    "v3.75.0 application log tabs"
)

foreach ($token in $cssTokens) {
    if (-not $css.Contains($token)) {
        throw "Eksik CSS token: $token"
    }
}

Write-Host "Logs tabs UI guard passed."
