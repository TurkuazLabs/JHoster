# 📄 Dosya Yolu: E:\JHoster\docs\ARCHITECTURE.md
# 📌 Amac: JHoster katmanli mimarisini aciklar
# 📌 Modul - Markdown
# Version: 3.12.0
# Aciklama: Controller, Service, Repo, Tool, View ve Language katmanlarini ozetler
# Bagimli Oldugu Katman: View

# Architecture

JHoster agent katmanlari:

```text
Controller -> Service -> Repo -> Tool -> View -> Language
```

## Project manager akisi

```text
project_controller -> project_service -> project_registry_repository
project_service -> runtime_version_repository
project_service -> project_path_tool
```

Controller sadece request alir. Project olusturma kurali service katmanindadir. Dosya yolu dogrulama tool katmaninda yapilir. Kayitlar repository katmaninda JSON olarak saklanir.

## v3.12.0

- Virtual host snapshot generator eklendi.
- Config dosyalari sadece `snapshot/vhosts/nginx` altina yazilir.
- Sistem nginx ve hosts dosyalari otomatik degistirilmez.
