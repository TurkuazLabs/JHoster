// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\tools\DesktopMetadataTool.java
// # 📌 Amac: JHoster Desktop urun, TurkuazLabs marka ve update metadata degerlerini resource dosyasindan okur
// # 📌 Modul - Java
// # Version: 3.80.0
// # Aciklama: Publisher, website, support email, GitHub repo ve otomatik update ayarlarini merkezi saglar
// # Bagimli Oldugu Katman: Tool

package com.jhoster.desktop.tools;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public final class DesktopMetadataTool {
    private static final String RESOURCE_NAME = "/jhoster-desktop.properties";
    private static final String DEFAULT_PUBLISHER = "TurkuazLabs";
    private static final String DEFAULT_WEBSITE = "https://turkuazlabs.com";
    private static final String DEFAULT_SUPPORT_EMAIL = "support@turkuazlabs.com";
    private static final String DEFAULT_SUPPORT_URL = "https://turkuazlabs.com";
    private static final String DEFAULT_GITHUB = "https://github.com/TurkuazLabs";
    private static final String DEFAULT_UPDATE_REPO = "TurkuazLabs/JHoster";

    private final Properties properties;

    public DesktopMetadataTool() {
        this.properties = load();
    }

    public String publisher() {
        return value("brand.publisher", DEFAULT_PUBLISHER);
    }

    public String websiteUrl() {
        return value("brand.website", DEFAULT_WEBSITE);
    }

    public String supportEmail() {
        return value("brand.supportEmail", DEFAULT_SUPPORT_EMAIL);
    }

    public String supportUrl() {
        return value("brand.supportUrl", DEFAULT_SUPPORT_URL);
    }

    public String githubUrl() {
        return value("brand.github", DEFAULT_GITHUB);
    }

    public String updateRepository() {
        return value("app.update.repo", DEFAULT_UPDATE_REPO);
    }

    public boolean updateEnabled() {
        return Boolean.parseBoolean(value("app.update.enabled", "true"));
    }

    public boolean autoInstallEnabled() {
        return Boolean.parseBoolean(value("app.update.autoInstall", "true"));
    }

    public String installerAssetPrefix() {
        return value("app.update.assetPrefix", "JHoster-Setup-");
    }

    private String value(String key, String fallback) {
        String current = properties.getProperty(key, fallback);
        return current == null || current.isBlank() ? fallback : current.trim();
    }

    private Properties load() {
        Properties loaded = new Properties();
        try (InputStream stream = DesktopMetadataTool.class.getResourceAsStream(RESOURCE_NAME)) {
            if (stream != null) {
                loaded.load(stream);
            }
        } catch (IOException ignored) {
            // Defaults keep launcher usable when metadata cannot be loaded.
        }
        return loaded;
    }
}
