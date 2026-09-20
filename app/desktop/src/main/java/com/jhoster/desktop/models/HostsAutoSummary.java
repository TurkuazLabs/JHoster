// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\HostsAutoSummary.java
// # 📌 Amac: Desktop hosts auto inspect ve repair ozetini tasir
// # 📌 Modul - Java
// # Version: 3.68.0
// # Aciklama: JHoster managed hosts blok sagligini UI ve log katmanina aktarir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.models;

public final class HostsAutoSummary {
    private static final String DEFAULT_TITLE = "Hosts Auto";
    private static final String DEFAULT_STATUS = "offline";
    private static final String DEFAULT_MESSAGE = "Hosts auto endpoint not ready";
    private static final String DEFAULT_TARGET_FILE = "-";
    private static final String DEFAULT_APPLY_MODE = "-";
    private static final String LABEL_HEALTHY = "Healthy";
    private static final String LABEL_REPAIR_NEEDED = "Repair Needed";
    private static final String LABEL_REJECTED = "Admin Needed";
    private static final String LABEL_OFFLINE = "Offline";
    private static final String LINE_SEPARATOR = System.lineSeparator();

    private final String title;
    private final boolean success;
    private final String status;
    private final String message;
    private final int expectedCount;
    private final int managedCount;
    private final int missingCount;
    private final int staleCount;
    private final int wrongIpCount;
    private final int duplicateCount;
    private final int externalConflictCount;
    private final boolean repairRequired;
    private final boolean safeToRepair;
    private final String applyMode;
    private final String targetFile;
    private final String rawLog;

    public HostsAutoSummary(
        String title,
        boolean success,
        String status,
        String message,
        int expectedCount,
        int managedCount,
        int missingCount,
        int staleCount,
        int wrongIpCount,
        int duplicateCount,
        int externalConflictCount,
        boolean repairRequired,
        boolean safeToRepair,
        String applyMode,
        String targetFile,
        String rawLog
    ) {
        this.title = fallback(title, DEFAULT_TITLE);
        this.success = success;
        this.status = fallback(status, DEFAULT_STATUS);
        this.message = fallback(message, DEFAULT_MESSAGE);
        this.expectedCount = Math.max(0, expectedCount);
        this.managedCount = Math.max(0, managedCount);
        this.missingCount = Math.max(0, missingCount);
        this.staleCount = Math.max(0, staleCount);
        this.wrongIpCount = Math.max(0, wrongIpCount);
        this.duplicateCount = Math.max(0, duplicateCount);
        this.externalConflictCount = Math.max(0, externalConflictCount);
        this.repairRequired = repairRequired;
        this.safeToRepair = safeToRepair;
        this.applyMode = fallback(applyMode, DEFAULT_APPLY_MODE);
        this.targetFile = fallback(targetFile, DEFAULT_TARGET_FILE);
        this.rawLog = fallback(rawLog, "");
    }

    public static HostsAutoSummary empty() {
        return new HostsAutoSummary(
            DEFAULT_TITLE,
            false,
            DEFAULT_STATUS,
            DEFAULT_MESSAGE,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            false,
            false,
            DEFAULT_APPLY_MODE,
            DEFAULT_TARGET_FILE,
            ""
        );
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

    public String getMessage() {
        return message;
    }

    public int getExpectedCount() {
        return expectedCount;
    }

    public int getManagedCount() {
        return managedCount;
    }

    public int getMissingCount() {
        return missingCount;
    }

    public int getStaleCount() {
        return staleCount;
    }

    public int getWrongIpCount() {
        return wrongIpCount;
    }

    public int getDuplicateCount() {
        return duplicateCount;
    }

    public int getExternalConflictCount() {
        return externalConflictCount;
    }

    public boolean isRepairRequired() {
        return repairRequired;
    }

    public boolean isSafeToRepair() {
        return safeToRepair;
    }

    public String getApplyMode() {
        return applyMode;
    }

    public String getTargetFile() {
        return targetFile;
    }

    public String getHealthLabel() {
        if (!success) {
            if ("rejected".equals(status)) {
                return LABEL_REJECTED;
            }
            return LABEL_OFFLINE;
        }

        if (repairRequired || missingCount > 0 || staleCount > 0 || wrongIpCount > 0 || duplicateCount > 0) {
            return LABEL_REPAIR_NEEDED;
        }

        return LABEL_HEALTHY;
    }

    public String getCountLabel() {
        return managedCount + " / " + expectedCount;
    }

    public String getIssueLabel() {
        int issueCount = missingCount + staleCount + wrongIpCount + duplicateCount + externalConflictCount;
        return String.valueOf(issueCount);
    }

    public String toLogBlock() {
        return title + LINE_SEPARATOR
            + "status=" + status + LINE_SEPARATOR
            + "success=" + success + LINE_SEPARATOR
            + "health=" + getHealthLabel() + LINE_SEPARATOR
            + "expected=" + expectedCount + LINE_SEPARATOR
            + "managed=" + managedCount + LINE_SEPARATOR
            + "missing=" + missingCount + LINE_SEPARATOR
            + "stale=" + staleCount + LINE_SEPARATOR
            + "wrongIp=" + wrongIpCount + LINE_SEPARATOR
            + "duplicate=" + duplicateCount + LINE_SEPARATOR
            + "externalConflict=" + externalConflictCount + LINE_SEPARATOR
            + "repairRequired=" + repairRequired + LINE_SEPARATOR
            + "safeToRepair=" + safeToRepair + LINE_SEPARATOR
            + "applyMode=" + applyMode + LINE_SEPARATOR
            + "targetFile=" + targetFile + LINE_SEPARATOR
            + "message=" + message + LINE_SEPARATOR
            + rawLog;
    }

    private static String fallback(String value, String fallbackValue) {
        return value == null || value.isBlank() ? fallbackValue : value;
    }
}
