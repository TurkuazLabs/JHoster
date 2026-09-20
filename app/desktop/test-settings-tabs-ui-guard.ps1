# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-settings-tabs-ui-guard.ps1
# 📌 Amac: Settings icinde tab menu kullaniminin statik UI kontrolunu yapar
# 📌 Modul - PowerShell
# Version: 3.73.1
# Aciklama: Ana LauncherView dosyasinda sol sidebar korunurken Settings TabPane kontrol edilir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$viewPath = Join-Path $PSScriptRoot "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$content = Get-Content $viewPath -Raw

if ($content -notmatch "new TabPane\(\)") {
    throw "Settings TabPane bulunamadi."
}

if ($content -notmatch "buildSettingsTab\("General"") {
    throw "General settings tab bulunamadi."
}

if ($content -notmatch "buildSettingsTab\("Services"") {
    throw "Services settings tab bulunamadi."
}

if ($content -notmatch "buildSettingsTab\(LICENSE_SETTINGS_TAB") {
    throw "License settings tab bulunamadi."
}

if ($content -notmatch "buildSettingsTab\(LABEL_HOSTS_AUTO_SETTINGS_TAB") {
    throw "Hosts settings tab bulunamadi."
}

if ($content -notmatch "buildSettingsTab\("Appearance"") {
    throw "Appearance settings tab bulunamadi."
}

if ($content -notmatch "buildSettingsTab\("Advanced"") {
    throw "Advanced settings tab bulunamadi."
}

Write-Host "Settings tabs UI guard passed."
