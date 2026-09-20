// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\repositories\DesktopServiceSelectionRepository.java
// # 📌 Amac: Desktop servis secim ayarlarini dosyadan okur ve dosyaya yazar
// # 📌 Modul - Java
// # Version: 3.55.1
// # Aciklama: data/jhoster/desktop_service_selection_settings.json dosyasini sade JSON metni olarak saklar
// # Bagimli Oldugu Katman: Repo

package com.jhoster.desktop.repositories;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopServiceSelectionSettings;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class DesktopServiceSelectionRepository {
    private static final String SETTINGS_RELATIVE_PATH = "data/jhoster/desktop_service_selection_settings.json";
    private static final String TRUE_TEXT = "true";
    private static final String FALSE_TEXT = "false";

    public DesktopServiceSelectionSettings load() {
        Path path = resolveSettingsPath();
        if (!Files.isRegularFile(path)) {
            DesktopServiceSelectionSettings settings = DesktopServiceSelectionSettings.defaults();
            save(settings);
            return settings;
        }

        try {
            String content = Files.readString(path, StandardCharsets.UTF_8);
            DesktopServiceSelectionSettings defaults = DesktopServiceSelectionSettings.defaults();
            return new DesktopServiceSelectionSettings(
                readString(content, "active_web_server", defaults.getActiveWebServer()),
                readBoolean(content, "apache_enabled", defaults.isApacheEnabled()),
                readBoolean(content, "nginx_enabled", defaults.isNginxEnabled()),
                readBoolean(content, "mysql_enabled", defaults.isMysqlEnabled()),
                readBoolean(content, "php_enabled", defaults.isPhpEnabled()),
                readBoolean(content, "mailpit_enabled", defaults.isMailpitEnabled())
            ).normalized();
        } catch (IOException exception) {
            return DesktopServiceSelectionSettings.defaults();
        }
    }

    public void save(DesktopServiceSelectionSettings settings) {
        DesktopServiceSelectionSettings safeSettings = settings == null ? DesktopServiceSelectionSettings.defaults() : settings.normalized();
        Path path = resolveSettingsPath();
        try {
            Files.createDirectories(path.getParent());
            Files.writeString(path, toJson(safeSettings), StandardCharsets.UTF_8);
        } catch (IOException exception) {
            // Desktop ayar dosyasi yazilamazsa uygulama calismaya devam eder.
        }
    }

    public Path resolveSettingsPath() {
        return resolveRootPath().resolve(SETTINGS_RELATIVE_PATH).normalize();
    }

    private Path resolveRootPath() {
        Path currentPath = Paths.get(System.getProperty("user.dir")).toAbsolutePath().normalize();
        if (isRootPath(currentPath)) {
            return currentPath;
        }

        Path parent = currentPath.getParent();
        if (parent != null && isRootPath(parent)) {
            return parent;
        }

        Path grandParent = parent == null ? null : parent.getParent();
        if (grandParent != null && isRootPath(grandParent)) {
            return grandParent;
        }

        if ("desktop".equalsIgnoreCase(currentPath.getFileName().toString()) && parent != null && "app".equalsIgnoreCase(parent.getFileName().toString()) && grandParent != null) {
            return grandParent;
        }

        return currentPath;
    }

    private boolean isRootPath(Path path) {
        return Files.isDirectory(path.resolve("app/desktop")) && Files.isDirectory(path.resolve("app/agent"));
    }

    private String readString(String content, String key, String fallback) {
        Pattern pattern = Pattern.compile("\\\"" + Pattern.quote(key) + "\\\"\\s*:\\s*\\\"([^\\\"]*)\\\"");
        Matcher matcher = pattern.matcher(content);
        if (matcher.find()) {
            return matcher.group(1);
        }
        return fallback;
    }

    private boolean readBoolean(String content, String key, boolean fallback) {
        Pattern pattern = Pattern.compile("\\\"" + Pattern.quote(key) + "\\\"\\s*:\\s*(true|false)");
        Matcher matcher = pattern.matcher(content);
        if (matcher.find()) {
            return TRUE_TEXT.equalsIgnoreCase(matcher.group(1));
        }
        return fallback;
    }

    private String toJson(DesktopServiceSelectionSettings settings) {
        StringBuilder builder = new StringBuilder();
        builder.append("{\n");
        builder.append("  \"active_web_server\": \"").append(settings.getActiveWebServer()).append("\",\n");
        builder.append("  \"shared_www\": \"").append(DesktopApiConfig.WEB_SERVER_SHARED_DOCUMENT_ROOT).append("\",\n");
        builder.append("  \"apache_enabled\": ").append(toJsonBoolean(settings.isApacheEnabled())).append(",\n");
        builder.append("  \"nginx_enabled\": ").append(toJsonBoolean(settings.isNginxEnabled())).append(",\n");
        builder.append("  \"mysql_enabled\": ").append(toJsonBoolean(settings.isMysqlEnabled())).append(",\n");
        builder.append("  \"php_enabled\": ").append(toJsonBoolean(settings.isPhpEnabled())).append(",\n");
        builder.append("  \"mailpit_enabled\": ").append(toJsonBoolean(settings.isMailpitEnabled())).append("\n");
        builder.append("}\n");
        return builder.toString();
    }

    private String toJsonBoolean(boolean value) {
        return value ? TRUE_TEXT : FALSE_TEXT;
    }
}
