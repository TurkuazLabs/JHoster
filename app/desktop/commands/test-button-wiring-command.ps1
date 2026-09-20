# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-button-wiring-command.ps1
# 📌 Amac: JHoster Desktop button wiring compile testini komut klasorunden baslatir
# 📌 Modul - PowerShell
# Version: 3.53.1
# Aciklama: test-button-wiring-compile.ps1 dosyasini proje desktop kokunden calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$CommandDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopDir = Split-Path -Parent $CommandDir
& (Join-Path $DesktopDir "test-button-wiring-compile.ps1")
