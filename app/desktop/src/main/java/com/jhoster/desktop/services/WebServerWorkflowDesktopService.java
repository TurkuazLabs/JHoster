// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\services\WebServerWorkflowDesktopService.java
// # 📌 Amac: JavaFX unified web server workflow is kurallarini yonetir
// # 📌 Modul - Java
// # Version: 3.54.1
// # Aciklama: Active profile secimi, Apache/Nginx mode switch, workflow plan, dry-run, run listesi ve lock listesi aksiyonlarini agent API uzerinden cagirir ve ozetler
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.services;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.DesktopHttpResult;
import com.jhoster.desktop.models.WebServerWorkflowRequest;
import com.jhoster.desktop.models.WorkflowDesktopSummary;
import com.jhoster.desktop.tools.HttpRequestTool;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

public final class WebServerWorkflowDesktopService {
    private static final String PATH_SEPARATOR = "/";
    private static final String PLAN_ACTION = "/plan";
    private static final String RUN_ACTION = "/run";
    private static final String QUERY_PREFIX = "?";
    private static final String QUERY_AND = "&";
    private static final String QUERY_DOMAIN = "domain=";
    private static final String QUERY_PORT = "port=";
    private static final String QUERY_TARGET_DIR = "target_dir=";
    private static final String QUERY_DRY_RUN = "dry_run=";
    private static final String QUERY_RELOAD = "reload=";
    private static final String QUERY_ALLOW_REAL_EXECUTION = "allow_real_execution=";
    private static final String QUERY_ROLLBACK_ON_FAILURE = "rollback_on_failure=";

    private final HttpRequestTool httpRequestTool;
    private final WorkflowResultFormatterService workflowResultFormatterService;

    public WebServerWorkflowDesktopService() {
        this.httpRequestTool = new HttpRequestTool();
        this.workflowResultFormatterService = new WorkflowResultFormatterService();
    }

    public DesktopHttpResult getCurrentProfile() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.WEB_SERVER_CURRENT_PROFILE_ROUTE));
    }

    public DesktopHttpResult selectProfile(String serverCode) {
        String route = DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(serverCode)
            ? DesktopApiConfig.WEB_SERVER_PROFILE_NGINX_SELECT_ROUTE
            : DesktopApiConfig.WEB_SERVER_PROFILE_APACHE_SELECT_ROUTE;
        return httpRequestTool.post(DesktopApiConfig.resolveUrl(route) + DesktopApiConfig.WEB_SERVER_PROFILE_SELECT_DRY_RUN_FALSE_QUERY);
    }

    public DesktopHttpResult listRuns() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.WEB_SERVER_WORKFLOW_RUNS_ROUTE));
    }

    public DesktopHttpResult listLocks() {
        return httpRequestTool.get(DesktopApiConfig.resolveUrl(DesktopApiConfig.WEB_SERVER_WORKFLOW_LOCKS_ROUTE));
    }


    public WorkflowDesktopSummary getCurrentProfileSummary() {
        return workflowResultFormatterService.formatProfile(getCurrentProfile());
    }

    public WorkflowDesktopSummary selectProfileSummary(String serverCode) {
        return workflowResultFormatterService.formatProfile(selectProfile(serverCode));
    }

    public WorkflowDesktopSummary listRunsSummary() {
        return workflowResultFormatterService.formatRuns(listRuns());
    }

    public WorkflowDesktopSummary listLocksSummary() {
        return workflowResultFormatterService.formatLocks(listLocks());
    }

    public WorkflowDesktopSummary planWorkflowSummary(WebServerWorkflowRequest request) {
        return workflowResultFormatterService.formatPlan(planWorkflow(request));
    }

    public WorkflowDesktopSummary runDryWorkflowSummary(WebServerWorkflowRequest request) {
        return workflowResultFormatterService.formatDryRun(runDryWorkflow(request));
    }

    public DesktopHttpResult planWorkflow(WebServerWorkflowRequest request) {
        String url = DesktopApiConfig.resolveUrl(buildProjectActionRoute(request.getProjectCode(), PLAN_ACTION))
            + buildWorkflowPlanQuery(request);
        return httpRequestTool.get(url);
    }

    public DesktopHttpResult runDryWorkflow(WebServerWorkflowRequest request) {
        String url = DesktopApiConfig.resolveUrl(buildProjectActionRoute(request.getProjectCode(), RUN_ACTION))
            + buildWorkflowRunQuery(request);
        return httpRequestTool.post(url);
    }

    private String buildProjectActionRoute(String projectCode, String action) {
        return DesktopApiConfig.WEB_SERVER_WORKFLOW_ROUTE
            + PATH_SEPARATOR
            + encode(projectCode)
            + action;
    }

    private String buildWorkflowPlanQuery(WebServerWorkflowRequest request) {
        return QUERY_PREFIX
            + QUERY_DOMAIN + encode(request.getDomain())
            + QUERY_AND + QUERY_PORT + request.getPort()
            + QUERY_AND + QUERY_TARGET_DIR + encode(request.getTargetDir())
            + QUERY_AND + QUERY_RELOAD + request.isReload()
            + QUERY_AND + QUERY_ROLLBACK_ON_FAILURE + request.isRollbackOnFailure();
    }

    private String buildWorkflowRunQuery(WebServerWorkflowRequest request) {
        return QUERY_PREFIX
            + QUERY_DOMAIN + encode(request.getDomain())
            + QUERY_AND + QUERY_PORT + request.getPort()
            + QUERY_AND + QUERY_TARGET_DIR + encode(request.getTargetDir())
            + QUERY_AND + QUERY_DRY_RUN + request.isDryRun()
            + QUERY_AND + QUERY_RELOAD + request.isReload()
            + QUERY_AND + QUERY_ALLOW_REAL_EXECUTION + request.isAllowRealExecution()
            + QUERY_AND + QUERY_ROLLBACK_ON_FAILURE + request.isRollbackOnFailure();
    }

    private String encode(String value) {
        return URLEncoder.encode(value == null ? "" : value, StandardCharsets.UTF_8);
    }
}
