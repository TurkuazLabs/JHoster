# 📄 Dosya Yolu: E:\JHoster\app\agent\test-runtime-manager-active.ps1
# 📌 Amac: Runtime Manager active endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.41.0
# Aciklama: Runtime list, active ve activate endpointleri icin smoke test saglar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions" | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/active" | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/php/active" | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/php-8.3/activate?dry_run=true" | ConvertTo-Json -Depth 10

Write-Host "Runtime manager active smoke test completed."
