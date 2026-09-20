# 📄 Dosya Yolu: E:\JHoster\app\docs\WEB_SERVER_MODE_SETTINGS.md
# 📌 Amac: Apache/Nginx aktif web server mode ayarinin nasil calistigini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Secilebilir web server profile, ortak www document root ve port guard davranisini dokumante eder

Bagimli Oldugu Katman: Config | Service | Repo | Tool | View

# Active Web Server Mode

JHoster icinde Apache ve Nginx ayni anda 80/443 public portlarini sahiplenmez. Kullanici aktif web server olarak Apache veya Nginx secer. Secili olmayan web server start/restart istegi backend tarafinda engellenir.

## Ortak document root

Iki web server da ortak proje klasorunu kullanir:

```text
E:\JHoster\www
```

Bu sayede Apache veya Nginx arasinda gecis yapildiginda projelerin yeri degismez.

## Davranis

- Apache secilirse Nginx durdurulur ve Apache baslatilir.
- Nginx secilirse Apache durdurulur ve Nginx baslatilir.
- Start All secili web server profilini okur.
- Secili olmayan web server icin manuel Start/Restart profile mismatch ile bloke edilir.

## State dosyasi

Aktif secim su dosyada saklanir:

```text
E:\JHoster\data\jhoster\web_server_profile_registry.json
```
