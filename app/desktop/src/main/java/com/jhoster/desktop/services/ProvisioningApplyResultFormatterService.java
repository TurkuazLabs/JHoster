// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\ProvisioningApplyResultFormatterService.java
// # 📌 Amac: Provisioning plan/apply HTTP cevaplarini Desktop modeline cevirir
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: Hazirlik, run id, step count ve hata durumlarini hafif JSON extractor ile formatlar
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.ProvisioningApplySummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class ProvisioningApplyResultFormatterService {
    private static final String TITLE_PLAN = "Provisioning apply plan";
    private static final String TITLE_APPLY = "Provisioning apply";
    private static final String KEY_SUCCESS = "success";
    private static final String KEY_STATUS = "status";
    private static final String KEY_PROJECT_CODE = "project_code";
    private static final String KEY_RUN_ID = "run_id";
    private static final String KEY_STEP_COUNT = "step_count";
    private static final String KEY_READY_FOR_APPLY = "ready_for_apply";
    private static final String KEY_ERROR = "error";
    private static final int VALUE_NOT_AVAILABLE = -1;
    private final JsonTextExtractorTool jsonTextExtractorTool = new JsonTextExtractorTool();

    public ProvisioningApplySummary formatPlan(String projectCode, DesktopHttpResult result) {
        if (result == null) return ProvisioningApplySummary.empty(TITLE_PLAN, "");
        String body = result.getBody();
        boolean apiSuccess = result.isSuccess() && jsonTextExtractorTool.extractBoolean(body, KEY_SUCCESS, result.isSuccess());
        boolean ready = jsonTextExtractorTool.extractBoolean(body, KEY_READY_FOR_APPLY, false);
        String status = fallback(jsonTextExtractorTool.extractString(body, KEY_STATUS), apiSuccess ? "planned" : "error");
        String error = jsonTextExtractorTool.extractString(body, KEY_ERROR);
        String message = !error.isBlank() ? error : ready ? "Provisioning plan ready for apply" : "Provisioning plan has blockers";
        return new ProvisioningApplySummary(
            TITLE_PLAN, apiSuccess, status,
            fallback(jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE), projectCode),
            "", VALUE_NOT_AVAILABLE, ready, message, result.toLogBlock()
        );
    }

    public ProvisioningApplySummary formatApply(String projectCode, DesktopHttpResult result) {
        if (result == null) return ProvisioningApplySummary.empty(TITLE_APPLY, "");
        String body = result.getBody();
        boolean apiSuccess = result.isSuccess() && jsonTextExtractorTool.extractBoolean(body, KEY_SUCCESS, result.isSuccess());
        String status = fallback(jsonTextExtractorTool.extractString(body, KEY_STATUS), apiSuccess ? "completed" : "error");
        String error = jsonTextExtractorTool.extractString(body, KEY_ERROR);
        String message = error.isBlank() ? (apiSuccess ? "Provisioning apply completed" : "Provisioning apply failed") : error;
        return new ProvisioningApplySummary(
            TITLE_APPLY, apiSuccess, status,
            fallback(jsonTextExtractorTool.extractString(body, KEY_PROJECT_CODE), projectCode),
            jsonTextExtractorTool.extractString(body, KEY_RUN_ID),
            jsonTextExtractorTool.extractInt(body, KEY_STEP_COUNT, VALUE_NOT_AVAILABLE),
            apiSuccess, message, result.toLogBlock()
        );
    }

    private String fallback(String value, String fallbackValue) {
        return value == null || value.isBlank() ? fallbackValue : value;
    }
}
