# 📄 Dosya Yolu: E:\JHoster\app\agent\test-hosts-auto.ps1
# 📌 Amac: JHoster hosts auto endpointlerini yerel agent uzerinden test eder
# 📌 Modul - FileType
# Version: 3.66.0
# Aciklama: Hosts auto plan ve snapshot sync endpointleri icin hizli smoke test scripti
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster Hosts Auto Smoke Test"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-auto/plan?real_write=false" | ConvertTo-Json -Depth 10
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-auto/sync?real_write=false&dry_run=true" | ConvertTo-Json -Depth 10
