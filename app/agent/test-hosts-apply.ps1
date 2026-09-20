# 📄 Dosya Yolu: E:\JHoster\app\agent\test-hosts-apply.ps1
# 📌 Amac: JHoster hosts apply ve rollback endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Virtual host generate sonrasi snapshot hosts apply, backup ve rollback akisini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster hosts apply test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$Domain = "demo-site.localhost"
$IpAddress = "127.0.0.1"

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/plan?ip=$IpAddress&real_write=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/apply?ip=$IpAddress&real_write=false&dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/apply?ip=$IpAddress&real_write=false&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/apply?ip=$IpAddress&real_write=false&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/rollback-plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/rollback?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode/rollback?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/hosts-apply/$ProjectCode" | ConvertTo-Json -Depth 12

Write-Host "JHoster hosts apply test tamamlandi"
