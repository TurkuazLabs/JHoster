# 📄 Dosya Yolu: E:\JHoster\app\agent\test-process.ps1
# 📌 Amac: JHoster process manager endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Demo app kurulumu sonrasi status, start, stop ve liste API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster process manager testi basladi..."
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/health" | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/components/demo-archive/execute?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/demo-archive/status" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/demo-archive/start?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/demo-archive/start?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/demo-archive/status" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/demo-archive/stop?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/demo-archive/status" | ConvertTo-Json -Depth 12
Write-Host "JHoster process manager testi tamamlandi."
