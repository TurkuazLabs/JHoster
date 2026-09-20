# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-fullscreen-stack-ui-guard.ps1
# 📌 Amac: Fullscreen tabsiz stack wizard UI statik guard testini calistirir
# 📌 Modul - PowerShell
# Version: 3.72.0
# Aciklama: LauncherView icinde normal mod ana TabPane kullaniminin kaldirildigini ve stack secim alanlarinin varligini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$View = Join-Path $Root "src/main/java/com/jhoster/desktop/views/LauncherView.java"
$Text = Get-Content $View -Raw
if ($Text -notmatch "buildQuickAppStackSelectionPanel") { throw "Stack selection panel missing" }
if ($Text -notmatch "STYLE_FULLSCREEN_STACK") { throw "Fullscreen stack style missing" }
if ($Text -match "new Tab\("Services", buildSimpleModeCenterGrid\(\)\)") { throw "Old main tab menu still exists" }
if ($Text -notmatch "getQuickAppWebServer") { throw "Quick App web server getter missing" }
Write-Host "fullscreen stack UI guard ok"
