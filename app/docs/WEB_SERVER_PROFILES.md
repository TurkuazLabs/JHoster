# 📄 Dosya Yolu: E:\JHoster\docs\WEB_SERVER_PROFILES.md
# 📌 Amac: JHoster web server profile secim sistemini aciklar
# 📌 Modul - Markdown
# Version: 1.1.0
# Aciklama: Nginx ve Apache adapter secim mimarisi, ready/planned guard kurallari
# Bagimli Oldugu Katman: Language

# JHoster Web Server Profiles

JHoster web server secimini tek bir profil katmani uzerinden yonetir.

## Mevcut profiller

- `nginx`: `ready` durumundadir. Publish, validate, reload, executable, real validate/reload guard ve preflight zinciri vardir.
- `apache`: `planned` durumundadir. Profil katalogda gorunur ama adapter zinciri tamamlanana kadar aktif secilemez.

## Secim kurali

Bir web server profilinin aktif secilebilmesi icin:

- Profil katalogda bulunmalidir.
- Profil desteklenen kodlardan biri olmalidir.
- Profil `ready` durumunda olmalidir.

Bu nedenle v3.23.0 durumunda:

- `nginx` secilebilir.
- `apache` listelenir fakat `web_server_profile_not_ready` ile reddedilir.

## Endpointler

- `GET /api/v1/web-server-profiles`
- `GET /api/v1/web-server-profiles/current`
- `GET /api/v1/web-server-profiles/nginx`
- `GET /api/v1/web-server-profiles/apache`
- `GET /api/v1/web-server-profiles/{server_code}/plan`
- `POST /api/v1/web-server-profiles/{server_code}/select?dry_run=true`
- `POST /api/v1/web-server-profiles/{server_code}/select?dry_run=false`

## Tasarim karari

Nginx ve Apache ayni controller/service/repo/tool prensibiyle ilerleyecek.
Her adapter kendi publish, validate, reload ve preflight katmanina sahip olacak.

## Sonraki adim

Apache icin ilk gercek adim `apache-vhosts` generator katmanidir.
