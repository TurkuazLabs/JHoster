# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-web-server-port-guard-command.ps1
# 📌 Amac: Web server port guard Python testini calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Apache ve Nginx 80/443 cakisma testleri icin pytest komutunu sarar
# Bagimli Oldugu Katman: Tool

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$AgentPath = "E:\JHoster\app\agent"
Set-Location -LiteralPath $AgentPath
python -m pytest .\test-web-server-port-guard.py
