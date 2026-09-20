# 📄 Dosya Yolu: E:\JHoster\app\agent\test-virtual-hosts.ps1
# 📌 Amac: JHoster virtual host endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Local package kurulumu, runtime aktivasyonu, project create ve virtual host generate API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster virtual host test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$Domain = "demo-site.localhost"

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/virtual-hosts" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/plan?domain=$Domain&port=80" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode" | ConvertTo-Json -Depth 12

Write-Host "JHoster virtual host test tamamlandi"
