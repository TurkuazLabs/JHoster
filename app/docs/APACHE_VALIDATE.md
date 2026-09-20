# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_VALIDATE.md
# 📌 Amac: Apache validate katmaninin kullanimini ve guvenlik davranisini aciklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Apache publish sonrasi internal static scan dogrulama dokumani
# Bagimli Oldugu Katman: Language

# Apache Validate

Apache validate katmani, publish edilmis Apache virtual host config dosyasini gercek `httpd -t` calistirmadan once guvenli internal static scan ile kontrol eder.

## Akis

1. Apache vhost generate
2. Apache publish
3. Apache validate plan
4. Apache validate dry-run
5. Apache validate static scan

## Endpointler

- `GET /api/v1/apache-validate`
- `GET /api/v1/apache-validate/{project_code}`
- `GET /api/v1/apache-validate/{project_code}/plan`
- `POST /api/v1/apache-validate/{project_code}/validate?dry_run=true`
- `POST /api/v1/apache-validate/{project_code}/validate?dry_run=false`

## Kontroller

- Dosya bos degil
- Hedef dosya `snapshot\vhosts\apache-published` altinda
- Uzanti `.conf`
- `VirtualHost`, `ServerName`, `DocumentRoot`, `Directory`, `Require all granted` direktifleri mevcut
- `<VirtualHost>` ve `</VirtualHost>` dengeli
- `<Directory>` ve `</Directory>` dengeli
- Riskli path tokenlari yok

Gercek Apache `httpd -t` adapteri sonraki surumde ayrica eklenecektir.
