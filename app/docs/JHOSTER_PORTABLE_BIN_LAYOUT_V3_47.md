# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_PORTABLE_BIN_LAYOUT_V3_47.md
# 📌 Amac: JHoster portable bin layout ve Laragon klasor eslesmesini tanimlar
# 📌 Modul - Markdown
# Version: 3.47.0
# Aciklama: Bin klasoru, tray araclari ve servis profile eslesmelerini standardize eder

Bagimli Oldugu Katman: Config | Tool | View

# JHoster Portable Bin Layout v3.47.0

Bu surumde Laragon ekraninda gorulen `bin` mantigi JHoster tarafina standart olarak alindi.

## Standart bin klasorleri

| Klasor | Gorev |
|---|---|
| bin/apache | Apache portable servis dosyalari |
| bin/nginx | Nginx portable servis dosyalari |
| bin/mysql | MySQL portable servis dosyalari |
| bin/php | PHP runtime ailesi |
| bin/nodejs | Node.js runtime ailesi |
| bin/python | Python runtime ailesi |
| bin/mailpit | Mailpit mail catcher |
| bin/redis | Redis servis dosyalari |
| bin/memcached | Memcached servis dosyalari |
| bin/sendmail | Sendmail araci |
| bin/heidisql | HeidiSQL Portable |
| bin/cmder | Cmder terminal |
| bin/git | Git portable |
| bin/composer | Composer |
| bin/yarn | Yarn |
| bin/ngrok | Ngrok tunnel araci |
| bin/notepad++ | Notepad++ portable |
| bin/cronical | Scheduler araci |
| bin/telnet | Telnet araci |
| bin/jhoster | JHoster ic yardimci araclari |

## Desktop tray eslesmesi

Tray menude `Araclar` altina su hizli girisler eklendi:

- Bin
- Cmder
- Git Bash
- Notepad++
- Ngrok
- Composer
- Yarn

`Veritabani` butonu HeidiSQL Portable acmaya devam eder.

## Servis eslesmesi

Service registry icinde su servislerin install path degerleri bin layout ile hizalandi:

- apache -> bin/apache
- nginx -> bin/nginx
- mysql -> bin/mysql
- php -> bin/php
- mailpit -> bin/mailpit
- redis -> bin/redis
- memcached -> bin/memcached
- sendmail -> bin/sendmail

## Guvenlik

Real execution varsayilan olarak kapali kalir.

Gercek calistirma icin siralama:

1. Real profile apply
2. Preflight
3. allow_real_execution=true
4. Start / Stop / Restart

Bu akista shell komutu dogrudan UI tarafindan calistirilmaz.
