// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\WorkflowResultFormatterService.java
// # 📌 Amac: Agent workflow HTTP sonucunu Desktop icin okunabilir ozet haline getirir
// # 📌 Modul - Java
// # Version: 3.35.1
// # Aciklama: Profile, plan, dry-run, runs ve locks cevaplarini status/run/step/count summary modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.WorkflowDesktopSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class WorkflowResultFormatterService {
    private static final String TITLE_PROFILE = "Workflow active profile";
    private static final String TITLE_PLAN = "Workflow plan";
    private static final String TITLE_DRY_RUN = "Workflow dry-run";
    private static final String TITLE_RUNS = "Workflow runs";
    private static final String TITLE_LOCKS = "Workflow locks";

    private static final String KEY_SUCCESS = "success";
    private static final String KEY_STATUS = "status";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_RUN_ID = "run_id";
    private static final String KEY_WEB_SERVER = "web_server";
    private static final String KEY_SERVER_CODE = "server_code";
    private static final String KEY_PROJECT_CODE = "project_code";
    private static final String KEY_STEP_COUNT = "step_count";
    private static final String KEY_COUNT = "count";
    private static final String KEY_NAME = "name";

    private static final int VALUE_NOT_AVAILABLE = -1;

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public WorkflowResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public WorkflowDesktopSummary formatProfile(DesktopHttpResult result) {
        String body = result.getBody();
        String serverCode = jsonTextExtractorTool.extractString(body, KEY_SERVER_CODE);
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);

        return buildSummary(
            TITLE_PROFILE,
            result,
            status,
            "",
            serverCode,
            "",
            VALUE_NOT_AVAILABLE,
            VALUE_NOT_AVAILABLE,
            message
        );
    }

    public WorkflowDesktopSummary formatPlan(DesktopHttpResult result) {
        return formatWorkflow(TITLE_PLAN, result);
    }

    public WorkflowDesktopSummary formatDryRun(DesktopHttpResult result) {
        return formatWorkflow(TITLE_DRY_RUN, result);
    }

    public WorkflowDesktopSummary formatRuns(DesktopHttpResult result) {
        String body = result.getBody();
        String runId = jsonTextExtractorTool.extractString(body, KEY_RUN_ID);
        String projectCode = jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE);
        int count = jsonTextExtractorTool.extractInt(body, KEY_COUNT, VALUE_NOT_AVAILABLE);

        return buildSummary(
            TITLE_RUNS,
            result,
            "listed",
            runId,
            "",
            projectCode,
            VALUE_NOT_AVAILABLE,
            count,
            ""
        );
    }

    public WorkflowDesktopSummary formatLocks(DesktopHttpResult result) {
        String body = result.getBody();
        String runId = jsonTextExtractorTool.extractString(body, KEY_RUN_ID);
        String projectCode = jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE);
        String serverCode = jsonTextExtractorTool.extractString(body, KEY_SERVER_CODE);
        int count = jsonTextExtractorTool.extractInt(body, KEY_COUNT, VALUE_NOT_AVAILABLE);

        return buildSummary(
            TITLE_LOCKS,
            result,
            "listed",
            runId,
            serverCode,
            projectCode,
            VALUE_NOT_AVAILABLE,
            count,
            ""
        );
    }

    private WorkflowDesktopSummary formatWorkflow(String title, DesktopHttpResult result) {
        String body = result.getBody();
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String runId = jsonTextExtractorTool.extractString(body, KEY_RUN_ID);
        String webServer = jsonTextExtractorTool.extractString(body, KEY_WEB_SERVER);
        String projectCode = jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);
        int stepCount = jsonTextExtractorTool.extractInt(body, KEY_STEP_COUNT, countStepNames(body));

        return buildSummary(
            title,
            result,
            status,
            runId,
            webServer,
            projectCode,
            stepCount,
            VALUE_NOT_AVAILABLE,
            message
        );
    }

    private WorkflowDesktopSummary buildSummary(
        String title,
        DesktopHttpResult result,
        String status,
        String runId,
        String webServer,
        String projectCode,
        int stepCount,
        int recordCount,
        String message
    ) {
        if (result == null) {
            return WorkflowDesktopSummary.empty(title, "");
        }

        boolean apiSuccess = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(result.getBody(), KEY_SUCCESS, result.isSuccess());

        return new WorkflowDesktopSummary(
            title,
            apiSuccess,
            status,
            runId,
            webServer,
            projectCode,
            stepCount,
            recordCount,
            message,
            result.toLogBlock()
        );
    }

    private int countStepNames(String body) {
        int nameCount = jsonTextExtractorTool.countKeyOccurrences(body, KEY_NAME);
        return nameCount <= 0 ? VALUE_NOT_AVAILABLE : nameCount;
    }
}
