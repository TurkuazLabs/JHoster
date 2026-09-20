// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\UpdateCheckResult.java
// # 📌 Amac: GitHub Release surum kontrol sonucunu tasir
// # 📌 Modul - Java
// # Version: 3.61.0
// # Aciklama: Launcher splash akisi icin update durumu, son surum, release URL ve mesaj bilgisini modeller
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.models;

public final class UpdateCheckResult {
    private final boolean checked;
    private final boolean updateAvailable;
    private final boolean skipped;
    private final String currentVersion;
    private final String latestVersion;
    private final String releaseUrl;
    private final String message;

    private UpdateCheckResult(
        boolean checked,
        boolean updateAvailable,
        boolean skipped,
        String currentVersion,
        String latestVersion,
        String releaseUrl,
        String message
    ) {
        this.checked = checked;
        this.updateAvailable = updateAvailable;
        this.skipped = skipped;
        this.currentVersion = normalize(currentVersion);
        this.latestVersion = normalize(latestVersion);
        this.releaseUrl = normalize(releaseUrl);
        this.message = normalize(message);
    }

    public static UpdateCheckResult skipped(String currentVersion, String message) {
        return new UpdateCheckResult(false, false, true, currentVersion, currentVersion, "", message);
    }

    public static UpdateCheckResult unavailable(String currentVersion, String message) {
        return new UpdateCheckResult(true, false, false, currentVersion, currentVersion, "", message);
    }

    public static UpdateCheckResult current(String currentVersion, String latestVersion, String releaseUrl) {
        return new UpdateCheckResult(true, false, false, currentVersion, latestVersion, releaseUrl, "JHoster is up to date.");
    }

    public static UpdateCheckResult available(String currentVersion, String latestVersion, String releaseUrl) {
        return new UpdateCheckResult(true, true, false, currentVersion, latestVersion, releaseUrl, "A newer JHoster release is available.");
    }

    public static UpdateCheckResult failed(String currentVersion, String message) {
        return new UpdateCheckResult(false, false, false, currentVersion, currentVersion, "", message);
    }

    public boolean isChecked() {
        return checked;
    }

    public boolean isUpdateAvailable() {
        return updateAvailable;
    }

    public boolean isSkipped() {
        return skipped;
    }

    public String getCurrentVersion() {
        return currentVersion;
    }

    public String getLatestVersion() {
        return latestVersion;
    }

    public String getReleaseUrl() {
        return releaseUrl;
    }

    public String getMessage() {
        return message;
    }

    private static String normalize(String value) {
        return value == null ? "" : value.trim();
    }
}
