# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_FOLDER_STANDARD.md
# 📌 Amac: JHoster nihai klasor standardini tanimlar
# 📌 Modul - Markdown
# Version: 3.43.0
# Aciklama: Laragon benzeri ama daha genisleyebilir JHoster klasor yerlesimini ve sorumluluklarini belirler

Bagimli Oldugu Katman: Service

# JHoster Folder Standard v3.43.0

## Ana hedef

JHoster kok dizini, gunluk kullanimda Laragon kadar okunur; gelistirme tarafinda ise API, Desktop, service, runtime, template ve proje dosyalarini net ayirmalidir.

Ana kok:

```text
E:\JHoster
```

## Nihai kok klasorler

```text
E:\JHoster\
|-- agent\             # FastAPI agent kaynaklari ve API endpointleri
|-- desktop\           # JavaFX desktop kaynaklari
|-- app\               # Desktop/panel uygulama metadatalari
|-- backup\            # Otomatik ve manuel yedekler
|-- bin\               # Portable yardimci programlar
|-- cache\             # Indirme ve paket cache alani
|-- commands\          # Kullanici tarafindan calistirilacak ps1/cmd dosyalari
|-- config\            # Global JHoster config dosyalari
|-- data\              # Runtime state ve local veri dosyalari
|-- databases\         # DB dump, export ve snapshot dosyalari
|-- docs\              # Teknik dokumanlar
|-- etc\               # Web server ve runtime config dosyalari
|-- logs\              # Tum uygulama ve servis loglari
|-- modules\           # JHoster modul paketleri
|-- cache\packages\          # Local package kaynaklari
|-- www\          # Kullanici projeleri
|-- bin\          # PHP, Node, Python, Composer surumleri
|-- bin\          # Apache, Nginx, MySQL, Mailpit, Redis gibi servisler
|-- etc\ssl\               # Local CA ve domain sertifikalari
|-- templates\         # Quick App template dosyalari
|-- tmp\               # Gecici dosyalar
|-- tools\             # Agent/Desktop tool yardimcilari
|-- usr\               # Kullanici profili ve local ayarlar
|-- www\               # Varsayilan web root
```

## Portable arac standardi

Veritabani butonu HeidiSQL Portable icin once su yolu arar:

```text
E:\JHoster\bin\heidisql\heidisql.exe
```

Alternatif geriye uyumluluk yollari:

```text
E:\JHoster\tools\heidisql\heidisql.exe
E:\JHoster\apps\heidisql\heidisql.exe
E:\JHoster\usr\bin\heidisql\heidisql.exe
```

## Servis standardi

```text
E:\JHoster\bin\apache
E:\JHoster\bin\nginx
E:\JHoster\bin\mysql
E:\JHoster\bin\mailpit
E:\JHoster\bin\redis
```

Servis executable yollari real profile tarafindan kaydedilir. Desktop tarafinda real execution default kapali kalir.

## Runtime standardi

```text
E:\JHoster\bin\php\8.3
E:\JHoster\bin\php\8.2
E:\JHoster\bin\node\20
E:\JHoster\bin\node\22
E:\JHoster\bin\python\3.12
```

Aktif runtime secimi once JHoster registry icinde tutulur. PATH veya sistem environment degisikligi sonraki surumlerde ayrica guard ile acilacaktir.

## Proje standardi

```text
E:\JHoster\www\demo-site\
|-- public\
|-- config\
|-- storage\
|-- logs\
|-- .jhoster\
    |-- project.json
    |-- vhost.json
    |-- workflow.json
    |-- runtime.json
```

Controller proje dosyasi yazmaz. Proje olusturma Quick App Service tarafindan yonetilir. Storage ve dosya yazma Repo/Tool katmanindan yapilir.
