# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_PORTABLE_VERSION_DEEP_REVISION_V3_49.md
# 📌 Amac: JHoster portable version mimarisi derin analiz ve revizyon notlari
# 📌 Modul - FileType
# Version: 3.49.0
# Aciklama: Laragon benzeri bin klasorlerinde version degistirme standardini JHoster'a uyarlar

Bagimli Oldugu Katman: Service | Repo | Tool | View | Config

## Tespit

Laragon yapisinda her ana teknoloji kendi `bin` klasoru altinda versionlu klasorlerle tutulur. Ornekler:

- `bin/php/php-8.3.30-Win32-vs16-x64`
- `bin/apache/httpd-2.4.66-260223-Win64-VS18`
- `bin/nginx/nginx-1.28.2`
- `bin/memcached/memcached-1.6.8-win64-mingw`
- `bin/python/python-3.13`

Bu nedenle JHoster icin dogru model sadece `runtime` degil, `portable family` modelidir.

## Revizyon karari

v3.49.0 ile `runtime-versions` endpoint grubu artik sadece PHP/Node/Python icin degil, version degistirilebilir tum portable aileler icin calisir.

Desteklenen aileler:

- apache
- nginx
- mysql
- mariadb
- php
- node
- python
- memcached
- redis
- mailpit

## Yeni prensip

Her aile icin standart kural:

```text
E:\JHoster\bin\{family}\{version-folder}\{executable}
```

Ornek:

```text
E:\JHoster\bin\php\php-8.3.30-Win32-vs16-x64\php.exe
E:\JHoster\bin\apache\httpd-2.4.66-260223-Win64-VS18\bin\httpd.exe
E:\JHoster\bin\nginx\nginx-1.28.2\nginx.exe
```

## Yeni endpointler

- `GET /api/v1/runtime-versions/portable-definitions`
- `GET /api/v1/runtime-versions/portable-summary`
- `POST /api/v1/runtime-versions/{family}/activate-latest-portable?dry_run=true`
- `POST /api/v1/runtime-versions/{family}/activate-latest-portable?dry_run=false`

## Var olan endpointlerin guclendirilmesi

- `GET /api/v1/runtime-versions/portable-scan`
- `GET /api/v1/runtime-versions/{family}/portable-scan`
- `POST /api/v1/runtime-versions/{family}/activate-portable?folder_name=...&dry_run=false`

Artik semantic version siralama, alias cozumu ve process profile sync daha guclu calisir.

## Alias destegi

- `httpd` -> `apache`
- `nodejs` -> `node`
- `py` -> `python`
- `mysqld` -> `mysql`

## Desktop revizyonu

Runtime Manager paneli `Portable Version Manager` mantigina genisletildi.

Panelde version secimi yapilabilecek aileler:

- Apache
- Nginx
- MySQL
- PHP
- Node
- Python
- Memcached
- Redis
- Mailpit

Her satirda:

- Active
- Activate
- Use Folder

## Guvenlik

- Version secimi sadece JHoster root altindaki `bin` klasorlerini kabul eder.
- Path traversal engellenir.
- Real process execution otomatik acilmaz.
- `real_process.enabled=false` korunur.
- Executable yoksa scan bunu raporlar ama calistirma acmaz.

## Kritik fark

Bu surumde JHoster, Laragon benzeri klasor mimarisine daha yakin hale geldi ancak daha kontrollu calisir:

- dry-run korunur
- active version JSON registry ile izlenir
- process profile sync ayridir
- real execution ayrica guard ister
