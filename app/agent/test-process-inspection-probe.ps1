# 📄 Dosya Yolu: E:\JHoster\app\agent\test-process-inspection-probe.ps1
# 📌 Amac: Process inspection probe endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.38.0
# Aciklama: Service Manager icin inspect ve prefer_real status akislarini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"
$ServiceCode = "apache"

Write-Host "========================================"
Write-Host "JHoster Process Inspection Probe Test"
Write-Host "========================================"

Write-Host "[1] Inspect endpoint"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/inspect" | ConvertTo-Json -Depth 12

Write-Host "[2] Real-preferred status endpoint"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/status?prefer_real=true" | ConvertTo-Json -Depth 12

Write-Host "[3] Normal status endpoint"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/status" | ConvertTo-Json -Depth 12

Write-Host "========================================"
Write-Host "Process inspection probe test completed"
Write-Host "========================================"
