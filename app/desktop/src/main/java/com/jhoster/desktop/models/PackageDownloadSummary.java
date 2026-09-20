// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\PackageDownloadSummary.java
// # 📌 Amac: Desktop package downloader ozet metinlerini tasir
// # 📌 Modul - Java
// # Version: 3.58.0
// # Aciklama: Package downloader API sonucunu UI icin standart model olarak saklar
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class PackageDownloadSummary {
    private final String title;
    private final String description;
    private final String body;

    public PackageDownloadSummary(String title, String description, String body) {
        this.title = title == null ? "" : title;
        this.description = description == null ? "" : description;
        this.body = body == null ? "" : body;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getBody() {
        return body;
    }
}
