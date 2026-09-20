# 📄 Dosya Yolu: E:\JHoster\app\agent\test-service-adapters.ps1
# 📌 Amac: JHoster service adapter endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Adapter liste, PHP adapter detay ve simulated adapter detay API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster service adapter testi basladi..."
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/service-adapters" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/service-adapters/php" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/service-adapters/simulated" | ConvertTo-Json -Depth 12
Write-Host "JHoster service adapter testi tamamlandi."
