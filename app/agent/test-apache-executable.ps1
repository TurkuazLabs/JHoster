# 📄 Dosya Yolu: E:\JHoster\app\agent\test-apache-executable.ps1
# 📌 Amac: JHoster Apache executable tespit endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Snapshot httpd.exe adayi olusturur, plan ve detect API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster Apache executable test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ApacheBinDir = "E:\JHoster\snapshot\apache\bin"
$ApacheExeFile = "$ApacheBinDir\httpd.exe"

if (!(Test-Path $ApacheBinDir)) {
    New-Item -ItemType Directory -Path $ApacheBinDir -Force | Out-Null
}

if (!(Test-Path $ApacheExeFile)) {
    Set-Content -Path $ApacheExeFile -Value "JHoster simulated apache httpd executable marker" -Encoding UTF8
}

Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apache-executable/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-executable/detect?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-executable/detect?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apache-executable/latest" | ConvertTo-Json -Depth 12

Write-Host "JHoster Apache executable test tamamlandi"
