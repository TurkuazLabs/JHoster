// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\RuntimeManagerSummary.java
// # 📌 Amac: Desktop runtime manager ozet verisini tasir
// # 📌 Modul - Java
// # Version: 3.41.0
// # Aciklama: Runtime listeleme, aktif runtime ve aktivasyon sonuclarini UI icin sade modele cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.models;

public final class RuntimeManagerSummary {
    private static final String EMPTY_VALUE = "";
    private static final String VALUE_NOT_AVAILABLE = "-";
    private static final String NEW_LINE = "\n";

    private final String title;
    private final boolean success;
    private final String family;
    private final String status;
    private final String componentCode;
    private final String version;
    private final String message;
    private final int count;
    private final String rawLog;

    public RuntimeManagerSummary(
        String title,
        boolean success,
        String family,
        String status,
        String componentCode,
        String version,
        String message,
        int count,
        String rawLog
    ) {
        this.title = normalize(title);
        this.success = success;
        this.family = normalize(family);
        this.status = normalize(status);
        this.componentCode = normalize(componentCode);
        this.version = normalize(version);
        this.message = normalize(message);
        this.count = count;
        this.rawLog = normalize(rawLog);
    }

    public static RuntimeManagerSummary empty(String title, String rawLog) {
        return new RuntimeManagerSummary(title, false, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, -1, rawLog);
    }

    public String getTitle() {
        return title;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getFamily() {
        return family;
    }

    public String getStatus() {
        return status;
    }

    public String getComponentCode() {
        return componentCode;
    }

    public String getVersion() {
        return version;
    }

    public String getMessage() {
        return message;
    }

    public int getCount() {
        return count;
    }

    public boolean hasFamily() {
        return !family.isBlank();
    }

    public boolean hasComponentCode() {
        return !componentCode.isBlank();
    }

    public boolean hasVersion() {
        return !version.isBlank();
    }

    public boolean hasCount() {
        return count >= 0;
    }

    public String toDisplayValue() {
        if (hasComponentCode() && hasVersion()) {
            return componentCode + " / " + version;
        }

        if (hasComponentCode()) {
            return componentCode;
        }

        return VALUE_NOT_AVAILABLE;
    }

    public String toLogBlock() {
        return title + NEW_LINE
            + "success: " + success + NEW_LINE
            + "family: " + family + NEW_LINE
            + "status: " + status + NEW_LINE
            + "component: " + componentCode + NEW_LINE
            + "version: " + version + NEW_LINE
            + "count: " + count + NEW_LINE
            + "message: " + message + NEW_LINE
            + rawLog;
    }

    private static String normalize(String value) {
        return value == null ? EMPTY_VALUE : value;
    }
}
