# 📄 Dosya Yolu: E:\JHoster\app\agent\test-cache.ps1
# 📌 Amac: JHoster cache ve safe extract endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Cache listeleme, demo archive dry run ve gercek safe extract API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$baseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster cache test basladi"
Write-Host "GET /api/v1/cache"
Invoke-RestMethod -Uri "$baseUrl/api/v1/cache" -Method Get | ConvertTo-Json -Depth 8

Write-Host "POST /api/v1/components/demo-archive/execute?dry_run=true"
Invoke-RestMethod -Uri "$baseUrl/api/v1/components/demo-archive/execute?dry_run=true" -Method Post | ConvertTo-Json -Depth 8

Write-Host "POST /api/v1/components/demo-archive/execute?dry_run=false"
Invoke-RestMethod -Uri "$baseUrl/api/v1/components/demo-archive/execute?dry_run=false" -Method Post | ConvertTo-Json -Depth 8

Write-Host "JHoster cache test tamamlandi"
