# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-workflow-runs.ps1
# 📌 Amac: Unified web server workflow run tracking endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Workflow calismasi olusturur, run_id alir ve run listesi/detayi endpointlerini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster web server workflow run tracking test basladi"

Invoke-RestMethod -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-profiles/nginx/select?dry_run=false" -Method Post | ConvertTo-Json -Depth 10

$RunResponse = Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/run?domain=demo-site.localhost&port=80&dry_run=false&reload=true&allow_real_execution=false&rollback_on_failure=true" -Method Post
$RunResponse | ConvertTo-Json -Depth 20

$RunId = $RunResponse.run_id
if ([string]::IsNullOrWhiteSpace($RunId) -and $RunResponse.workflow) {
    $RunId = $RunResponse.workflow.run_id
}

if ([string]::IsNullOrWhiteSpace($RunId)) {
    throw "Workflow run_id bos dondu"
}

Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/runs" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/runs?project_code=demo-site" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/runs?status=completed" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/runs/$RunId" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/runs" -Method Get | ConvertTo-Json -Depth 20

Write-Host "JHoster web server workflow run tracking test tamamlandi"
