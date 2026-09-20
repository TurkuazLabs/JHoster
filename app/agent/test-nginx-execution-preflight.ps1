# 📄 Dosya Yolu: E:\JHoster\app\agent\test-nginx-execution-preflight.ps1
# 📌 Amac: JHoster Nginx real execution preflight endpointlerini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Real execution oncesi executable, main config ve include zinciri guvenlik kontrolunu calistirir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster Nginx execution preflight test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$Domain = "demo-site.localhost"
$NginxBinDir = "E:\JHoster\snapshot\nginx\bin"
$NginxConfDir = "E:\JHoster\snapshot\nginx\conf"
$NginxExeFile = "$NginxBinDir\nginx.exe"
$NginxMainConfigFile = "$NginxConfDir\nginx.conf"

if (!(Test-Path $NginxBinDir)) {
    New-Item -ItemType Directory -Path $NginxBinDir -Force | Out-Null
}

if (!(Test-Path $NginxConfDir)) {
    New-Item -ItemType Directory -Path $NginxConfDir -Force | Out-Null
}

if (!(Test-Path $NginxExeFile)) {
    Set-Content -Path $NginxExeFile -Value "JHoster simulated nginx executable marker" -Encoding UTF8
}

$MainConfigContent = @"
events {}
http {
    include E:/JHoster/snapshot/vhosts/nginx-published/*.conf;
}
"@

Set-Content -Path $NginxMainConfigFile -Value $MainConfigContent -Encoding UTF8

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&runtime_family=demo-local-package&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/virtual-hosts/$ProjectCode/generate?domain=$Domain&port=80&dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-publish/$ProjectCode/publish?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-executable/detect?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-execution-preflight/$ProjectCode/plan" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-execution-preflight/$ProjectCode/preflight?dry_run=true" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/nginx-execution-preflight/$ProjectCode/preflight?dry_run=false" | ConvertTo-Json -Depth 12
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/nginx-execution-preflight/$ProjectCode" | ConvertTo-Json -Depth 12

Write-Host "JHoster Nginx execution preflight test tamamlandi"
