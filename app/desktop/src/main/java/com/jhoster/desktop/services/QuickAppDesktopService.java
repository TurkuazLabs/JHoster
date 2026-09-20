// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\QuickAppDesktopService.java
// # 📌 Amac: JavaFX Quick App ve New Site stack secimi is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.76.1
// # Aciklama: Quick App template listeleme, stack secimli planlama ve guvenli scaffold create aksiyonlarini agent API uzerinden cagirir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.QuickAppSummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class QuickAppDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String TEMPLATES_ACTION = "/templates";
    private static final String PLAN_ACTION = "/plan";
    private static final String CREATE_ACTION = "/create";
    private static final String QUERY_PREFIX = "?";
    private static final String QUERY_AND = "&";
    private static final String QUERY_TEMPLATE_CODE = "template_code=";
    private static final String QUERY_PROJECT_NAME = "project_name=";
    private static final String QUERY_DOMAIN = "domain=";
    private static final String QUERY_PORT = "port=";
    private static final String QUERY_DRY_RUN = "dry_run=";
    private static final String QUERY_WEB_SERVER = "web_server=";
    private static final String QUERY_INCLUDE_MYSQL = "include_mysql=";
    private static final String QUERY_INCLUDE_PHP = "include_php=";
    private static final String QUERY_INCLUDE_MAILPIT = "include_mailpit=";

    private final HttpRequestTool httpRequestTool;
    private final QuickAppResultFormatterService quickAppResultFormatterService;

    public QuickAppDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.quickAppResultFormatterService = new QuickAppResultFormatterService();
    }

    public QuickAppSummary templatesSummary() {
        return quickAppResultFormatterService.formatTemplates(listTemplates());
    }

    public QuickAppSummary planSummary(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return quickAppResultFormatterService.formatPlan(
            projectCode,
            templateCode,
            planApp(projectCode, projectName, templateCode, domain, port, webServer, includeMysql, includePhp, includeMailpit)
        );
    }

    public QuickAppSummary createSummary(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return quickAppResultFormatterService.formatCreate(
            projectCode,
            templateCode,
            createApp(projectCode, projectName, templateCode, domain, port, webServer, includeMysql, includePhp, includeMailpit)
        );
    }

    public DesktopHttpResult listTemplates() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.QUICK_APPS_ROUTE + TEMPLATES_ACTION));
    }

    public DesktopHttpResult planApp(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(buildProjectRoute(projectCode) + PLAN_ACTION) + buildQuery(projectName, templateCode, domain, port, true, webServer, includeMysql, includePhp, includeMailpit));
    }

    public DesktopHttpResult createApp(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(buildProjectRoute(projectCode) + CREATE_ACTION) + buildQuery(projectName, templateCode, domain, port, DesktopApiConfig.QUICK_APP_CREATE_DRY_RUN, webServer, includeMysql, includePhp, includeMailpit));
    }

    private String buildProjectRoute(String projectCode) {
        return DesktopApiConfig.QUICK_APPS_ROUTE + PATH_SEPARATOR + encode(projectCode);
    }

    private String buildQuery(String projectName, String templateCode, String domain, int port, boolean dryRun, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return QUERY_PREFIX
            + QUERY_TEMPLATE_CODE + encode(templateCode)
            + QUERY_AND + QUERY_PROJECT_NAME + encode(projectName)
            + QUERY_AND + QUERY_DOMAIN + encode(domain)
            + QUERY_AND + QUERY_PORT + port
            + QUERY_AND + QUERY_DRY_RUN + dryRun
            + QUERY_AND + QUERY_WEB_SERVER + encode(webServer)
            + QUERY_AND + QUERY_INCLUDE_MYSQL + includeMysql
            + QUERY_AND + QUERY_INCLUDE_PHP + includePhp
            + QUERY_AND + QUERY_INCLUDE_MAILPIT + includeMailpit;
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value.trim(), StandardCharsets.UTF_8);
    }
}
