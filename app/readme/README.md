# 📄 Dosya Yolu: E:\JHoster\readme\README.md
# 📌 Amac: JHoster readme ek dokuman klasorunu aciklar
# 📌 Modul - Markdown
# Version: 3.19.0
# Aciklama: Quick start ve project status dosyalarina yonlendirir
# Bagimli Oldugu Katman: View

# Readme

- `QUICK_START.md`
- `PROJECT_STATUS.md`

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.14.0

Nginx validate katmani eklendi. Test: `E:\JHoster\app\agent\test-nginx-validate.ps1`.


## v3.18.0

Nginx executable detection eklendi. Test: `E:\JHoster\app\agent\test-nginx-executable.ps1`.


## v3.20.0

- Nginx real reload adapter eklendi.
- Real reload, son real validate `valid` olmadan calismaz.
