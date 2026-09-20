// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\ServiceResultFormatterService.java
// # 📌 Amac: Agent process HTTP sonucunu Desktop service manager icin okunabilir ozet haline getirir
// # 📌 Modul - Java
// # Version: 3.53.2
// # Aciklama: Process list/status/start/stop ve port guard cevaplarini servis status summary modeline cevirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.tools.JsonTextExtractorTool;

public final class ServiceResultFormatterService {
    private static final String TITLE_LIST = "Service list";
    private static final String TITLE_STATUS = "Service status";
    private static final String TITLE_PREFLIGHT = "Service preflight";
    private static final String TITLE_REAL_PROFILE = "Service real profile";
    private static final String TITLE_START = "Service start";
    private static final String TITLE_STOP = "Service stop";
    private static final String TITLE_RESTART = "Service restart";

    private static final String KEY_SUCCESS = "success";
    private static final String KEY_STATUS = "status";
    private static final String KEY_OPERATION = "operation";
    private static final String KEY_MESSAGE = "message";
    private static final String KEY_COUNT = "count";

    private static final int VALUE_NOT_AVAILABLE = -1;

    private final JsonTextExtractorTool jsonTextExtractorTool;

    public ServiceResultFormatterService() {
        this.jsonTextExtractorTool = new JsonTextExtractorTool();
    }

    public ServiceManagerSummary formatList(DesktopHttpResult result) {
        if (result == null) {
            return ServiceManagerSummary.empty(TITLE_LIST, "");
        }

        int count = jsonTextExtractorTool.extractInt(result.getBody(), KEY_COUNT, VALUE_NOT_AVAILABLE);
        return buildSummary(TITLE_LIST, result, "", "list", "listed", "", count);
    }

    public ServiceManagerSummary formatStatus(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_STATUS, serviceCode, result);
    }

    public ServiceManagerSummary formatPreflight(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_PREFLIGHT, serviceCode, result);
    }

    public ServiceManagerSummary formatRealProfile(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_REAL_PROFILE, serviceCode, result);
    }

    public ServiceManagerSummary formatStart(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_START, serviceCode, result);
    }

    public ServiceManagerSummary formatStop(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_STOP, serviceCode, result);
    }


    public ServiceManagerSummary formatRestart(String serviceCode, DesktopHttpResult result) {
        return formatSingle(TITLE_RESTART, serviceCode, result);
    }

    public ServiceManagerSummary formatRestart(String serviceCode, DesktopHttpResult stopResult, DesktopHttpResult startResult) {
        if (startResult == null) {
            return ServiceManagerSummary.empty(TITLE_RESTART, "");
        }

        String body = startResult.getBody();
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);
        boolean apiSuccess = startResult.isSuccess()
            && jsonTextExtractorTool.extractBoolean(body, KEY_SUCCESS, startResult.isSuccess());

        String rawLog = "stop_result:\n"
            + (stopResult == null ? "" : stopResult.toLogBlock())
            + "\nstart_result:\n"
            + startResult.toLogBlock();

        return new ServiceManagerSummary(
            TITLE_RESTART,
            apiSuccess,
            serviceCode,
            "restart",
            status,
            message,
            VALUE_NOT_AVAILABLE,
            rawLog
        );
    }

    private ServiceManagerSummary formatSingle(String title, String serviceCode, DesktopHttpResult result) {
        if (result == null) {
            return ServiceManagerSummary.empty(title, "");
        }

        String body = result.getBody();
        String operation = jsonTextExtractorTool.extractString(body, KEY_OPERATION);
        String status = jsonTextExtractorTool.extractString(body, KEY_STATUS);
        String message = jsonTextExtractorTool.extractString(body, KEY_MESSAGE);

        return buildSummary(title, result, serviceCode, operation, status, message, VALUE_NOT_AVAILABLE);
    }

    private ServiceManagerSummary buildSummary(
        String title,
        DesktopHttpResult result,
        String serviceCode,
        String operation,
        String status,
        String message,
        int count
    ) {
        boolean apiSuccess = result.isSuccess()
            && jsonTextExtractorTool.extractBoolean(result.getBody(), KEY_SUCCESS, result.isSuccess());

        return new ServiceManagerSummary(
            title,
            apiSuccess,
            serviceCode,
            operation,
            status,
            message,
            count,
            result.toLogBlock()
        );
    }
}
