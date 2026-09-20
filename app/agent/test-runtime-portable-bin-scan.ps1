# 📄 Dosya Yolu: E:\JHoster\app\agent\test-runtime-portable-bin-scan.ps1
# 📌 Amac: Runtime portable bin scan endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.48.0
# Aciklama: Portable bin version tarama, family scan ve dry-run activate akisini dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"

Write-Host "Runtime portable bin scan test basladi"

$scan = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/portable-scan"
if ($scan.success -ne $true) {
    throw "Portable scan basarisiz"
}

$phpScan = Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/runtime-versions/php/portable-scan"
if ($phpScan.success -ne $true) {
    throw "PHP portable scan basarisiz"
}

$dryRun = Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/php/activate-portable?folder_name=php-8.3.30-Win32-vs16-x64&dry_run=true"
if ($dryRun.success -ne $true) {
    throw "Portable activate dry-run basarisiz"
}

Write-Host "Runtime portable bin scan test tamamlandi"
