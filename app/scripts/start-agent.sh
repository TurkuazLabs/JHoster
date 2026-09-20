# 📄 Dosya Yolu: scripts/start-agent.sh
# 📌 Amac: Linux/macOS uzerinden Python agent baslatir
# 📌 Modul - Shell
# Version: 3.2.0
# Aciklama: Gelistirme ortaminda hizli agent calistirma yardimcisidir

# Bagimli Oldugu Katman: Tool

cd "$(dirname "$0")/../agent" || exit 1
python3 -m pip install -r requirements.txt
python3 main.py
