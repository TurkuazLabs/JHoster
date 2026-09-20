# 📄 Dosya Yolu: E:/JHoster/app/agent/test-api-surface-audit.ps1
# 📌 Amac: Agent API route yuzeyi ve DesktopApiConfig endpoint uyum testini calistirir
# 📌 Modul - PowerShell
# Version: 3.76.0
# Aciklama: Python API surface audit testini proje kokunden baslatir
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

$RootPath = Resolve-Path (Join-Path $PSScriptRoot "../..")
Push-Location $RootPath
try {
    python app/agent/test-api-surface-audit.py
}
finally {
    Pop-Location
}
