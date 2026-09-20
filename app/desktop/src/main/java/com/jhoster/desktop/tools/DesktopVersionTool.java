// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\DesktopVersionTool.java
// # 📌 Amac: Desktop uygulama surumunu resource property dosyasindan okur
// # 📌 Modul - Java
// # Version: 3.61.1
// # Aciklama: Launcher ve updater akisi icin mevcut JHoster surum bilgisini merkezi saglar
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public final class DesktopVersionTool {
    private static final String RESOURCE_NAME = "/jhoster-desktop.properties";
    private static final String KEY_APP_VERSION = "app.version";
    private static final String FALLBACK_VERSION = "0.0.0";

    public String currentVersion() {
        Properties properties = new Properties();
        try (InputStream stream = DesktopVersionTool.class.getResourceAsStream(RESOURCE_NAME)) {
            if (stream == null) {
                return FALLBACK_VERSION;
            }
            properties.load(stream);
            return normalize(properties.getProperty(KEY_APP_VERSION, FALLBACK_VERSION));
        } catch (IOException exception) {
            return FALLBACK_VERSION;
        }
    }

    private String normalize(String value) {
        String normalized = value == null ? "" : value.trim();
        return normalized.isBlank() ? FALLBACK_VERSION : normalized;
    }
}
