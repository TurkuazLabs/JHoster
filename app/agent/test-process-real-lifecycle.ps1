# 📄 Dosya Yolu: E:\JHoster\app\agent\test-process-real-lifecycle.ps1
# 📌 Amac: Process real lifecycle guard endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.40.0
# Aciklama: Start, stop, restart, inspect ve guard cevaplarini guvenli dry-run/blocked modda dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Write-Host "========================================"
Write-Host "JHoster Process Real Lifecycle Test"
Write-Host "========================================"

$inspect = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/apache/inspect"
if ($null -eq $inspect) {
    throw "Inspect response is empty."
}

$dryStart = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/apache/start?dry_run=true&allow_real_execution=false"
if ($dryStart.success -ne $true) {
    throw "Dry-run start failed."
}

$blockedStart = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/apache/start?dry_run=false&allow_real_execution=true"
if ($blockedStart.success -eq $true) {
    throw "Real start should be blocked until real profile and executable are ready."
}

$blockedRestart = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/apache/restart?dry_run=false&allow_real_execution=true"
if ($blockedRestart.success -eq $true) {
    throw "Real restart should be blocked until real profile and executable are ready."
}

Write-Host "Process real lifecycle guard test passed."
