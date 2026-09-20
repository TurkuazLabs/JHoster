# 📄 Dosya Yolu: E:\JHoster\docs\MANIFEST_GUIDE.md
# 📌 Amac: JHoster manifest yapisini aciklar
# 📌 Modul - Markdown
# Version: 3.11.0
# Aciklama: Local package ve runtime family alanlarini dokumante eder
# Bagimli Oldugu Katman: View

# Manifest Guide

Runtime paketleri manifest icinde `installer.runtime_family` alanini kullanir. Project manager, aktif runtime family secimini bu alan uzerinden kullanir.

```yaml
installer:
  runtime_adapter: simulated
  runtime_family: demo-local-package
  mode: local_package
```

Gercek download halen kapali tutulur. Paketler cache altindan checksum ile dogrulanarak kurulur.
