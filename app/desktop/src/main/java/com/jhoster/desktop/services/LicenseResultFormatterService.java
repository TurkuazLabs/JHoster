// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\LicenseResultFormatterService.java
// # 📌 Amac: Agent lisans HTTP sonucunu Desktop icin okunabilir ozet haline getirir
// # 📌 Modul - Java
// # Version: 3.65.0
// # Aciklama: License endpoint cevabini plan, kullanim ve Pro feature registry bilgisiyle LicensePlanSummary modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.LicensePlanSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class LicenseResultFormatterService {
    private static final String TITLE_LICENSE = "License Status";
    private static final String KEY_SUCCESS = "success";
    private static final String KEY_PLAN_KEY = "plan_key";
    private static final String KEY_PLAN_LABEL = "plan_label";
    private static final String KEY_ACTIVE_PROJECT_COUNT = "active_project_count";
    private static final String KEY_MAX_ACTIVE_PROJECTS = "max_active_projects";
    private static final String KEY_USAGE_LABEL = "usage_label";
    private static final String KEY_CAN_CREATE_PROJECT = "can_create_project";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_UPGRADE_HINT = "upgrade_hint";
    private static final String KEY_FEATURE_SITE_LIMIT = "site_limit";
    private static final String KEY_FEATURE_ADVANCED_SSL = "advanced_ssl";
    private static final String KEY_FEATURE_AUTOMATED_BACKUP = "automated_backup";
    private static final String KEY_FEATURE_ADVANCED_DNS = "advanced_dns";
    private static final String KEY_FEATURE_AI_OLLAMA = "ai_ollama";
    private static final int DEFAULT_ACTIVE_PROJECT_COUNT = 0;
    private static final int DEFAULT_MAX_ACTIVE_PROJECTS = 5;

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public LicenseResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public LicensePlanSummary format(DesktopHttpResult result) {
        if (result == null) {
            return LicensePlanSummary.empty();
        }

        String body = result.getBody();
        boolean success = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(body, KEY_SUCCESS, result.isSuccess());

        return new LicensePlanSummary(
            TITLE_LICENSE,
            success,
            jsonTextExtractorTool.extractString(body, KEY_PLAN_KEY),
            jsonTextExtractorTool.extractString(body, KEY_PLAN_LABEL),
            jsonTextExtractorTool.extractInt(body, KEY_ACTIVE_PROJECT_COUNT, DEFAULT_ACTIVE_PROJECT_COUNT),
            jsonTextExtractorTool.extractInt(body, KEY_MAX_ACTIVE_PROJECTS, DEFAULT_MAX_ACTIVE_PROJECTS),
            jsonTextExtractorTool.extractString(body, KEY_USAGE_LABEL),
            jsonTextExtractorTool.extractBoolean(body, KEY_CAN_CREATE_PROJECT, true),
            jsonTextExtractorTool.extractString(body, KEY_MESSAGE),
            jsonTextExtractorTool.extractString(body, KEY_UPGRADE_HINT),
            jsonTextExtractorTool.extractBoolean(body, KEY_FEATURE_SITE_LIMIT, true),
            jsonTextExtractorTool.extractBoolean(body, KEY_FEATURE_ADVANCED_SSL, false),
            jsonTextExtractorTool.extractBoolean(body, KEY_FEATURE_AUTOMATED_BACKUP, false),
            jsonTextExtractorTool.extractBoolean(body, KEY_FEATURE_ADVANCED_DNS, false),
            jsonTextExtractorTool.extractBoolean(body, KEY_FEATURE_AI_OLLAMA, false),
            result.toLogBlock()
        );
    }
}
