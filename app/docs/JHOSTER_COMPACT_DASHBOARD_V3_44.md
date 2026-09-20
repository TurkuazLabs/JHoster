# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_COMPACT_DASHBOARD_V3_44.md
# 📌 Amac: JHoster compact dashboard ve Mailpit entegrasyon planini aciklar
# 📌 Modul - FileType
# Version: 3.44.0
# Aciklama: Laragon benzeri daha pratik ana ekran, Start All, Stop All ve Mailpit servis akisini dokumante eder

Bagimli Oldugu Katman: View | Service | Tool

# JHoster Compact Dashboard v3.44.0

Bu surum, JHoster Desktop ana ekranini gunluk kullanim icin daha pratik hale getirir.

## Ana hedef

Laragon ekranindaki hizli kontrol hissini koruyup JHoster mimarisindeki guvenli API-first akisla birlestirmek.

## Eklenen hizli aksiyonlar

- Start All
- Stop All
- Web
- Veritabani
- Mailpit
- Terminal
- Root
- Projects
- Logs

## Veritabani butonu

Veritabani butonu HeidiSQL Portable arar ve bulursa calistirir.

Beklenen ana yol:

```text
E:\JHoster\bin\heidisql\heidisql.exe
```

Alternatif yollar:

```text
E:\JHoster\tools\heidisql\heidisql.exe
E:\JHoster\apps\heidisql\heidisql.exe
E:\JHoster\usr\bin\heidisql\heidisql.exe
```

## Mailpit

Mailpit su degerlerle Desktop tarafina eklendi:

```text
Servis kodu: mailpit
SMTP port: 1025
Web port: 8025
Web URL: http://localhost:8025
```

## Guvenlik

- Start All ve Stop All gercek process calistirma acmaz.
- Desktop varsayilaninda `allow_real_execution=false` kalir.
- Service Manager islemleri halen guvenli simulated state ile calisir.
- Gercek executable baglantisi sadece real profile + guard akisi ile acilir.

## Sonraki adim

v3.45.0 icin dogru adim: Logs Viewer ve Service Config Shortcut panelidir.
