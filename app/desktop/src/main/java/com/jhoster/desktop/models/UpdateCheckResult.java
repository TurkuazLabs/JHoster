// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\UpdateCheckResult.java
// # 📌 Amac: GitHub Release surum kontrol sonucunu ve dogrulanabilir installer asset bilgisini tasir
// # 📌 Modul - Java
// # Version: 3.80.0
// # Aciklama: Latest release, setup EXE ve SHA-256 asset URL bilgilerini launcher otomatik update akisina saglar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.models;

public final class UpdateCheckResult {
    private final boolean checked;
    private final boolean updateAvailable;
    private final boolean skipped;
    private final String currentVersion;
    private final String latestVersion;
    private final String releaseUrl;
    private final String installerAssetName;
    private final String installerDownloadUrl;
    private final String checksumDownloadUrl;
    private final String message;

    private UpdateCheckResult(
        boolean checked,
        boolean updateAvailable,
        boolean skipped,
        String currentVersion,
        String latestVersion,
        String releaseUrl,
        String installerAssetName,
        String installerDownloadUrl,
        String checksumDownloadUrl,
        String message
    ) {
        this.checked = checked;
        this.updateAvailable = updateAvailable;
        this.skipped = skipped;
        this.currentVersion = normalize(currentVersion);
        this.latestVersion = normalize(latestVersion);
        this.releaseUrl = normalize(releaseUrl);
        this.installerAssetName = normalize(installerAssetName);
        this.installerDownloadUrl = normalize(installerDownloadUrl);
        this.checksumDownloadUrl = normalize(checksumDownloadUrl);
        this.message = normalize(message);
    }

    public static UpdateCheckResult skipped(String currentVersion, String message) {
        return new UpdateCheckResult(false, false, true, currentVersion, currentVersion, "", "", "", "", message);
    }

    public static UpdateCheckResult current(String currentVersion, String latestVersion, String releaseUrl) {
        return new UpdateCheckResult(
            true, false, false, currentVersion, latestVersion, releaseUrl, "", "", "",
            "JHoster is up to date."
        );
    }

    public static UpdateCheckResult available(
        String currentVersion,
        String latestVersion,
        String releaseUrl,
        String installerAssetName,
        String installerDownloadUrl,
        String checksumDownloadUrl
    ) {
        return new UpdateCheckResult(
            true,
            true,
            false,
            currentVersion,
            latestVersion,
            releaseUrl,
            installerAssetName,
            installerDownloadUrl,
            checksumDownloadUrl,
            "A newer JHoster release is available."
        );
    }

    public static UpdateCheckResult failed(String currentVersion, String message) {
        return new UpdateCheckResult(false, false, false, currentVersion, currentVersion, "", "", "", "", message);
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

    public boolean hasVerifiedInstallerAssets() {
        return !installerAssetName.isBlank()
            && !installerDownloadUrl.isBlank()
            && !checksumDownloadUrl.isBlank();
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

    public String getInstallerAssetName() {
        return installerAssetName;
    }

    public String getInstallerDownloadUrl() {
        return installerDownloadUrl;
    }

    public String getChecksumDownloadUrl() {
        return checksumDownloadUrl;
    }

    public String getMessage() {
        return message;
    }

    private static String normalize(String value) {
        return value == null ? "" : value.trim();
    }
}
