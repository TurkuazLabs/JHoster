# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_REAL_VALIDATE.md
# 📌 Amac: Apache real validate adapter akisini aciklar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: httpd.exe tespit kaydi ile httpd -t -f main config plan/dry-run/izinli calistirma kurallarini dokumante eder
# Bagimli Oldugu Katman: Language

# Apache Real Validate

Bu modul Apache icin gercek `httpd -t` adapter katmanidir.

Varsayilan davranis guvenlidir:

- `dry_run=true`
- `allow_real_execution=false`
- `shell_execution=false`

Gercek komut sadece su kosullarda calisir:

1. Apache vhost publish kaydi vardir.
2. `httpd.exe` tespit kaydi vardir.
3. Published vhost config dosyasi vardir.
4. Main `httpd.conf` vardir.
5. Path kontrolleri guvenlidir.
6. `allow_real_execution=true` acikca verilir.

Planlanan komut:

`httpd -t -f <main httpd.conf>`

Snapshot main config varsayilan yolu:

`E:\JHoster\snapshot\apache\conf\httpd.conf`

Ortama gore override:

`JHOSTER_APACHE_MAIN_CONFIG`

Endpointler:

- `GET /api/v1/apache-real-validate`
- `GET /api/v1/apache-real-validate/{project_code}`
- `GET /api/v1/apache-real-validate/{project_code}/plan`
- `POST /api/v1/apache-real-validate/{project_code}/validate?dry_run=true`
- `POST /api/v1/apache-real-validate/{project_code}/validate?dry_run=false&allow_real_execution=false`
