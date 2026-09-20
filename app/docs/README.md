# 📄 Dosya Yolu: E:\JHoster\docs\README.md
# 📌 Amac: JHoster docs klasorunu aciklar
# 📌 Modul - Markdown
# Version: 3.21.0
# Aciklama: Dokuman basliklarini ve surum kapsamlarini listeler
# Bagimli Oldugu Katman: View

# Docs

Bu klasor JHoster agent, manifest, runtime version, project manager, nginx lifecycle, hosts lifecycle ve unified workflow ve workflow run tracking dokumanlarini tutar.

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.


## v3.14.0

Nginx validate katmani eklendi. Test: `E:\JHoster\app\agent\test-nginx-validate.ps1`.


## v3.15.0

Nginx reload katmani eklendi. Test: `E:\JHoster\app\agent\test-nginx-reload.ps1`.

- HOSTS_PUBLISH.md: Hosts publish snapshot dokumani.


## v3.17.0

Hosts apply admin/backup/rollback katmani eklendi. Test: `E:\JHoster\app\agent\test-hosts-apply.ps1`.

- HOSTS_APPLY.md: Hosts apply ve rollback dokumani.


## v3.18.0

Nginx executable detection katmani eklendi. Test: `E:\JHoster\app\agent\test-nginx-executable.ps1`.

- NGINX_EXECUTABLE.md: Nginx executable path discovery dokumani.


## v3.19.0 - Nginx Real Validate Adapter

- Nginx executable detect sonrasinda nginx -t real validate adapter katmani eklendi.
- Varsayilan test akisi shell calistirmadan dry-run ve execution skipped modunda kalir.
- Yeni endpoint grubu: `/api/v1/nginx-real-validate`.

- `NGINX_REAL_RELOAD.md`: Nginx real reload adapter dokumani.

- `NGINX_EXECUTION_PREFLIGHT.md` - Nginx real execution preflight dokumani.


## v3.24.0

- Apache virtual host generator eklendi.
- Apache publish/validate/reload henuz guard altindaki sonraki adimdir.


## v3.30.0

- `WEB_SERVER_WORKFLOW.md`: Active profile tabanli unified web server workflow dokumani.


## v3.31.0

- `WEB_SERVER_WORKFLOW.md`: Rollback guard parametreleri guncellendi.
- `WEB_SERVER_WORKFLOW_ROLLBACK.md`: Publish sonrasi hata durumunda geri alma davranisi eklendi.


## v3.32.0

- `WEB_SERVER_WORKFLOW_RUNS.md`: Run id, run listesi, proje bazli gecmis ve run detayi dokumani eklendi.
- `PROJECT_AUDIT_V3_32.md`: Workflow run tracking denetim raporu eklendi.


## v3.33.0

- `WEB_SERVER_WORKFLOW_LOCKS.md`: Unified workflow lock guard dokumani.
- `PROJECT_AUDIT_V3_33.md`: Lock guard audit raporu.
