# 📄 Dosya Yolu: E:\JHoster\app\agent\test-nginx-reload.ps1
# 📌 Amac: JHoster Nginx reload endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Generate, publish ve validate akisindan sonra reload dry-run ve simulated reload API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster Nginx reload test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$Domain = "demo-site.localhost"

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-publish/$ProjectCode/publish?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-validate/$ProjectCode/validate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-reload/$ProjectCode/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-reload/$ProjectCode/reload?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-reload/$ProjectCode/reload?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-reload/$ProjectCode" | ConvertTo-Json -Depth 12

Write-Host "JHoster Nginx reload test tamamlandi"
