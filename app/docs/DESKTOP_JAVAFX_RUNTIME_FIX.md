# 📄 Dosya Yolu: E:\JHoster\docs\DESKTOP_JAVAFX_RUNTIME_FIX.md
# 📌 Amac: JHoster Desktop JavaFX runtime hatasinin nedenini ve cozumunu belgeler
# 📌 Modul - Markdown
# Version: 1.0.0
# Aciklama: NetBeans Maven exec akisi icin JavaFX Application launcher ayrimini aciklar
# Bagimli Oldugu Katman: View

# Desktop JavaFX Runtime Fix

## Problem

NetBeans Maven calistirma akisi asagidaki hatayi uretiyordu:

```text
Error: JavaFX runtime components are missing, and are required to run this application
```

## Neden

`MainApp` dogrudan `javafx.application.Application` sinifindan turetilmisti.
NetBeans ise uygulamayi standart `exec:exec` classpath akisiyle baslatiyordu.
Bu durumda Java launcher, JavaFX runtime module path hazir degilse uygulamayi baslatmiyordu.

## Cozum

`MainApp` artik normal Java launcher sinifidir.
Gercek JavaFX yasam dongusu `FxApplication` sinifina tasindi.

Akis:

```text
MainApp -> Application.launch(FxApplication.class, args) -> LauncherController -> LauncherView
```

## Kontrol

Java 21 aktif olmali:

```powershell
java -version
javac -version
```

Uygulama su komutla calistirilabilir:

```powershell
cd E:\JHoster\app\desktop
mvn clean javafx:run
```

NetBeans kendi `exec:exec` akisiyle calistirdiginda da `MainApp` artik JavaFX Application sinifindan turemedigi icin runtime component guard hatasi asilmis olur.
