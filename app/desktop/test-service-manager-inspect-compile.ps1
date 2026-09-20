# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-service-manager-inspect-compile.ps1
# 📌 Amac: Desktop Service Manager inspect baglanti siniflarini derleme testi yapar
# 📌 Modul - PowerShell
# Version: 3.40.0
# Aciklama: JavaFX olmayan service manager inspect siniflarini javac ile kontrol eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$DesktopDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutDir = Join-Path $DesktopDir "build-check-service-inspect"

if (Test-Path $OutDir) {
    Remove-Item -Recurse -Force $OutDir
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$Sources = @(
    "src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java",
    "src\main\java\com\jhoster\desktop\models\DesktopHttpResult.java",
    "src\main\java\com\jhoster\desktop\models\ServiceManagerSummary.java",
    "src\main\java\com\jhoster\desktop\tools\HttpRequestTool.java",
    "src\main\java\com\jhoster\desktop\tools\JsonTextExtractorTool.java",
    "src\main\java\com\jhoster\desktop\bin\ServiceResultFormatterService.java",
    "src\main\java\com\jhoster\desktop\bin\ServiceManagerDesktopService.java"
)

Push-Location $DesktopDir
javac --release 21 -d $OutDir $Sources
Pop-Location

Write-Host "Desktop service manager inspect compile test completed."
