# 📄 Dosya Yolu: E:\JHoster\app\agent\test-package-downloads.ps1
# 📌 Amac: Package downloader Python testini PowerShell uzerinden calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Agent dizininde test-package-downloads.py dosyasini calistiran komut dosyasi
# Bagimli Oldugu Katman: Tool

Set-Location -LiteralPath $PSScriptRoot
python .\test-package-downloads.py
