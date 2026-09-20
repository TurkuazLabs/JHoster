# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-port-guard.ps1
# 📌 Amac: Web server port guard test komut dosyasini cagirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Apache ve Nginx public port cakisma testlerini tek komutla calistirir
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

& "E:\JHoster\app\agent\commands\test-web-server-port-guard-command.ps1"
