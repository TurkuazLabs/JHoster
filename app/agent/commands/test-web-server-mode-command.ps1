# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-web-server-mode-command.ps1
# 📌 Amac: Web server mode test komutunu agent klasorune delege eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache/Nginx secim testi icin kisayol komut dosyasi
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$CommandRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentRoot = Split-Path -Parent $CommandRoot
& (Join-Path $AgentRoot "test-web-server-mode.ps1")
