# 📄 Dosya Yolu: E:\JHoster\app\docs\PROVISIONING_APPLY.md
# 📌 Amac: v3.78.0 kullanici onayli provisioning apply akisini dokumante eder
# 📌 Modul - Markdown
# Version: 3.79.0
# Aciklama: Dry-run, approval guard, package/runtime, web workflow ve MySQL database create siralamasini tanimlar
# Bagimli Oldugu Katman: Service | Tool | Config

# Provisioning Apply v3.78.0

JHoster New Site stack plani v3.78.0 ile ayri bir apply endpointine baglanir. Varsayilan davranis dry-run'dir. Gercek dosya, paket, web server veya database degisikligi icin `dry_run=false` ve `approved=true` birlikte gerekir.

## Endpointler

- `GET /api/v1/provisioning-apply`
- `GET /api/v1/provisioning-apply/{project_code}`
- `GET /api/v1/provisioning-apply/{project_code}/plan`
- `POST /api/v1/provisioning-apply/{project_code}/apply`

POST body icinde MySQL yonetici sifresi tasinabilir. Sifre query string'e yazilmaz, apply registry'ye kaydedilmez ve response icinde geri dondurulmez.

## Apply sirasi

1. Stack provisioning plan ve preflight.
2. Eksik ve indirilebilir paketlerin download/install islemi.
3. Gerekirse runtime activation.
4. Quick App scaffold ve project registry create.
5. Apache/Nginx profile selection.
6. Unified web server workflow generate/publish/validate/reload akisi.
7. MySQL seciliyse database create adapter.

MySQL adapter shell kullanmaz; `mysql.exe` process'i arguman listesi ile baslatilir. Admin sifresi `MYSQL_PWD` environment degeri ile process'e aktarilir ve kayit altina alinmaz.

Gercek MySQL apply preflight asamasinda `mysql.exe` discovery ve `executor.allow_shell_commands` kontrol edilir. Bu kosullardan biri hazir degilse Quick App create baslamadan apply bloklanir.


## Desktop v3.79.0

New Site Wizard ayni backend apply endpointini kullanir. `Plan Site` preflight calistirir. Plan hazir degilse gercek apply baslatilmaz. Hazir plan icin `Create Test Site` kullanici onayi ister.

MySQL seciliyse sifre JavaFX PasswordField uzerinden alinir ve yalniz JSON request body icinde kullanilir. Desktop request body loglanmaz.

Uzun apply islemi JavaFX `Task` ile arka planda calisir. Wizard progress alani `Applying provisioning...` durumunu gosterir; tamamlandiginda `Apply Steps` ve `Apply Run` ozetleri guncellenir. Failure dialog'u kullaniciya Workflow ekranini acarak web workflow run/rollback kayitlarini inceleme secenegi verir.
