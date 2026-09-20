// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\RuntimeResultFormatterService.java
// # 📌 Amac: Agent runtime HTTP sonucunu Desktop runtime manager icin okunabilir ozet haline getirir
// # 📌 Modul - Java
// # Version: 3.48.1
// # Aciklama: Runtime listeleme, aktif runtime, aktivasyon ve portable bin scan cevaplarini summary modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class RuntimeResultFormatterService {
    private static final String TITLE_LIST = "Runtime list";
    private static final String TITLE_ACTIVE = "Runtime active";
    private static final String TITLE_ACTIVATE = "Runtime activate";
    private static final String TITLE_PORTABLE_SCAN = "Portable bin scan";
    private static final String TITLE_PORTABLE_ACTIVATE = "Portable bin activate";

    private static final String KEY_SUCCESS = "success";
    private static final String KEY_FAMILY = "family";
    private static final String KEY_STATUS = "status";
    private static final String KEY_COMPONENT_CODE = "component_code";
    private static final String KEY_VERSION = "version";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_FOLDER_NAME = "folder_name";
    private static final String KEY_COUNT = "count";

    private static final int VALUE_NOT_AVAILABLE = -1;

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public RuntimeResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public RuntimeManagerSummary formatList(DesktopHttpResult result) {
        if (result == null) {
            return RuntimeManagerSummary.empty(TITLE_LIST, "");
        }

        int count = jsonTextExtractorTool.extractInt(result.getBody(), KEY_COUNT, VALUE_NOT_AVAILABLE);
        return buildSummary(TITLE_LIST, result, "", "listed", "", "", "", count);
    }

    public RuntimeManagerSummary formatActive(String family, DesktopHttpResult result) {
        if (result == null) {
            return RuntimeManagerSummary.empty(TITLE_ACTIVE, "");
        }

        String body = result.getBody();
        String responseFamily = jsonTextExtractorTool.extractString(body, KEY_FAMILY);
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String componentCode = jsonTextExtractorTool.extractString(body, KEY_COMPONENT_CODE);
        String version = jsonTextExtractorTool.extractString(body, KEY_VERSION);

        return buildSummary(TITLE_ACTIVE, result, fallback(responseFamily, family), status, componentCode, version, "", VALUE_NOT_AVAILABLE);
    }

    public RuntimeManagerSummary formatActivate(String componentCode, DesktopHttpResult result) {
        if (result == null) {
            return RuntimeManagerSummary.empty(TITLE_ACTIVATE, "");
        }

        String body = result.getBody();
        String family = jsonTextExtractorTool.extractString(body, KEY_FAMILY);
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String responseComponentCode = jsonTextExtractorTool.extractString(body, KEY_COMPONENT_CODE);
        String version = jsonTextExtractorTool.extractString(body, KEY_VERSION);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);

        return buildSummary(TITLE_ACTIVATE, result, family, status, fallback(responseComponentCode, componentCode), version, message, VALUE_NOT_AVAILABLE);
    }


    public RuntimeManagerSummary formatPortableScan(DesktopHttpResult result) {
        if (result == null) {
            return RuntimeManagerSummary.empty(TITLE_PORTABLE_SCAN, "");
        }

        int count = jsonTextExtractorTool.extractInt(result.getBody(), KEY_COUNT, VALUE_NOT_AVAILABLE);
        String message = jsonTextExtractorTool.extractString(result.getBody(), KEY_MESSAGE);
        return buildSummary(TITLE_PORTABLE_SCAN, result, "", "scanned", "", "", message, count);
    }

    public RuntimeManagerSummary formatPortableActivate(String family, String folderName, DesktopHttpResult result) {
        if (result == null) {
            return RuntimeManagerSummary.empty(TITLE_PORTABLE_ACTIVATE, "");
        }

        String body = result.getBody();
        String responseFamily = jsonTextExtractorTool.extractString(body, KEY_FAMILY);
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String componentCode = jsonTextExtractorTool.extractString(body, KEY_COMPONENT_CODE);
        String version = jsonTextExtractorTool.extractString(body, KEY_VERSION);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);
        String responseFolderName = jsonTextExtractorTool.extractString(body, KEY_FOLDER_NAME);

        return buildSummary(
            TITLE_PORTABLE_ACTIVATE,
            result,
            fallback(responseFamily, family),
            status,
            fallback(componentCode, responseFolderName.isBlank() ? folderName : responseFolderName),
            version,
            message,
            VALUE_NOT_AVAILABLE
        );
    }

    private RuntimeManagerSummary buildSummary(
        String title,
        DesktopHttpResult result,
        String family,
        String status,
        String componentCode,
        String version,
        String message,
        int count
    ) {
        boolean apiSuccess = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(result.getBody(), KEY_SUCCESS, result.isSuccess());

        return new RuntimeManagerSummary(
            title,
            apiSuccess,
            family,
            status,
            componentCode,
            version,
            message,
            count,
            result.toLogBlock()
        );
    }

    private String fallback(String value, String fallbackValue) {
        return value == null || value.isBlank() ? fallbackValue : value;
    }
}
