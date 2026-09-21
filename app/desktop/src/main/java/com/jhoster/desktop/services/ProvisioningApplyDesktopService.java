// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\ProvisioningApplyDesktopService.java
// # 📌 Amac: Desktop New Site provisioning plan ve apply API isteklerini yonetir
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: GET plan ve kullanici onayli JSON POST apply isteklerini agent API'ye gonderir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.ProvisioningApplySummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class ProvisioningApplyDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String PLAN_ACTION = "/plan";
    private static final String APPLY_ACTION = "/apply";
    private final HttpRequestTool httpRequestTool = new HttpRequestTool();
    private final ProvisioningApplyResultFormatterService formatter = new ProvisioningApplyResultFormatterService();

    public ProvisioningApplySummary planSummary(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        DesktopHttpResult result = httpRequestTool.get(
            DesktopApiConfig.resolveUrl(buildProjectRoute(projectCode) + PLAN_ACTION)
                + buildPlanQuery(projectName, templateCode, domain, port, webServer, includeMysql, includePhp, includeMailpit)
        );
        return formatter.formatPlan(projectCode, result);
    }

    public ProvisioningApplySummary applySummary(String projectCode, String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit, String mysqlAdminPassword) {
        DesktopHttpResult result = httpRequestTool.postJson(
            DesktopApiConfig.resolveUrl(buildProjectRoute(projectCode) + APPLY_ACTION),
            buildApplyBody(projectName, templateCode, domain, port, webServer, includeMysql, includePhp, includeMailpit, mysqlAdminPassword)
        );
        return formatter.formatApply(projectCode, result);
    }

    private String buildProjectRoute(String projectCode) {
        return DesktopApiConfig.PROVISIONING_APPLY_ROUTE + PATH_SEPARATOR + encode(projectCode);
    }

    private String buildPlanQuery(String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit) {
        return "?template_code=" + encode(templateCode)
            + "&project_name=" + encode(projectName)
            + "&domain=" + encode(domain)
            + "&port=" + port
            + "&web_server=" + encode(webServer)
            + "&include_mysql=" + includeMysql
            + "&include_php=" + includePhp
            + "&include_mailpit=" + includeMailpit
            + "&mysql_admin_user=" + encode(DesktopApiConfig.DEFAULT_MYSQL_ADMIN_USER);
    }

    private String buildApplyBody(String projectName, String templateCode, String domain, int port, String webServer, boolean includeMysql, boolean includePhp, boolean includeMailpit, String mysqlAdminPassword) {
        return "{"
            + "\"project_name\":" + quote(projectName) + ","
            + "\"template_code\":" + quote(templateCode) + ","
            + "\"domain\":" + quote(domain) + ","
            + "\"port\":" + port + ","
            + "\"web_server\":" + quote(webServer) + ","
            + "\"include_mysql\":" + includeMysql + ","
            + "\"include_php\":" + includePhp + ","
            + "\"include_mailpit\":" + includeMailpit + ","
            + "\"dry_run\":false,"
            + "\"approved\":true,"
            + "\"allow_real_execution\":" + DesktopApiConfig.PROVISIONING_ALLOW_REAL_EXECUTION + ","
            + "\"target_dir\":\"\","
            + "\"mysql_admin_user\":" + quote(DesktopApiConfig.DEFAULT_MYSQL_ADMIN_USER) + ","
            + "\"mysql_admin_password\":" + quote(mysqlAdminPassword)
            + "}";
    }

    private String quote(String value) { return "\"" + escapeJson(value) + "\""; }

    private String escapeJson(String value) {
        String safeValue = value == null ? "" : value;
        return safeValue.replace("\\", "\\\\").replace("\"", "\\\"").replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t");
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value.trim(), StandardCharsets.UTF_8);
    }
}
