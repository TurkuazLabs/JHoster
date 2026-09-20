# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-mode.ps1
# 📌 Amac: Apache/Nginx aktif web server mode testini PowerShell uzerinden calistirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent Python testini proje kokunden calistiran komut dosyasi
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$AgentRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $AgentRoot
python test-web-server-mode.py
