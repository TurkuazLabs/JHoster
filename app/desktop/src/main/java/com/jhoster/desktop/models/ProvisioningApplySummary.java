// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\ProvisioningApplySummary.java
// # 📌 Amac: Desktop provisioning plan/apply sonucunu sade UI modeline tasir
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: Plan hazirlik durumu, apply status, run id ve step sayisini View katmanina aktarir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class ProvisioningApplySummary {
    private static final String EMPTY_VALUE = "";
    private static final String NEW_LINE = "\n";
    private final String title;
    private final boolean success;
    private final String status;
    private final String projectCode;
    private final String runId;
    private final int stepCount;
    private final boolean readyForApply;
    private final String message;
    private final String rawLog;

    public ProvisioningApplySummary(String title, boolean success, String status, String projectCode, String runId, int stepCount, boolean readyForApply, String message, String rawLog) {
        this.title = normalize(title);
        this.success = success;
        this.status = normalize(status);
        this.projectCode = normalize(projectCode);
        this.runId = normalize(runId);
        this.stepCount = stepCount;
        this.readyForApply = readyForApply;
        this.message = normalize(message);
        this.rawLog = normalize(rawLog);
    }

    public static ProvisioningApplySummary empty(String title, String rawLog) {
        return new ProvisioningApplySummary(title, false, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, -1, false, EMPTY_VALUE, rawLog);
    }

    public String getTitle() { return title; }
    public boolean isSuccess() { return success; }
    public String getStatus() { return status; }
    public String getProjectCode() { return projectCode; }
    public String getRunId() { return runId; }
    public int getStepCount() { return stepCount; }
    public boolean isReadyForApply() { return readyForApply; }
    public String getMessage() { return message; }
    public boolean hasStatus() { return !status.isBlank(); }
    public boolean hasRunId() { return !runId.isBlank(); }
    public boolean hasStepCount() { return stepCount >= 0; }

    public String toLogBlock() {
        return title + NEW_LINE
            + "success: " + success + NEW_LINE
            + "status: " + status + NEW_LINE
            + "project: " + projectCode + NEW_LINE
            + "ready_for_apply: " + readyForApply + NEW_LINE
            + "run_id: " + runId + NEW_LINE
            + "step_count: " + stepCount + NEW_LINE
            + "message: " + message + NEW_LINE
            + rawLog;
    }

    private static String normalize(String value) {
        return value == null ? EMPTY_VALUE : value;
    }
}
