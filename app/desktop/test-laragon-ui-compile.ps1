# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-laragon-ui-compile.ps1
# 📌 Amac: JHoster Desktop Laragon style UI revizyonu icin Maven compile testi calistirir
# 📌 Modul - PowerShell
# Version: 3.51.0
# Aciklama: Desktop JavaFX kaynaklarini compile ederek compact servis aksiyonlari ve dock revizyonunu dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

mvn -DskipTests compile
