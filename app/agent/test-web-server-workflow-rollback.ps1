# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-workflow-rollback.ps1
# 📌 Amac: Unified web server workflow rollback endpointini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Son workflow publish kaydindan rollback planini uretir ve dry-run modunda dogrular
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"
$BaseUrl = "http://127.0.0.1:8751"

Write-Host "JHoster web server workflow rollback test basladi"

Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site/rollback?dry_run=true" -Method Post | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$BaseUrl/api/v1/web-server-workflow/demo-site" -Method Get | ConvertTo-Json -Depth 20

Write-Host "JHoster web server workflow rollback test tamamlandi"
