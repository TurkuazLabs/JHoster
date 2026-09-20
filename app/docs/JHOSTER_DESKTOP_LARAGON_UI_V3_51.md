# 📄 Dosya Yolu: E:\JHoster\app\docs\JHOSTER_DESKTOP_LARAGON_UI_V3_51.md
# 📌 Amac: JHoster Desktop v3.51 Laragon style UI revizyonunu aciklar
# 📌 Modul - Markdown
# Version: 3.51.0
# Aciklama: Compact servis kontrol satirlari, alt quick dock ve portable tool dock duzenini dokumante eder

Bagimli Oldugu Katman: View

# JHoster Desktop Laragon UI v3.51.0

Bu surumde Desktop ana ekran daha pratik bir Laragon benzeri kullanim akisi aldi.

## Ana hedef

- Start, Stop ve Restart butonlari compact servis satirlarina indi.
- Quick Actions alani sag panel olmaktan cikti ve dashboard alt dock yapisina dondu.
- Portable Tools dock eklendi.
- Veritabani butonu HeidiSQL Portable acma davranisini korudu.
- Agent kontrol butonlari ustte daha gorunur hale geldi.

## Compact service rows

Servis satirlari artik sadece durum gostermekle kalmaz.

Her satirda su aksiyonlar vardir:

- Start
- Stop
- Restart
- Status

Bu akis su servisleri kapsar:

- Apache
- Nginx
- MySQL
- PHP
- Mailpit

## Quick Actions dock

Dashboard altinda gunluk aksiyonlar tek satirda gorunur.

- Start All
- Stop All
- Web
- Veritabani
- Mailpit
- Terminal
- Root
- Projects
- Logs

## Portable Tools dock

Dashboard altinda ikinci dock olarak portable araclar gorunur.

- Bin
- Cmder
- Git Bash
- Notepad++
- Ngrok
- Composer
- Yarn

## HeidiSQL davranisi

Veritabani butonu once su yolu dener:

- E:\JHoster\bin\heidisql\heidisql.exe

Bulamazsa eski uyumluluk yollari denenir.

## Korunan mimari

- Controller sadece event handler baglar.
- Service is kararlarini yonetir.
- Tool dis dunya ve executable acma isini yapar.
- View sadece JavaFX ekranini kurar.
- Inline shell execution guard kurallari korunur.


## Test komutu

Desktop Maven compile testi icin:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\test-laragon-ui-compile.ps1
```
