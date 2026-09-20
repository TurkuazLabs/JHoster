# 📄 Dosya Yolu: E:\JHoster\docs\RUNTIME_PORTABLE_BIN_SCAN.md
# 📌 Amac: Portable bin version tarama ve aktif version secimi dokumani
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Laragon benzeri versionlu klasorlerin JHoster icinde nasil algilanacagini aciklar
# Bagimli Oldugu Katman: Service

# Runtime Portable Bin Scan

JHoster v3.48.0 ile runtime ve servis versionlari Laragon benzeri klasor duzeniyle algilanabilir.

## Temel mantik

Her teknoloji kendi `bin` alt klasorunde versionlu klasor olarak durur.

Ornekler:

```text
E:\JHoster\bin\php\php-8.3.30-Win32-vs16-x64
E:\JHoster\bin\apache\httpd-2.4.66-260223-Win64-VS18
E:\JHoster\bin\nginx\nginx-1.28.2
E:\JHoster\bin\memcached\memcached-1.6.8-win64-mingw
E:\JHoster\bin\python\python-3.13
```

## Endpointler

```text
GET  /api/v1/runtime-versions/portable-scan
GET  /api/v1/runtime-versions/{family}/portable-scan
POST /api/v1/runtime-versions/{family}/activate-portable?folder_name=...&dry_run=true
POST /api/v1/runtime-versions/{family}/activate-portable?folder_name=...&dry_run=false
```

## Desteklenen family degerleri

- `php`
- `apache`
- `nginx`
- `mysql`
- `mariadb`
- `node`
- `python`
- `memcached`
- `redis`
- `mailpit`

## Aktivasyon davranisi

`dry_run=false` ile portable version secildiginde iki is yapilir:

1. `runtime_versions.json` icinde ilgili family aktif version olarak kaydedilir.
2. Eger ayni family icin ana servis profili varsa `app_registry.json` icindeki ana servis `install_path` yeni version klasorune eslenir.

Bu sayede ornegin `apache` icin version klasoru secildiginde process preflight/start daha sonra secili klasor uzerinden calisabilir.

## Guvenlik

- Klasor adi path separator iceremez.
- Sadece JHoster root altindaki `bin/*` klasorleri taranir.
- Internetten download yapilmaz.
- Shell komutu calistirilmaz.
- Real process start/stop yine ayri guard ister.
