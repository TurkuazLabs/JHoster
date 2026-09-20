// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\QuickAppSummary.java
// # 📌 Amac: Desktop Quick App ve stack secimi ozet verisini tasir
// # 📌 Modul - Java
// # Version: 3.77.0
// # Aciklama: Quick App template listeleme, stack secimli planlama ve create cevaplarini UI icin sade modele cevirir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class QuickAppSummary {
    private static final String EMPTY_VALUE = "";
    private static final String VALUE_NOT_AVAILABLE = "-";
    private static final String NEW_LINE = "\n";

    private final String title;
    private final boolean success;
    private final String status;
    private final String projectCode;
    private final String templateCode;
    private final String runtimeFamily;
    private final String message;
    private final int count;
    private final int fileCount;
    private final String stackLabel;
    private final String provisioningStatus;
    private final String databaseLabel;
    private final String rawLog;

    public QuickAppSummary(
        String title,
        boolean success,
        String status,
        String projectCode,
        String templateCode,
        String runtimeFamily,
        String message,
        int count,
        int fileCount,
        String stackLabel,
        String provisioningStatus,
        String databaseLabel,
        String rawLog
    ) {
        this.title = normalize(title);
        this.success = success;
        this.status = normalize(status);
        this.projectCode = normalize(projectCode);
        this.templateCode = normalize(templateCode);
        this.runtimeFamily = normalize(runtimeFamily);
        this.message = normalize(message);
        this.count = count;
        this.fileCount = fileCount;
        this.stackLabel = normalize(stackLabel);
        this.provisioningStatus = normalize(provisioningStatus);
        this.databaseLabel = normalize(databaseLabel);
        this.rawLog = normalize(rawLog);
    }

    public static QuickAppSummary empty(String title, String rawLog) {
        return new QuickAppSummary(title, false, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, -1, -1, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, rawLog);
    }

    public String getTitle() {
        return title;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getStatus() {
        return status;
    }

    public String getProjectCode() {
        return projectCode;
    }

    public String getTemplateCode() {
        return templateCode;
    }

    public String getRuntimeFamily() {
        return runtimeFamily;
    }

    public String getMessage() {
        return message;
    }

    public int getCount() {
        return count;
    }

    public int getFileCount() {
        return fileCount;
    }

    public String getStackLabel() {
        return stackLabel;
    }

    public String getProvisioningStatus() {
        return provisioningStatus;
    }

    public String getDatabaseLabel() {
        return databaseLabel;
    }

    public boolean hasStatus() {
        return !status.isBlank();
    }

    public boolean hasProjectCode() {
        return !projectCode.isBlank();
    }

    public boolean hasTemplateCode() {
        return !templateCode.isBlank();
    }

    public boolean hasRuntimeFamily() {
        return !runtimeFamily.isBlank();
    }

    public boolean hasCount() {
        return count >= 0;
    }

    public boolean hasFileCount() {
        return fileCount >= 0;
    }

    public boolean hasStackLabel() {
        return !stackLabel.isBlank();
    }

    public boolean hasProvisioningStatus() {
        return !provisioningStatus.isBlank();
    }

    public boolean hasDatabaseLabel() {
        return !databaseLabel.isBlank();
    }

    public String toDisplayValue() {
        if (hasProjectCode() && hasTemplateCode()) {
            return projectCode + " / " + templateCode;
        }

        if (hasTemplateCode()) {
            return templateCode;
        }

        return VALUE_NOT_AVAILABLE;
    }

    public String toLogBlock() {
        return title + NEW_LINE
            + "success: " + success + NEW_LINE
            + "status: " + status + NEW_LINE
            + "project: " + projectCode + NEW_LINE
            + "template: " + templateCode + NEW_LINE
            + "runtime_family: " + runtimeFamily + NEW_LINE
            + "count: " + count + NEW_LINE
            + "file_count: " + fileCount + NEW_LINE
            + "stack: " + stackLabel + NEW_LINE
            + "provisioning: " + provisioningStatus + NEW_LINE
            + "database: " + databaseLabel + NEW_LINE
            + "message: " + message + NEW_LINE
            + rawLog;
    }

    private static String normalize(String value) {
        return value == null ? EMPTY_VALUE : value;
    }
}
