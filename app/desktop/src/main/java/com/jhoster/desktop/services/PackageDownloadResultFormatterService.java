// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\PackageDownloadResultFormatterService.java
// # 📌 Amac: Package downloader API cevaplarini okunabilir UI ozetine cevirir
// # 📌 Modul - Java
// # Version: 3.58.0
// # Aciklama: HTTP sonucunu baslik, aciklama ve log govdesi olarak formatlayan service katmani
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.PackageDownloadSummary;

public final class PackageDownloadResultFormatterService {
    public PackageDownloadSummary format(String title, String description, DesktopHttpResult result) {
        String safeTitle = title == null ? "Package Downloader" : title;
        String safeDescription = description == null ? "" : description;
        return new PackageDownloadSummary(safeTitle, safeDescription, result.toLogBlock());
    }
}
