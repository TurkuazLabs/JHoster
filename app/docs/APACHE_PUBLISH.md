# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_PUBLISH.md
# 📌 Amac: Apache virtual host publish akisini aciklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Snapshot Apache vhost dosyasinin guvenli publish klasorune kopyalanmasi, backup ve checksum mantigi
# Bagimli Oldugu Katman: Language

# Apache Publish

Apache publish katmani, `snapshot\vhosts\apache` altinda uretilen Apache virtual host config dosyasini guvenli test publish klasorune kopyalar.

Varsayilan hedef:

`E:\JHoster\snapshot\vhosts\apache-published`

Gercek Apache klasorune yazmaz. Bu asamada sadece snapshot publish yapar.

## Akis

1. Apache vhost generate
2. Apache publish dry-run
3. Apache publish
4. Checksum dogrulama
5. Varsa onceki hedef dosya backup
6. Registry kaydi

## Endpointler

- `GET /api/v1/apache-publish`
- `GET /api/v1/apache-publish/{project_code}`
- `GET /api/v1/apache-publish/{project_code}/plan`
- `POST /api/v1/apache-publish/{project_code}/publish?dry_run=true`
- `POST /api/v1/apache-publish/{project_code}/publish?dry_run=false`

## Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-apache-publish.ps1
```
