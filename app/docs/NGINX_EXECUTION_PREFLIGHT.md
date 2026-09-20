# 📄 Dosya Yolu: E:\JHoster\docs\NGINX_EXECUTION_PREFLIGHT.md
# 📌 Amac: Nginx real execution preflight katmanini dokumante eder
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: Gercek nginx calistirma oncesi guvenlik kontrol akisini aciklar
# Bagimli Oldugu Katman: View

# JHoster Nginx Execution Preflight

Bu modul, `allow_real_execution=true` verilmeden once Nginx real adapter zincirinin guvenli olup olmadigini kontrol eder.

Kontrol edilen alanlar:

- Publish edilmis vhost config dosyasi var mi?
- Dosya `snapshot\vhosts\nginx-published` altinda mi?
- Dosya uzantisi `.conf` mu?
- Tespit edilen `nginx.exe` var mi?
- Dosya adi `nginx.exe` mi?
- Path kaynagi guvenli mi?
- Dosya Windows PE header tasiyor mu?
- Main `nginx.conf` var mi?
- Main config icinde `events`, `http`, `include` direktifleri var mi?
- Main config include satiri publish klasorunu isaret ediyor mu?
- Include path icinde bloklanan karakter/token var mi?

Guvenlik notu:

Bu modul gercek komut calistirmaz. `shell_execution=false` ve `real_nginx_execution=false` kalir.

Test komutu:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-execution-preflight.ps1
```

Beklenen sonuc:

Simulated `nginx.exe` kullaniliyorsa preflight `blocked` donebilir. Bu dogrudur; cunku dosya gercek Windows executable degildir ve PE header tasimaz.
