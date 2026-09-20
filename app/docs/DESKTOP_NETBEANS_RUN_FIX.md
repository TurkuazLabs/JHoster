# 📄 Dosya Yolu: E:\JHoster\docs\DESKTOP_NETBEANS_RUN_FIX.md
# 📌 Amac: NetBeans packageClassName placeholder hatasinin cozumunu belgeler
# 📌 Modul - Markdown
# Version: 3.2.2
# Aciklama: JHoster Desktop Maven run action icin MainApp sabitleme notlari
# Bagimli Oldugu Katman: Tool

# JHoster Desktop NetBeans Run Fix

## Problem

NetBeans Maven run komutu bazen main class degerini su sekilde gonderir:

```text
-Dexec.mainClass=${packageClassName}
```

Bu placeholder cozulemezse Java su hatayi verir:

```text
Could not find or load main class ${packageClassName}
```

## Cozum

`desktop/nbactions.xml` eklendi ve run/debug action icinde main class sabitlendi:

```text
com.jhoster.desktop.MainApp
```

## Manuel Calistirma

NetBeans hala eski action cache ile calisirsa su script kullanilir:

```powershell
powershell -ExecutionPolicy Bypass -File E:\JHoster\app\desktop\commands\run-desktop-netbeans-fixed.ps1
```

## NetBeans Icin Ek Kontrol

NetBeans icinde:

Project Properties -> Run -> Main Class

alaninin su deger oldugundan emin ol:

```text
com.jhoster.desktop.MainApp
```
