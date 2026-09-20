# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_VALIDATE.md
# 📌 Amac: JHoster Nginx validate katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 3.14.0
# Aciklama: Publish edilmis Nginx config dosyasi icin guvenli validate akisinin endpoint ve test komutlarini aciklar
# Bagimli Oldugu Katman: View

# Nginx Validate

Bu modul publish edilmis Nginx virtual host config dosyasini gercek sistem nginx konumuna dokunmadan dogrular.

## Guvenlik sinirlari

- Sadece `snapshot/vhosts/nginx-published` altindaki `.conf` dosyalari kontrol edilir.
- Gercek `nginx -t` komutu bu surumde calistirilmaz.
- Bu surum internal static scan yapar.
- Path traversal engellenir.
- Validate sonucu registry dosyasina kaydedilir.

## Endpointler

```text
GET  /api/v1/nginx-validate
GET  /api/v1/nginx-validate/{project_code}
GET  /api/v1/nginx-validate/{project_code}/plan
POST /api/v1/nginx-validate/{project_code}/validate?dry_run=true
POST /api/v1/nginx-validate/{project_code}/validate?dry_run=false
```

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-validate.ps1
```

## Beklenen sonuc

- Plan sonucu `status: planned` doner.
- Validate sonucu `status: valid` doner.
- Registry kaydi `data/jhoster/nginx_validate_registry.json` icine yazilir.

## Sonraki adim

Bundan sonraki surumde gercek Nginx adapter uzerinden kontrollu `nginx -t` ve reload plan katmani eklenebilir.
