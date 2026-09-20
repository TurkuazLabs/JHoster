# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-web-server-workflow-locks-command.ps1
# 📌 Amac: Unified web server workflow lock guard test scriptini kisayol komutu olarak calistirir
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent kok dizininden test-web-server-workflow-locks.ps1 dosyasini baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $PSScriptRoot
& "$ScriptRoot\test-web-server-workflow-locks.ps1"
