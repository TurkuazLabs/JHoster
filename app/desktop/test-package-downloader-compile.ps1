# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-package-downloader-compile.ps1
# 📌 Amac: Package downloader UI baglantilari icin Maven compile testini calistirir
# 📌 Modul - PowerShell
# Version: 1.0.0
# Aciklama: Desktop app compile ve JavaFX exec kontrolu icin yardimci script
# Bagimli Oldugu Katman: Tool

Set-Location -LiteralPath $PSScriptRoot
mvn --no-transfer-progress process-classes
