// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\ServiceManagerDesktopService.java
// # 📌 Amac: JavaFX service manager is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.54.1
// # Aciklama: Apache, Nginx, MySQL, PHP ve Mailpit servisleri icin inspect/preflight/start/stop/restart aksiyonlarini agent process API, aktif web server mode ve port guard uzerinden cagirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class ServiceManagerDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String STATUS_ACTION = "/status";
    private static final String INSPECT_ACTION = "/inspect";
    private static final String PREFLIGHT_ACTION = "/preflight";
    private static final String REAL_PROFILE_ACTION = "/real-profile";
    private static final String START_ACTION = "/start";
    private static final String STOP_ACTION = "/stop";
    private static final String RESTART_ACTION = "/restart";
    private static final String QUERY_PREFIX = "?";
    private static final String QUERY_DRY_RUN = "dry_run=";
    private static final String QUERY_AND = "&";
    private static final String QUERY_ALLOW_REAL_EXECUTION = "allow_real_execution=";

    private final HttpRequestTool httpRequestTool;
    private final ServiceResultFormatterService serviceResultFormatterService;

    public ServiceManagerDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.serviceResultFormatterService = new ServiceResultFormatterService();
    }

    public ServiceManagerSummary listServicesSummary() {
        return serviceResultFormatterService.formatList(listServices());
    }

    public ServiceManagerSummary statusSummary(String serviceCode) {
        return serviceResultFormatterService.formatStatus(serviceCode, statusService(serviceCode));
    }

    public ServiceManagerSummary preflightSummary(String serviceCode) {
        return serviceResultFormatterService.formatPreflight(serviceCode, preflightService(serviceCode));
    }

    public ServiceManagerSummary realProfileSummary(String serviceCode) {
        return serviceResultFormatterService.formatRealProfile(serviceCode, realProfileService(serviceCode));
    }

    public ServiceManagerSummary startSummary(String serviceCode) {
        return serviceResultFormatterService.formatStart(serviceCode, startService(serviceCode));
    }

    public ServiceManagerSummary stopSummary(String serviceCode) {
        return serviceResultFormatterService.formatStop(serviceCode, stopService(serviceCode));
    }

    public ServiceManagerSummary restartSummary(String serviceCode) {
        return serviceResultFormatterService.formatRestart(serviceCode, restartService(serviceCode));
    }

    public DesktopHttpResult listServices() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.PROCESS_ROUTE));
    }

    public DesktopHttpResult statusService(String serviceCode) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, INSPECT_ACTION)));
    }

    public DesktopHttpResult preflightService(String serviceCode) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, PREFLIGHT_ACTION)));
    }

    public DesktopHttpResult realProfileService(String serviceCode) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, REAL_PROFILE_ACTION)));
    }

    public DesktopHttpResult startService(String serviceCode) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, START_ACTION)) + buildStateQuery());
    }

    public DesktopHttpResult stopService(String serviceCode) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, STOP_ACTION)) + buildStateQuery());
    }

    public DesktopHttpResult restartService(String serviceCode) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildServiceActionRoute(serviceCode, RESTART_ACTION)) + buildStateQuery());
    }

    private String buildServiceActionRoute(String serviceCode, String action) {
        return DesktopApiConfig.PROCESS_ROUTE
            + PATH_SEPARATOR
            + encode(serviceCode)
            + action;
    }

    private String buildStateQuery() {
        return QUERY_PREFIX
            + QUERY_DRY_RUN
            + DesktopApiConfig.SERVICE_MANAGER_STATE_DRY_RUN
            + QUERY_AND
            + QUERY_ALLOW_REAL_EXECUTION
            + DesktopApiConfig.SERVICE_MANAGER_REAL_EXECUTION;
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value, StandardCharsets.UTF_8);
    }
}
