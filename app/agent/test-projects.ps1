# 📄 Dosya Yolu: E:\JHoster\app\agent\test-www.ps1
# 📌 Amac: JHoster project endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Local package kurulumu, runtime aktivasyonu, project dry run, project create ve detail API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster project test basladi"

Invoke-RestMethod -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects" -Method Get | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=true" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects/demo-site" -Method Get | ConvertTo-Json -Depth 10

Write-Host "JHoster project test tamamlandi"
