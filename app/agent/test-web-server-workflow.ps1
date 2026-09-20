# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-workflow.ps1
# 📌 Amac: Unified web server workflow endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Active web server profile secimine gore plan, run ve rollback guard akisini tek endpointten dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster web server workflow test basladi"

Invoke-RestMethod -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-profiles/nginx/select?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/plan?domain=demo-site.localhost&port=80&reload=true&rollback_on_failure=true" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/run?domain=demo-site.localhost&port=80&dry_run=false&reload=true&allow_real_execution=false&rollback_on_failure=true" -Method Post | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/rollback?dry_run=true" -Method Post | ConvertTo-Json -Depth 20

Write-Host "JHoster web server workflow test tamamlandi"
