# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-profiles.ps1
# 📌 Amac: JHoster web server profile endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Nginx ve Apache profil listeleme, planlama ve secim akisini test eder
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster web server profile test basladi"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles/current" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles/nginx" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles/apache" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles/apache/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/web-server-profiles/apache/select?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/web-server-profiles/nginx/select?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/web-server-profiles/current" | ConvertTo-Json -Depth 12
Write-Host "JHoster web server profile test tamamlandi"
