# 📄 Dosya Yolu: E:\JHoster\app\desktop\commands\test-web-server-mode-command.ps1
# 📌 Amac: Desktop aktif web server mode Maven compile testini komut klasorunden baslatir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Ana desktop test dosyasini cagirir
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$CommandRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$DesktopRoot = Split-Path -Parent $CommandRoot
& (Join-Path $DesktopRoot "test-web-server-mode-compile.ps1")
