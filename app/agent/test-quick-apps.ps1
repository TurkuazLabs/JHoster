# 📄 Dosya Yolu: E:\JHoster\app\agent\test-quick-apps.ps1
# 📌 Amac: Quick App endpointleri icin smoke test yapar
# 📌 Modul - PowerShell
# Version: 3.42.0
# Aciklama: Template listeleme, planlama ve dry-run create akislarini agent API uzerinden test eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Write-Host "========================================"
Write-Host "JHoster Quick App Test"
Write-Host "========================================"

$Templates = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/quick-apps/templates"
if (-not $Templates.success) {
    throw "Quick App templates basarisiz"
}

$Plan = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/quick-apps/demo-quick-app/plan?template_code=opencart-3&project_name=Demo%20OpenCart&domain=demo-quick-app.test&port=80"
if (-not $Plan.success) {
    throw "Quick App plan basarisiz"
}

$DryRun = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/quick-apps/demo-quick-app/create?template_code=php-empty&project_name=Demo%20Quick%20App&domain=demo-quick-app.test&port=80&dry_run=true"
if (-not $DryRun.success) {
    throw "Quick App dry-run create basarisiz"
}

Write-Host "Quick App templates:" $Templates.count
Write-Host "Quick App plan status:" $Plan.status
Write-Host "Quick App dry-run status:" $DryRun.status
Write-Host "Quick App smoke test tamamlandi."
