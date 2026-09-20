# 📄 Dosya Yolu: scripts/start-agent.ps1
# 📌 Amac: Windows PowerShell uzerinden Python agent baslatir
# 📌 Modul - PowerShell
# Version: 3.2.0
# Aciklama: Gelistirme ortaminda hizli agent calistirma yardimcisidir

# Bagimli Oldugu Katman: Tool

Set-Location "$PSScriptRoot\..\agent"
python -m pip install -r requirements.txt
python main.py
