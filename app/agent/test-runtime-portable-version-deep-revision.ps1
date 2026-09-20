# 📄 Dosya Yolu: E:\JHoster\app\agent\test-runtime-portable-version-deep-revision.ps1
# 📌 Amac: Portable version deep revision endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.49.0
# Aciklama: Portable definitions, summary, family scan ve activate latest dry-run endpointleri icin smoke test yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751/api/v1/runtime-versions"

$Definitions = Invoke-RestMethod -Method Get -Uri "$BaseUrl/portable-definitions"
if ($Definitions.success -ne $true) {
    throw "portable-definitions basarisiz"
}

$Summary = Invoke-RestMethod -Method Get -Uri "$BaseUrl/portable-summary"
if ($Summary.success -ne $true) {
    throw "portable-summary basarisiz"
}

$PhpScan = Invoke-RestMethod -Method Get -Uri "$BaseUrl/php/portable-scan"
if ($PhpScan.success -ne $true) {
    throw "php portable-scan basarisiz"
}

$ApacheAliasScan = Invoke-RestMethod -Method Get -Uri "$BaseUrl/httpd/portable-scan"
if ($ApacheAliasScan.success -ne $true) {
    throw "httpd alias portable-scan basarisiz"
}

$LatestDryRun = Invoke-RestMethod -Method Post -Uri "$BaseUrl/php/activate-latest-portable?dry_run=true"
if ($LatestDryRun.success -ne $true -and $LatestDryRun.error -ne "portable latest version not found") {
    throw "activate-latest-portable dry-run beklenmeyen sonuc"
}

Write-Host "Portable version deep revision smoke test tamamlandi."
