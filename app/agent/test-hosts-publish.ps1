# 📄 Dosya Yolu: E:\JHoster\app\agent\test-hosts-publish.ps1
# 📌 Amac: JHoster hosts publish endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Generate, publish, validate ve reload akisindan sonra hosts dry-run ve snapshot publish API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster hosts publish test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$Domain = "demo-site.localhost"
$IpAddress = "127.0.0.1"

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-publish/$ProjectCode/publish?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-validate/$ProjectCode/validate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-reload/$ProjectCode/reload?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-publish/$ProjectCode/plan?ip=$IpAddress" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-publish/$ProjectCode/publish?ip=$IpAddress&dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-publish/$ProjectCode/publish?ip=$IpAddress&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-publish/$ProjectCode" | ConvertTo-Json -Depth 12

Write-Host "JHoster hosts publish test tamamlandi"
