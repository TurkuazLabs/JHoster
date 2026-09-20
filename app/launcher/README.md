# 📄 Dosya Yolu: E:\JHoster\app\launcher\README.md
# 📌 Amac: JHoster launcher, updater ve desktop ayrimini aciklar
# 📌 Modul - Markdown
# Version: 3.61.0
# Aciklama: JHoster.exe -> GitHub Release check -> updater -> desktop mimarisi icin uygulama notlari
# Bagimli Oldugu Katman: Tool

# JHoster Launcher Architecture

JHoster giris akisi uc parcaya ayrilir:

```text
JHoster.exe
  -> splash screen
  -> GitHub latest release check
  -> JHosterUpdater.exe
  -> app/desktop
```

## v3.61.0 durumu

Bu surumde JavaFX icinde guvenli bootstrap akisi eklendi:

- Splash ekran acilir.
- Local version `jhoster-desktop.properties` icinden okunur.
- GitHub latest release endpoint kontrolu yapilir.
- Repo tanimli degilse kontrol sessiz atlanir.
- Internet yoksa uygulama kilitlenmeden devam eder.
- Update varsa GitHub release sayfasi acma secenegi sunulur.
- Gercek dosya degistiren updater henuz calistirilmaz.

## GitHub repo ayari

Maven veya EXE calistirma sirasinda repo bilgisi verilir:

```text
-Djhoster.update.repo=owner/repo
```

Alternatif environment:

```text
JHOSTER_UPDATE_REPO=owner/repo
```

Update check kapatmak icin:

```text
-Djhoster.update.enabled=false
```

veya:

```text
JHOSTER_UPDATE_ENABLED=0
```

## Sonraki adim

v3.63.0 icinde `JHosterUpdater.exe` gercek dosya degistiren guvenli updater olarak ayrilacak:

```text
cache/updates
backup/updates
staging
sha256 verify
rollback
restart launcher
```
