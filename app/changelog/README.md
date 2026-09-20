# 📄 Dosya Yolu: E:\JHoster\changelog\README.md
# 📌 Amac: JHoster changelog klasorunu aciklar
# 📌 Modul - Markdown
# Version: 3.19.0
# Aciklama: Surum notlarinin nasil tutuldugunu belirtir
# Bagimli Oldugu Katman: View

# Changelog

Her modul veya bakim surumu icin ayri markdown dosyasi tutulur.

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.15.0

- Nginx reload surum notu eklendi.
- Reload test ve guvenlik notlari ayrildi.


- v3.16.0: Hosts publish snapshot katmani eklendi.


## v3.17.0

Hosts apply admin, backup ve rollback surumu eklendi.


## v3.18.0

Nginx executable detection surum notu eklendi.


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.

- v3.21.0 - Nginx execution preflight katmani eklendi.


## v3.23.0 - Derin Analiz ve Temizlik

- Paket temizligi, audit raporu ve Apache profile guard eklendi.
