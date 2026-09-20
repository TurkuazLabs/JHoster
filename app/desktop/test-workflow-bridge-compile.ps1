# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-workflow-bridge-compile.ps1
# 📌 Amac: JHoster Desktop workflow bridge Maven compile kontrolunu calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Desktop JavaFX projesini Maven ile derlemeyi dener ve NetBeans oncesi hizli kontrol saglar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "========================================"
Write-Host "JHoster Desktop Workflow Bridge Compile"
Write-Host "========================================"

$mvn = Get-Command mvn -ErrorAction SilentlyContinue
if ($null -eq $mvn) {
    Write-Host "Maven bulunamadi. NetBeans bundled Maven veya sistem Maven ile compile calistirin."
    exit 1
}

mvn -q -DskipTests compile

Write-Host "Desktop compile tamamlandi."
