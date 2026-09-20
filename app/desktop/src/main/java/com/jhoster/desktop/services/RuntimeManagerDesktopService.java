// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\RuntimeManagerDesktopService.java
// # 📌 Amac: JavaFX runtime manager is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.49.1
// # Aciklama: Portable servis ve runtime listeleme, aktif sorgulama, aktivasyon ve portable bin summary aksiyonlarini agent API uzerinden cagirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class RuntimeManagerDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String ACTIVE_ACTION = "/active";
    private static final String ACTIVATE_ACTION = "/activate";
    private static final String PORTABLE_SCAN_ACTION = "/portable-scan";
    private static final String PORTABLE_SUMMARY_ACTION = "/portable-summary";
    private static final String ACTIVATE_PORTABLE_ACTION = "/activate-portable";
    private static final String QUERY_PREFIX = "?";
    private static final String QUERY_DRY_RUN = "dry_run=";
    private static final String QUERY_FOLDER_NAME = "folder_name=";
    private static final String QUERY_AND = "&";

    private final HttpRequestTool httpRequestTool;
    private final RuntimeResultFormatterService runtimeResultFormatterService;

    public RuntimeManagerDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.runtimeResultFormatterService = new RuntimeResultFormatterService();
    }

    public RuntimeManagerSummary listRuntimeSummary() {
        return runtimeResultFormatterService.formatList(listRuntimes());
    }

    public RuntimeManagerSummary activeSummary(String family) {
        return runtimeResultFormatterService.formatActive(family, getActiveRuntime(family));
    }

    public RuntimeManagerSummary activateSummary(String componentCode) {
        return runtimeResultFormatterService.formatActivate(componentCode, activateRuntime(componentCode));
    }

    public RuntimeManagerSummary portableScanSummary() {
        return runtimeResultFormatterService.formatPortableScan(scanPortableRuntimes());
    }

    public RuntimeManagerSummary portableSummary() {
        return runtimeResultFormatterService.formatPortableScan(getPortableSummary());
    }

    public RuntimeManagerSummary activatePortableSummary(String family, String folderName) {
        return runtimeResultFormatterService.formatPortableActivate(family, folderName, activatePortableRuntime(family, folderName));
    }

    public DesktopHttpResult listRuntimes() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE));
    }

    public DesktopHttpResult getActiveRuntime(String family) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildActiveRoute(family)));
    }

    public DesktopHttpResult activateRuntime(String componentCode) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildActivateRoute(componentCode)) + buildActivateQuery());
    }

    public DesktopHttpResult scanPortableRuntimes() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE + PORTABLE_SCAN_ACTION));
    }

    public DesktopHttpResult getPortableSummary() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE + PORTABLE_SUMMARY_ACTION));
    }

    public DesktopHttpResult activatePortableRuntime(String family, String folderName) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildActivatePortableRoute(family)) + buildActivatePortableQuery(folderName));
    }

    private String buildActiveRoute(String family) {
        return DesktopApiConfig.RUNTIME_VERSIONS_ROUTE
            + PATH_SEPARATOR
            + encode(family)
            + ACTIVE_ACTION;
    }

    private String buildActivateRoute(String componentCode) {
        return DesktopApiConfig.RUNTIME_VERSIONS_ROUTE
            + PATH_SEPARATOR
            + encode(componentCode)
            + ACTIVATE_ACTION;
    }

    private String buildActivatePortableRoute(String family) {
        return DesktopApiConfig.RUNTIME_VERSIONS_ROUTE
            + PATH_SEPARATOR
            + encode(family)
            + ACTIVATE_PORTABLE_ACTION;
    }

    private String buildActivateQuery() {
        return QUERY_PREFIX + QUERY_DRY_RUN + DesktopApiConfig.RUNTIME_MANAGER_ACTIVATE_DRY_RUN;
    }

    private String buildActivatePortableQuery(String folderName) {
        return QUERY_PREFIX
            + QUERY_FOLDER_NAME
            + encode(folderName)
            + QUERY_AND
            + QUERY_DRY_RUN
            + DesktopApiConfig.RUNTIME_MANAGER_ACTIVATE_DRY_RUN;
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value.trim(), StandardCharsets.UTF_8);
    }
}
