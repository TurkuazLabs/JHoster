// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\WorkflowDesktopSummary.java
// # 📌 Amac: Desktop workflow API sonucunu okunabilir ozet modeline donusturur
// # 📌 Modul - Java
// # Version: 3.35.0
// # Aciklama: Active profile, workflow status, run id, step count ve record count degerlerini View katmanina tasir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

public final class WorkflowDesktopSummary {
    private static final String EMPTY_VALUE = "";
    private static final String LINE_SEPARATOR = "\n";
    private static final String TITLE_SEPARATOR = "------------------------------";
    private static final String FIELD_SUCCESS = "success=";
    private static final String FIELD_STATUS = "status=";
    private static final String FIELD_RUN_ID = "run_id=";
    private static final String FIELD_WEB_SERVER = "web_server=";
    private static final String FIELD_PROJECT_CODE = "project_code=";
    private static final String FIELD_STEP_COUNT = "step_count=";
    private static final String FIELD_RECORD_COUNT = "record_count=";
    private static final String FIELD_MESSAGE = "message=";
    private static final String FIELD_RAW = "raw=";
    private static final int VALUE_NOT_AVAILABLE = -1;

    private final String title;
    private final boolean success;
    private final String status;
    private final String runId;
    private final String webServer;
    private final String projectCode;
    private final int stepCount;
    private final int recordCount;
    private final String message;
    private final String rawLogBlock;

    public WorkflowDesktopSummary(
        String title,
        boolean success,
        String status,
        String runId,
        String webServer,
        String projectCode,
        int stepCount,
        int recordCount,
        String message,
        String rawLogBlock
    ) {
        this.title = normalize(title);
        this.success = success;
        this.status = normalize(status);
        this.runId = normalize(runId);
        this.webServer = normalize(webServer);
        this.projectCode = normalize(projectCode);
        this.stepCount = stepCount;
        this.recordCount = recordCount;
        this.message = normalize(message);
        this.rawLogBlock = normalize(rawLogBlock);
    }

    public static WorkflowDesktopSummary empty(String title, String rawLogBlock) {
        return new WorkflowDesktopSummary(
            title,
            false,
            EMPTY_VALUE,
            EMPTY_VALUE,
            EMPTY_VALUE,
            EMPTY_VALUE,
            VALUE_NOT_AVAILABLE,
            VALUE_NOT_AVAILABLE,
            EMPTY_VALUE,
            rawLogBlock
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

    public String getRunId() {
        return runId;
    }

    public String getWebServer() {
        return webServer;
    }

    public String getProjectCode() {
        return projectCode;
    }

    public int getStepCount() {
        return stepCount;
    }

    public int getRecordCount() {
        return recordCount;
    }

    public String getMessage() {
        return message;
    }

    public String getRawLogBlock() {
        return rawLogBlock;
    }

    public boolean hasStatus() {
        return !status.isBlank();
    }

    public boolean hasRunId() {
        return !runId.isBlank();
    }

    public boolean hasWebServer() {
        return !webServer.isBlank();
    }

    public boolean hasProjectCode() {
        return !projectCode.isBlank();
    }

    public boolean hasStepCount() {
        return stepCount >= 0;
    }

    public boolean hasRecordCount() {
        return recordCount >= 0;
    }

    public String toLogBlock() {
        StringBuilder builder = new StringBuilder();
        builder.append(title).append(LINE_SEPARATOR);
        builder.append(TITLE_SEPARATOR).append(LINE_SEPARATOR);
        builder.append(FIELD_SUCCESS).append(success).append(LINE_SEPARATOR);

        appendIfPresent(builder, FIELD_STATUS, status);
        appendIfPresent(builder, FIELD_RUN_ID, runId);
        appendIfPresent(builder, FIELD_WEB_SERVER, webServer);
        appendIfPresent(builder, FIELD_PROJECT_CODE, projectCode);
        appendIfAvailable(builder, FIELD_STEP_COUNT, stepCount);
        appendIfAvailable(builder, FIELD_RECORD_COUNT, recordCount);
        appendIfPresent(builder, FIELD_MESSAGE, message);

        if (!rawLogBlock.isBlank()) {
            builder.append(FIELD_RAW).append(LINE_SEPARATOR).append(rawLogBlock);
        }

        return builder.toString();
    }

    private static void appendIfPresent(StringBuilder builder, String fieldName, String value) {
        if (!value.isBlank()) {
            builder.append(fieldName).append(value).append(LINE_SEPARATOR);
        }
    }

    private static void appendIfAvailable(StringBuilder builder, String fieldName, int value) {
        if (value >= 0) {
            builder.append(fieldName).append(value).append(LINE_SEPARATOR);
        }
    }

    private static String normalize(String value) {
        return value == null ? EMPTY_VALUE : value.trim();
    }
}
