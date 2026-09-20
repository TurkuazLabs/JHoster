# 📄 Dosya Yolu: E:\JHoster\app\agent\test-nginx-executable.ps1
# 📌 Amac: JHoster Nginx executable tespit endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Snapshot nginx.exe adayi olusturur, plan ve detect API kontrollerini yapar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster Nginx executable test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$NginxBinDir = "E:\JHoster\snapshot\nginx\bin"
$NginxExeFile = "$NginxBinDir\nginx.exe"

if (!(Test-Path $NginxBinDir)) {
    New-Item -ItemType Directory -Path $NginxBinDir -Force | Out-Null
}

if (!(Test-Path $NginxExeFile)) {
    Set-Content -Path $NginxExeFile -Value "JHoster simulated nginx executable marker" -Encoding UTF8
}

Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-executable/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-executable/detect?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-executable/detect?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-executable/latest" | ConvertTo-Json -Depth 12

Write-Host "JHoster Nginx executable test tamamlandi"
