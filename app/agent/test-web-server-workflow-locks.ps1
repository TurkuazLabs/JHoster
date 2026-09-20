# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-workflow-locks.ps1
# 📌 Amac: Unified web server workflow lock guard endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Workflow lock listesi, normal run sonrasi lock release, fake lock collision ve force unlock akislarini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"
$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$LockRegistryPath = Join-Path $ScriptRoot "storage\web_server_workflow_lock_registry.json"

Write-Host "JHoster web server workflow lock guard test basladi"

Invoke-RestMethod -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/projects?project_code=demo-site&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" -Method Post | ConvertTo-Json -Depth 10
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-profiles/nginx/select?dry_run=false" -Method Post | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/locks" -Method Get | ConvertTo-Json -Depth 20

$RunResponse = Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/run?domain=demo-site.localhost&port=80&dry_run=false&reload=true&allow_real_execution=false&rollback_on_failure=true" -Method Post
$RunResponse | ConvertTo-Json -Depth 20

$LockListAfterRun = Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/locks" -Method Get
$LockListAfterRun | ConvertTo-Json -Depth 20

if ($LockListAfterRun.count -ne 0) {
    throw "Workflow lock release basarisiz"
}

$FakeLock = @{
    active_locks = @(
        @{
            project_code = "demo-site"
            run_id = "manual-lock-001"
            web_server = "nginx"
            status = "active"
            locked_at = "2026-05-12T00:00:00+00:00"
        }
    )
}
$FakeLock | ConvertTo-Json -Depth 10 | Set-Content -Path $LockRegistryPath -Encoding UTF8

$LockedRunResponse = Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/run?domain=demo-site.localhost&port=80&dry_run=false&reload=false&allow_real_execution=false&rollback_on_failure=true" -Method Post
$LockedRunResponse | ConvertTo-Json -Depth 20

if ($LockedRunResponse.success -ne $false) {
    throw "Workflow lock collision beklenen sekilde engellenmedi"
}

Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/lock" -Method Get | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/unlock?run_id=wrong&force=false" -Method Post | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/unlock?force=true" -Method Post | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/locks" -Method Get | ConvertTo-Json -Depth 20

Write-Host "JHoster web server workflow lock guard test tamamlandi"
