# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-clean-dashboard-compile.ps1
# 📌 Amac: JHoster Desktop clean dashboard revizyonu icin Maven compile testi calistirir
# 📌 Modul - PowerShell
# Version: 3.53.1
# Aciklama: Desktop JavaFX kaynaklarini compile ederek sade dashboard render akislarini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

mvn -DskipTests compile
