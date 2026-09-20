# 📄 Dosya Yolu: E:\JHoster\docs\TESTING.md
# 📌 Amac: JHoster test komutlarini listeler
# 📌 Modul - Markdown
# Version: 3.23.0
# Aciklama: Agent endpoint smoke test ve project manager, nginx validate ve nginx reload test komutlarini tanimlar
# Bagimli Oldugu Katman: View

# Testing

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-health.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-local-packages.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-runtime-versions.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-www.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-virtual-hosts.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-publish.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-validate.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-reload.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-executable.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-validate.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-reload.ps1
```

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.15.0

- Nginx reload smoke test eklendi.
- Generate -> publish -> validate -> reload akisi test edilir.


## Hosts Publish Test

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-hosts-publish.ps1
```


## v3.17.0 Hosts Apply

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-hosts-apply.ps1
```


## v3.18.0 Nginx Executable

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-executable.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-validate.ps1
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-reload.ps1
```


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.


## v3.20.0 Nginx Real Reload

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\agent\test-nginx-real-reload.ps1
```

Beklenen guvenli sonuc: son real validate `valid` degilse real reload `rejected` doner ve gercek `nginx -s reload` calismaz.


## v3.23.0 - Derin Analiz ve Temizlik

- Paket temizligi, audit raporu ve Apache profile guard eklendi.
