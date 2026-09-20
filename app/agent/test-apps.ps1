# 📄 Dosya Yolu: E:\JHoster\app\agent\test-apps.ps1
# 📌 Amac: JHoster app registry endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Demo archive execute sonrasi apps liste ve detay API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster app registry testi basladi..."
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/health" | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/components/demo-archive/execute?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apps" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apps/demo-archive" | ConvertTo-Json -Depth 12
Write-Host "JHoster app registry testi tamamlandi."
