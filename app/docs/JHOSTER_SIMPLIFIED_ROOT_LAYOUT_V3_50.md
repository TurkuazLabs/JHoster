# 📄 Dosya Yolu: E:\JHoster\app\docs\JHOSTER_SIMPLIFIED_ROOT_LAYOUT_V3_50.md
# 📌 Amac: JHoster sade root klasor standardini dokumante eder
# 📌 Modul - Markdown
# Version: 3.50.0
# Aciklama: Laragon benzeri app/bin/data/etc/logs/tmp/www/backup/cache merkezli klasor yapisini aciklar

Bagimli Oldugu Katman: Service | Tool | Config

## Karar

JHoster root klasoru artik sade tutulur. Ust seviyede yalnizca ana calisma klasorleri bulunur.

```text
E:\JHoster\
├─ app\
├─ bin\
├─ data\
├─ etc\
├─ logs\
├─ tmp\
├─ www\
├─ backup\
└─ cache\
```

## Klasor gorevleri

| Klasor | Gorev |
|---|---|
| app | JHoster agent, desktop, docs, templates, themes, modules ve ic kaynaklar |
| bin | Portable servisler, runtime'lar ve araclar |
| data | Kalici veri ve JHoster state dosyalari |
| etc | Apache, Nginx, PHP, MySQL, SSL ve generated config dosyalari |
| logs | Agent, desktop ve servis loglari |
| tmp | Gecici dosyalar |
| www | Local web projeleri |
| backup | Proje, config ve database yedekleri |
| cache | Download, package ve manifest cache dosyalari |

## Tasima eslesmeleri

| Eski | Yeni |
|---|---|
| agent | app\agent |
| desktop | app\desktop |
| docs | app\docs |
| changelog | app\changelog |
| modules | app\modules |
| templates | app\templates |
| themes | app\themes |
| tools | app\tools |
| scripts | app\scripts |
| projects | www |
| services | bin |
| runtimes | bin |
| packages | cache\packages |
| ssl | etc\ssl |
| databases | data\mysql veya backup\mysql |
| agent\storage | data\jhoster |

## Runtime/version mantigi

Version degisebilen her sey kendi `bin` alt klasorunde tutulur.

```text
bin\php\php-8.3.30-Win32-vs16-x64\
bin\php\php-8.2.30-Win32-vs16-x64\
bin\apache\httpd-2.4.66-260223-Win64-VS18\
bin\nginx\nginx-1.28.2\
bin\python\python-3.13\
bin\memcached\memcached-1.6.8-win64-mingw\
```

## State konumu

JHoster state dosyalari artik `data\jhoster` altindadir.

```text
data\jhoster\app_registry.json
data\jhoster\process_state.json
data\jhoster\runtime_versions.json
data\jhoster\project_registry.json
data\jhoster\web_server_workflow_registry.json
data\jhoster\web_server_workflow_lock_registry.json
```

## Quick App konumu

Quick App artik proje scaffold dosyalarini `www` altina olusturur.

```text
www\demo-site\
www\opencart-demo\
www\wordpress-test\
```

## Yeni layout endpointleri

```text
GET  /api/v1/folder-layout
GET  /api/v1/folder-layout/plan
POST /api/v1/folder-layout/apply?dry_run=true
POST /api/v1/folder-layout/apply?dry_run=false
```

`apply` sadece standart klasorleri olusturur. Veri silmez.
