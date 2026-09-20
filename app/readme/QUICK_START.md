# 📄 Dosya Yolu: E:\JHoster\readme\QUICK_START.md
# 📌 Amac: JHoster hizli baslangic komutlarini listeler
# 📌 Modul - Markdown
# Version: 3.19.0
# Aciklama: Agent baslatma ve project manager testini hizli sekilde calistirir
# Bagimli Oldugu Katman: View

# Quick Start

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\run-agent.ps1
```

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-www.ps1
```

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.14.0

Nginx validate katmani eklendi. Test: `E:\JHoster\app\agent\test-nginx-validate.ps1`.


## Hosts apply testi

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-hosts-apply.ps1
```


## v3.18.0

Nginx executable detection eklendi. Test: `E:\JHoster\app\agent\test-nginx-executable.ps1`.


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.


## v3.20.0

- Nginx real reload adapter eklendi.
- Real reload, son real validate `valid` olmadan calismaz.

- Nginx preflight test: `powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-execution-preflight.ps1`
