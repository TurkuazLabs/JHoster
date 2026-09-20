# 📄 Dosya Yolu: E:\JHoster\app\agent\test-process-real-preflight.ps1
# 📌 Amac: JHoster process real execution preflight ve guard endpointlerini test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache, Nginx, MySQL ve PHP icin preflight, restart dry-run ve real execution guard kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"
$Services = @("apache", "nginx", "mysql", "php")

Write-Host "JHoster process real preflight testi basladi..."
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/health" | ConvertTo-Json -Depth 8

foreach ($ServiceCode in $Services) {
    Write-Host "Preflight: $ServiceCode"
    Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/preflight" | ConvertTo-Json -Depth 14

    Write-Host "Restart dry-run: $ServiceCode"
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/$ServiceCode/restart?dry_run=true" | ConvertTo-Json -Depth 14

    Write-Host "Real guard: $ServiceCode"
    Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/$ServiceCode/start?dry_run=false&allow_real_execution=true" | ConvertTo-Json -Depth 14
}

Write-Host "JHoster process real preflight testi tamamlandi."
