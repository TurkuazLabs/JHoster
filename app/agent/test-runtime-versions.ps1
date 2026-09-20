# 📄 Dosya Yolu: E:\JHoster\app\agent\test-runtime-versions.ps1
# 📌 Amac: JHoster runtime version endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Local package kurulumu sonrasi runtime version liste, detay ve activate API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"
$ComponentCode = "demo-local-package"
$Family = "demo-local-package"

Write-Host "JHoster runtime version test basladi"

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/$ComponentCode/install?dry_run=false" | ConvertTo-Json -Depth 20
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions" | ConvertTo-Json -Depth 20
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/$Family" | ConvertTo-Json -Depth 20
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/$ComponentCode/activate?dry_run=true" | ConvertTo-Json -Depth 20
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/$ComponentCode/activate?dry_run=false" | ConvertTo-Json -Depth 20
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/$Family" | ConvertTo-Json -Depth 20

Write-Host "JHoster runtime version test tamamlandi"
