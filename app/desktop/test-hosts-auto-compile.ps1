# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-hosts-auto-compile.ps1
# 📌 Amac: Desktop hosts auto route ve New Test Site UI degisikliklerini javac ile kontrol eder
# 📌 Modul - FileType
# Version: 3.66.0
# Aciklama: Maven olmadan ilgili desktop dosyalarinin temel compile kontrolunu calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Src = Join-Path $Root "src\main\java"
$Out = Join-Path $Root "target\hosts-auto-compile"

if (Test-Path $Out) {
    Remove-Item $Out -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $Out | Out-Null

javac -d $Out `
    (Join-Path $Src "com\jhoster\desktop\config\DesktopApiConfig.java") `
    (Join-Path $Src "com\jhoster\desktop\views\LauncherView.java")

Write-Host "Hosts auto desktop compile smoke test completed."
