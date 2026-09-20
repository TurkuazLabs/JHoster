# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-button-wiring-compile.ps1
# 📌 Amac: JHoster Desktop button wiring revizyonu icin Maven compile testi calistirir
# 📌 Modul - PowerShell
# Version: 3.53.1
# Aciklama: JavaFX controller, view, service ve tool baglantilarini lokal Maven compile ile dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

mvn -DskipTests compile
