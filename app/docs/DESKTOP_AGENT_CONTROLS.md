# 📄 Dosya Yolu: E:\JHoster\docs\DESKTOP_AGENT_CONTROLS.md
# 📌 Amac: Desktop agent start stop restart butonlarinin davranisini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: JavaFX launcher icindeki agent lifecycle kontrollerinin kullanim notlari
# Bagimli Oldugu Katman: Language

# Desktop Agent Controls

JHoster Desktop uzerindeki agent lifecycle kontrolleri sunlardir:

- Start Agent
- Stop Agent
- Restart Agent
- Open Panel
- Check Status

## Start Agent

`E:\JHoster\app\agent\main.py` dosyasini `python main.py` komutu ile baslatir.

## Stop Agent

Sadece Desktop tarafindan baslatilmis managed process'i durdurur.

Harici PowerShell, CMD veya servis olarak baslatilmis agent process bu butonla kapatilmaz.

## Restart Agent

Once managed process icin stop dener, sonra agent'i tekrar baslatir.

## Check Status

`http://127.0.0.1:8751/api/v1/health` endpointini kontrol eder.
