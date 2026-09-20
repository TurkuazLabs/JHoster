# 📄 Dosya Yolu: E:\JHoster\app\agent\test-local-packages.ps1
# 📌 Amac: JHoster local package endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Local package liste, plan, dry run, kurulum ve app registry API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"
$ComponentCode = "demo-local-package"

Write-Host "JHoster local package test basladi"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/local-packages" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/local-cache/packages/$ComponentCode/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/$ComponentCode/install?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/$ComponentCode/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apps/$ComponentCode" | ConvertTo-Json -Depth 12
Write-Host "JHoster local package test tamamlandi"
