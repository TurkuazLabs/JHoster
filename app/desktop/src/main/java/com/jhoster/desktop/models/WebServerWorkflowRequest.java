// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\WebServerWorkflowRequest.java
// # 📌 Amac: Desktop unified web server workflow istegini model olarak tasir
// # 📌 Modul - Java
// # Version: 3.35.0
// # Aciklama: Project code, domain, port, target dir ve guvenli execution flag degerlerini Service katmanina aktarir
// # Bagimli Oldugu Katman: Repo/Model

package com.jhoster.desktop.models;

import com.jhoster.desktop.config.DesktopApiConfig;

public final class WebServerWorkflowRequest {
    private final String projectCode;
    private final String domain;
    private final int port;
    private final String targetDir;
    private final boolean dryRun;
    private final boolean reload;
    private final boolean allowRealExecution;
    private final boolean rollbackOnFailure;

    public WebServerWorkflowRequest(
        String projectCode,
        String domain,
        int port,
        String targetDir,
        boolean dryRun,
        boolean reload,
        boolean allowRealExecution,
        boolean rollbackOnFailure
    ) {
        this.projectCode = normalize(projectCode, DesktopApiConfig.DEFAULT_WORKFLOW_PROJECT_CODE);
        this.domain = normalize(domain, DesktopApiConfig.DEFAULT_WORKFLOW_DOMAIN);
        this.port = port <= 0 ? DesktopApiConfig.DEFAULT_WORKFLOW_PORT : port;
        this.targetDir = normalize(targetDir, DesktopApiConfig.DEFAULT_WORKFLOW_TARGET_DIR);
        this.dryRun = dryRun;
        this.reload = reload;
        this.allowRealExecution = allowRealExecution;
        this.rollbackOnFailure = rollbackOnFailure;
    }

    public static WebServerWorkflowRequest safeDryRun(String projectCode, String domain, int port, String targetDir) {
        return new WebServerWorkflowRequest(
            projectCode,
            domain,
            port,
            targetDir,
            DesktopApiConfig.SAFE_DRY_RUN,
            DesktopApiConfig.DEFAULT_WORKFLOW_RELOAD,
            DesktopApiConfig.SAFE_REAL_EXECUTION,
            DesktopApiConfig.DEFAULT_WORKFLOW_ROLLBACK_ON_FAILURE
        );
    }

    public String getProjectCode() {
        return projectCode;
    }

    public String getDomain() {
        return domain;
    }

    public int getPort() {
        return port;
    }

    public String getTargetDir() {
        return targetDir;
    }

    public boolean isDryRun() {
        return dryRun;
    }

    public boolean isReload() {
        return reload;
    }

    public boolean isAllowRealExecution() {
        return allowRealExecution;
    }

    public boolean isRollbackOnFailure() {
        return rollbackOnFailure;
    }

    private static String normalize(String value, String fallback) {
        if (value == null || value.isBlank()) {
            return fallback;
        }
        return value.trim();
    }
}
