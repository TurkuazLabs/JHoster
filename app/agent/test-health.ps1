# 📄 Dosya Yolu: E:\JHoster\app\agent\test-health.ps1
# 📌 Amac: JHoster agent health endpointini PowerShell ile test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Agent calisiyor mu kontrol eder
# Bagimli Oldugu Katman: Tool

Invoke-RestMethod -Uri "http://127.0.0.1:8751/api/v1/health"
