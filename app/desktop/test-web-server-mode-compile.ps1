# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-web-server-mode-compile.ps1
# 📌 Amac: Desktop aktif web server mode degisikligi sonrasi Maven compile testini calistirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: JavaFX desktop kaynaklarini process-classes hedefiyle derler
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$DesktopRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $DesktopRoot
mvn --no-transfer-progress process-classes
