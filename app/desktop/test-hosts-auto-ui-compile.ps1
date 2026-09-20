# 📄 Dosya Yolu: E:/JHoster/app/desktop/test-hosts-auto-ui-compile.ps1
# 📌 Amac: Hosts auto desktop service ve model dosyalarini parcali compile eder
# 📌 Modul - PowerShell
# Version: 3.69.0
# Aciklama: JavaFX olmadan hosts auto desktop servis/model siniflarini javac ile test eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "../..")
$SourcePath = Join-Path $RootPath "app/desktop/src/main/java"
$OutPath = Join-Path $RootPath "tmp/compile/hosts-auto-ui"

New-Item -ItemType Directory -Force -Path $OutPath | Out-Null

javac -d $OutPath `
    (Join-Path $SourcePath "com/jhoster/desktop/models/DesktopHttpResult.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/models/HostsAutoSummary.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/tools/JsonTextExtractorTool.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/tools/HttpRequestTool.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/config/DesktopApiConfig.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/services/HostsAutoResultFormatterService.java") `
    (Join-Path $SourcePath "com/jhoster/desktop/services/HostsAutoDesktopService.java")

Write-Host "Hosts auto UI compile OK"
