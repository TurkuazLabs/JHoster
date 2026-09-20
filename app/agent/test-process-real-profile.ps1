# 📄 Dosya Yolu: E:\JHoster\app\agent\test-process-real-profile.ps1
# 📌 Amac: Process real profile endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.40.0
# Aciklama: Service Manager real process profil goruntuleme, planlama ve dry-run apply akisini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"
$ServiceCode = "apache"
$InstallPath = [System.Web.HttpUtility]::UrlEncode("apps/apache")

Write-Host "========================================"
Write-Host "JHoster Process Real Profile Test"
Write-Host "========================================"

Write-Host "[1] Current real profile"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/real-profile" | ConvertTo-Json -Depth 14

Write-Host "[2] Plan real profile update"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/process/$ServiceCode/real-profile/plan?install_path=$InstallPath&enabled=true" | ConvertTo-Json -Depth 14

Write-Host "[3] Apply real profile dry-run"
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/process/$ServiceCode/real-profile/apply?install_path=$InstallPath&enabled=true&dry_run=true" | ConvertTo-Json -Depth 14

Write-Host "========================================"
Write-Host "Process real profile test completed"
Write-Host "========================================"
