# 📄 Dosya Yolu: E:\JHoster\app\agent\test-apache-real-validate.ps1
# 📌 Amac: JHoster Apache real validate adapter akisini guvenli dry-run ve execution-skipped modda test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache vhost publish, executable detect ve httpd -t adapter planini gercek calistirma olmadan dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "JHoster Apache real validate test basladi"

$BaseUrl = "http://127.0.0.1:8751"
$ProjectCode = "demo-site"
$ApacheBinDir = "E:\JHoster\snapshot\apache\bin"
$ApacheConfDir = "E:\JHoster\snapshot\apache\conf"
$ApacheExeFile = "$ApacheBinDir\httpd.exe"
$ApacheMainConfigFile = "$ApacheConfDir\httpd.conf"

if (!(Test-Path $ApacheBinDir)) {
    New-Item -ItemType Directory -Path $ApacheBinDir -Force | Out-Null
}

if (!(Test-Path $ApacheConfDir)) {
    New-Item -ItemType Directory -Path $ApacheConfDir -Force | Out-Null
}

if (!(Test-Path $ApacheExeFile)) {
    Set-Content -Path $ApacheExeFile -Value "JHoster simulated apache httpd executable marker" -Encoding UTF8
}

Set-Content -Path $ApacheMainConfigFile -Encoding UTF8 -Value @"
ServerRoot "E:/JHoster/snapshot/apache"
Listen 80
LoadModule mpm_winnt_module modules/mod_mpm_winnt.so
LoadModule authz_core_module modules/mod_authz_core.so
LoadModule dir_module modules/mod_dir.so
LoadModule mime_module modules/mod_mime.so
DocumentRoot "E:/JHoster/user_www/demo-site/public"
<Directory "E:/JHoster/user_www/demo-site/public">
    Require all granted
</Directory>
Include "E:/JHoster/snapshot/vhosts/apache-published/*.conf"
"@

Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/local-cache/packages/demo-local-package/install?dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/runtime-versions/demo-local-package/activate?dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/projects?project_code=$ProjectCode&project_name=Demo%20Site&dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-vhosts/$ProjectCode/generate?dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-publish/$ProjectCode/publish?dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-executable/detect?dry_run=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apache-real-validate/$ProjectCode/plan" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-real-validate/$ProjectCode/validate?dry_run=true" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Post -Uri "$BaseUrl/api/v1/apache-real-validate/$ProjectCode/validate?dry_run=false&allow_real_execution=false" | ConvertTo-Json -Depth 16
Invoke-RestMethod -Method Get -Uri "$BaseUrl/api/v1/apache-real-validate/$ProjectCode" | ConvertTo-Json -Depth 16

Write-Host "JHoster Apache real validate test tamamlandi"
