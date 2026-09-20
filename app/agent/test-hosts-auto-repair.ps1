# 📄 Dosya Yolu: E:/JHoster/app/agent/test-hosts-auto-repair.ps1
# 📌 Amac: Hosts auto inspect ve repair endpointlerini test eder
# 📌 Modul - PowerShell
# Version: 3.67.0
# Aciklama: Snapshot modda inspect, repair-plan ve repair akisini dogrular
# Bagimli Oldugu Katman: Tool

$BaseUrl = "http://127.0.0.1:8751/api/v1/hosts-auto"

Write-Host "JHoster Hosts Auto Repair Test"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/inspect?real_write=false"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/repair-plan?real_write=false"
Invoke-RestMethod -Method Post -Uri "$BaseUrl/repair?real_write=false&dry_run=false"
Invoke-RestMethod -Method Get -Uri "$BaseUrl/inspect?real_write=false"
