# 📄 Dosya Yolu: E:\JHoster\app\agent\commands\test-process-inspection-probe-command.ps1
# 📌 Amac: Process inspection probe test komutunu tek noktadan calistirir
# 📌 Modul - PowerShell
# Version: 3.38.0
# Aciklama: Agent process inspect test betigini ana klasorden cagirmak icin kullanilir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$AgentDir = Resolve-Path (Join-Path $ScriptDir "..")
& (Join-Path $AgentDir "test-process-inspection-probe.ps1")
