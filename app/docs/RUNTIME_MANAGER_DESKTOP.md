# 📄 Dosya Yolu: E:\JHoster\docs\RUNTIME_MANAGER_DESKTOP.md
# 📌 Amac: Desktop Runtime Manager ozelligini aciklar
# 📌 Modul - Markdown
# Version: 3.41.0
# Aciklama: PHP, Node ve Python runtime secimi icin Desktop UI ve agent endpoint akisini belgeler
# Bagimli Oldugu Katman: View

# Runtime Manager Desktop

JHoster v3.41.0 ile Desktop ana ekranina Runtime Manager karti eklendi.

## Amac

PHP, Node ve Python runtime surumlerini tek ekranda gormek ve aktif runtime secimini agent uzerinden yonetmek.

## Endpointler

- `GET /api/v1/runtime-versions`
- `GET /api/v1/runtime-versions/active`
- `GET /api/v1/runtime-versions/{family}/active`
- `POST /api/v1/runtime-versions/{component_code}/activate?dry_run=false`

## Varsayilan runtime kodlari

- PHP: `php-8.3`
- Node: `node-20`
- Python: `python-3.12`

## Guvenlik

Runtime aktivasyonu su an sadece JSON registry uzerinde aktif secimi kaydeder. Windows PATH, symlink veya gercek process degisikligi yapmaz.

## Sonraki adim

Runtime aktivasyonu sonrasinda PHP, Node ve Python icin PATH shim veya launcher wrapper katmani eklenecek.
