# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_TRAY_MENU_V3_46.md
# 📌 Amac: JHoster Desktop tray menu tasarimini ve davranisini tanimlar
# 📌 Modul - Markdown
# Version: 3.46.0
# Aciklama: Laragon benzeri alt sistem tepsisi menusunun JHoster icin nasil uygulanacagini aciklar

Bagimli Oldugu Katman: View

# JHoster Tray Menu v3.46.0

Bu surumde JHoster Desktop uygulamasina Laragon benzeri sistem tepsisi menusu eklenmistir.

## Amac

JHoster ana penceresi kapatilsa bile uygulama arka planda kalabilmeli ve kullanici alt sag sistem tepsisinden temel islemleri hizli sekilde yapabilmelidir.

## Menu yapisi

- JHoster Goster
- Gizle
- Panel
- JHoster
  - Web
  - Root
  - Projects
  - Logs
- www
- Hizli uygulama
  - Ac
  - Projects
- Araclar
  - Terminal
  - Veritabani
  - Mailpit
  - Logs
- Nginx
  - Status
  - Start
  - Stop
  - Restart
- MySQL
  - Status
  - Start
  - Stop
  - Restart
  - Veritabani
- Mailpit
  - Status
  - Start
  - Stop
  - Restart
  - Ac
- Node.js
- PHP
- Python
- Durdur
- Profil
- Secenekler
- Cikis

## Guvenlik

- Tray start/stop islemleri mevcut Service Manager guard akisini kullanir.
- Gercek process execution Desktop tarafinda hala kapali kalir.
- Veritabani aksiyonu HeidiSQL Portable arama yolunu kullanir.
- Cikis menusu tray ikonunu kaldirip JavaFX uygulamasini kapatir.
- Pencere kapatma islemi uygulamayi sonlandirmak yerine gizler.

## Not

Bu surum tray menu iskeletini getirir. Sonraki surumde menudeki servis check durumlari gercek status bilgisiyle dinamik hale getirilebilir.
