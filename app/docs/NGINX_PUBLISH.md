# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_PUBLISH.md
# 📌 Amac: JHoster Nginx publish modulunun kullanimini aciklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Snapshot virtual host config dosyasinin guvenli publish akis dokumani
# Bagimli Oldugu Katman: View

# Nginx Publish

JHoster v3.13.0 ile virtual host config uretiminden sonra guvenli publish katmani eklendi.

## Akis

Controller -> Service -> Repo -> Tool -> View

## Endpointler

- GET /api/v1/nginx-publish
- GET /api/v1/nginx-publish/{project_code}
- GET /api/v1/nginx-publish/{project_code}/plan
- POST /api/v1/nginx-publish/{project_code}/publish?dry_run=true
- POST /api/v1/nginx-publish/{project_code}/publish?dry_run=false

## Varsayilan hedef

Publish islemi bu surumde gercek sistem Nginx klasorune yazmaz.

Varsayilan hedef:

E:\JHoster\snapshot\vhosts\nginx-published

## Guvenlik

- Kaynak config sadece snapshot\vhosts\nginx altindan okunur.
- Hedef config sadece snapshot\vhosts\nginx-published altina yazilir.
- Sadece .conf uzantisi kabul edilir.
- Mevcut hedef dosya varsa once backup alinir.
- Kaynak ve hedef SHA256 checksum karsilastirilir.
