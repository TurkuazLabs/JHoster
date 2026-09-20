# 📄 Dosya Yolu: E:\JHoster\app\agent\test-components.ps1
# 📌 Amac: JHoster agent component endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Components API icin hizli test komutlari
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Write-Host "Testing components list..."
Invoke-RestMethod -Uri "$BaseUrl/api/v1/components" -Method GET | ConvertTo-Json -Depth 8

Write-Host "Testing PHP plan..."
Invoke-RestMethod -Uri "$BaseUrl/api/v1/components/php-8.3/plan" -Method GET | ConvertTo-Json -Depth 8
