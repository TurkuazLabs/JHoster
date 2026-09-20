# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-process-real-profile-command.ps1
# 📌 Amac: Process real profile test scriptini tek komutla calistirir
# 📌 Modul - PowerShell
# Version: 3.40.0
# Aciklama: Agent process real profile endpointleri icin test wrapper komutudur
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentRoot = Split-Path -Parent $ScriptRoot
& "$AgentRoot\test-process-real-profile.ps1"
