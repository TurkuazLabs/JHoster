# 📄 Dosya Yolu: E:\JHoster\app\agent\test-executor.ps1
# 📌 Amac: JHoster agent executor endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Dry run, guvenli execute ve history API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Write-Host "Testing PHP executor dry run..."
Invoke-RestMethod -Uri "$BaseUrl/api/v1/components/php-8.3/execute?dry_run=true" -Method POST | ConvertTo-Json -Depth 10

Write-Host "Testing demo safe executor real run..."
Invoke-RestMethod -Uri "$BaseUrl/api/v1/components/demo-safe/execute?dry_run=false" -Method POST | ConvertTo-Json -Depth 10

Write-Host "Testing install history..."
Invoke-RestMethod -Uri "$BaseUrl/api/v1/install/history" -Method GET | ConvertTo-Json -Depth 10
