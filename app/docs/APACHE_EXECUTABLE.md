# 📄 Dosya Yolu: E:\JHoster\docs\APACHE_EXECUTABLE.md
# 📌 Amac: Apache executable tespit katmanini aciklar
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: httpd.exe path tarama, dry-run ve registry akis dokumani
# Bagimli Oldugu Katman: View

# Apache Executable Detection

Bu modul Apache icin `httpd.exe` dosyasini shell calistirmadan tespit eder.

## Guvenlik

- Varsayilan akis dry-run olarak baslar.
- Shell calistirma yoktur.
- Gercek `httpd -v` veya `httpd -t` calistirilmaz.
- Env, snapshot ve standart Windows path adaylari kontrol edilir.
- Aday dosya adi `httpd.exe` degilse guvenli sayilmaz.
- Snapshot icindeki aday proje kokunun disina cikamaz.

## Endpointler

- `GET /api/v1/apache-executable`
- `GET /api/v1/apache-executable/latest`
- `GET /api/v1/apache-executable/plan`
- `POST /api/v1/apache-executable/detect?dry_run=true`
- `POST /api/v1/apache-executable/detect?dry_run=false`

## Snapshot test hedefi

`E:\JHoster\snapshot\apache\bin\httpd.exe`

## Sonraki adim

Bu tespit katmanindan sonra Apache real validate adapter eklenecektir.
