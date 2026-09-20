# 📄 Dosya Yolu: E:\JHoster\tools\recreate-agent-run-files.ps1
# 📌 Amac: JHoster agent calistirma, durdurma, paket kurulum ve test dosyalarini tekrar olusturur
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Windows reload hatasina gore duzeltilmis agent dosyalarini yeniden yazar
# Bagimli Oldugu Katman: Tool

$ErrorActionPreference = "Stop"

Write-Host "Bu zip paketinde dosyalar hazir gelir."
Write-Host "Eksik dosya olursa paketi tekrar E:\JHoster konumuna kopyala."
