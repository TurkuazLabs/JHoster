# 📄 Dosya Yolu: E:\JHoster\docs\JHOSTER_DESKTOP_WIREFRAME.md
# 📌 Amac: JHoster Desktop ana ekran wireframe planini tanimlar
# 📌 Modul - Markdown
# Version: 3.43.0
# Aciklama: Laragon benzeri ama daha modern JHoster dashboard yerlesimini ve buton davranislarini belirler

Bagimli Oldugu Katman: View

# JHoster Desktop Wireframe v3.43.0

## Tasarim hedefi

Ana ekran tek bakista su cevaplari vermelidir:

- Hangi servisler calisiyor?
- Aktif web server profili Apache mi Nginx mi?
- Aktif PHP/Node/Python surumu ne?
- Proje root nerede?
- Veritabani, terminal, root, logs ve web hizli aciliyor mu?

## Ekran yapisi

```text
+--------------------------------------------------------------------------------+
| JHoster Dashboard                                   Profile | PHP | Running     |
+--------------------------------------------------------------------------------+
| Quick Actions: Web | Veritabani | Terminal | Root | Projects | Logs             |
+--------------------------------------------------------------------------------+
| Services                         | Projects / Quick App                         |
| Apache  status port actions      | Active project                               |
| Nginx   status port actions      | Local URL                                    |
| MySQL   status port actions      | Create App / Plan App                         |
| Mailpit status port actions      | Workflow dry-run                              |
+--------------------------------------------------------------------------------+
| Runtime Manager                  | Workflow Summary                              |
| PHP active/switch                | profile/status/run/lock                       |
| Node active/switch               | generate -> publish -> validate -> reload     |
| Python active/switch             | rollback guard                                |
+--------------------------------------------------------------------------------+
| Activity Log                                                                    |
+--------------------------------------------------------------------------------+
```

## Quick action davranislari

| Buton | Davranis |
|---|---|
| Web | `http://localhost` adresini varsayilan tarayicida acar |
| Veritabani | HeidiSQL Portable executable dosyasini acar |
| Terminal | JHoster kok klasorunde PowerShell acar |
| Root | `E:\JHoster` klasorunu acar |
| Projects | `E:\JHoster\www` klasorunu acar |
| Logs | `E:\JHoster\logs` klasorunu acar |

## Veritabani butonu

Veritabani butonu kesin olarak HeidiSQL Portable icin tasarlanmistir.

Arama sirası:

```text
E:\JHoster\bin\heidisql\heidisql.exe
E:\JHoster\tools\heidisql\heidisql.exe
E:\JHoster\apps\heidisql\heidisql.exe
E:\JHoster\usr\bin\heidisql\heidisql.exe
```

Dosya bulunamazsa Activity Log icinde denenmis yollar gosterilir.

## UI ilkeleri

- Acik tema default kalir.
- Alt hizli butonlar Laragon gibi pratik olur.
- Ham JSON sadece debug/log alaninda kalir.
- Kartlar sade ve okunur olur.
- Gercek start/stop/reload default kapali kalir.
- Real execution daima guard ister.
