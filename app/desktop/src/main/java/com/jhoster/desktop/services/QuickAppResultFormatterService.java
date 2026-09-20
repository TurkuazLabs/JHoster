// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\QuickAppResultFormatterService.java
// # 📌 Amac: Agent Quick App ve stack secimi HTTP sonucunu Desktop icin okunabilir ozet haline getirir
// # 📌 Modul - Java
// # Version: 3.77.0
// # Aciklama: Template listeleme, stack secimli Quick App planlama ve create cevaplarini summary modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.QuickAppSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class QuickAppResultFormatterService {
    private static final String TITLE_TEMPLATES = "Quick App templates";
    private static final String TITLE_PLAN = "Quick App plan";
    private static final String TITLE_CREATE = "Quick App create";

    private static final String KEY_SUCCESS = "success";
    private static final String KEY_STATUS = "status";
    private static final String KEY_PROJECT_CODE = "project_code";
    private static final String KEY_TEMPLATE_CODE = "template_code";
    private static final String KEY_RUNTIME_FAMILY = "runtime_family";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_ERROR = "error";
    private static final String KEY_COUNT = "count";
    private static final String KEY_FILE_COUNT = "file_count";
    private static final String KEY_STACK_LABEL = "stack_label";
    private static final String KEY_PROVISIONING_STATUS = "provisioning_status";
    private static final String KEY_DATABASE_LABEL = "database_label";

    private static final int VALUE_NOT_AVAILABLE = -1;

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public QuickAppResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public QuickAppSummary formatTemplates(DesktopHttpResult result) {
        if (result == null) {
            return QuickAppSummary.empty(TITLE_TEMPLATES, "");
        }

        int count = jsonTextExtractorTool.extractInt(result.getBody(), KEY_COUNT, VALUE_NOT_AVAILABLE);
        return buildSummary(TITLE_TEMPLATES, result, "listed", "", "", "", "", count, VALUE_NOT_AVAILABLE, "", "", "");
    }

    public QuickAppSummary formatPlan(String projectCode, String templateCode, DesktopHttpResult result) {
        if (result == null) {
            return QuickAppSummary.empty(TITLE_PLAN, "");
        }

        String body = result.getBody();
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String responseProjectCode = jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE);
        String responseTemplateCode = jsonTextExtractorTool.extractString(body, KEY_TEMPLATE_CODE);
        String runtimeFamily = jsonTextExtractorTool.extractString(body, KEY_RUNTIME_FAMILY);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);
        String error = jsonTextExtractorTool.extractString(body, KEY_ERROR);
        int fileCount = jsonTextExtractorTool.extractInt(body, KEY_FILE_COUNT, VALUE_NOT_AVAILABLE);
        String stackLabel = jsonTextExtractorTool.extractString(body, KEY_STACK_LABEL);
        String provisioningStatus = jsonTextExtractorTool.extractString(body, KEY_PROVISIONING_STATUS);
        String databaseLabel = jsonTextExtractorTool.extractString(body, KEY_DATABASE_LABEL);

        return buildSummary(
            TITLE_PLAN,
            result,
            resolveStatus(result, status, "planned"),
            fallback(responseProjectCode, projectCode),
            fallback(responseTemplateCode, templateCode),
            runtimeFamily,
            fallback(message, error),
            VALUE_NOT_AVAILABLE,
            fileCount,
            stackLabel,
            provisioningStatus,
            databaseLabel
        );
    }

    public QuickAppSummary formatCreate(String projectCode, String templateCode, DesktopHttpResult result) {
        if (result == null) {
            return QuickAppSummary.empty(TITLE_CREATE, "");
        }

        String body = result.getBody();
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String responseProjectCode = jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE);
        String responseTemplateCode = jsonTextExtractorTool.extractString(body, KEY_TEMPLATE_CODE);
        String runtimeFamily = jsonTextExtractorTool.extractString(body, KEY_RUNTIME_FAMILY);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);
        String error = jsonTextExtractorTool.extractString(body, KEY_ERROR);
        int fileCount = jsonTextExtractorTool.extractInt(body, KEY_FILE_COUNT, VALUE_NOT_AVAILABLE);
        String stackLabel = jsonTextExtractorTool.extractString(body, KEY_STACK_LABEL);
        String provisioningStatus = jsonTextExtractorTool.extractString(body, KEY_PROVISIONING_STATUS);
        String databaseLabel = jsonTextExtractorTool.extractString(body, KEY_DATABASE_LABEL);

        return buildSummary(
            TITLE_CREATE,
            result,
            resolveStatus(result, status, "created"),
            fallback(responseProjectCode, projectCode),
            fallback(responseTemplateCode, templateCode),
            runtimeFamily,
            fallback(message, error),
            VALUE_NOT_AVAILABLE,
            fileCount,
            stackLabel,
            provisioningStatus,
            databaseLabel
        );
    }

    private QuickAppSummary buildSummary(
        String title,
        DesktopHttpResult result,
        String status,
        String projectCode,
        String templateCode,
        String runtimeFamily,
        String message,
        int count,
        int fileCount,
        String stackLabel,
        String provisioningStatus,
        String databaseLabel
    ) {
        boolean apiSuccess = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(result.getBody(), KEY_SUCCESS, result.isSuccess());

        return new QuickAppSummary(
            title,
            apiSuccess,
            status,
            projectCode,
            templateCode,
            runtimeFamily,
            message,
            count,
            fileCount,
            stackLabel,
            provisioningStatus,
            databaseLabel,
            result.toLogBlock()
        );
    }

    private String resolveStatus(DesktopHttpResult result, String status, String successFallback) {
        if (result != null && !result.isSuccess()) {
            return fallback(status, "error");
        }

        boolean apiSuccess = result != null
            && jsonTextExtractorTool.extractBoolean(result.getBody(), KEY_SUCCESS, result.isSuccess());

        if (!apiSuccess) {
            return fallback(status, "error");
        }

        return fallback(status, successFallback);
    }

    private String fallback(String value, String fallbackValue) {
        return value == null || value.isBlank() ? fallbackValue : value;
    }
}
