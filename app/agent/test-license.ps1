# 📄 Dosya Yolu: E:\JHoster\app\agent\test-license.ps1
# 📌 Amac: Agent license endpoint durumunu hizli test eder
# 📌 Modul - PowerShell
# Version: 3.65.0
# Aciklama: /api/v1/license endpointinden plan ve site kullanim bilgisini okur
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$BaseUrl = "http://127.0.0.1:8751"
$Endpoint = "$BaseUrl/api/v1/license"

$response = Invoke-RestMethod -Method Get -Uri $Endpoint
$response | ConvertTo-Json -Depth 8
