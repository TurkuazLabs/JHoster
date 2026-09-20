// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\models\LicensePlanSummary.java
// # 📌 Amac: Desktop lisans, plan ve feature registry durumu ozetini tasir
// # 📌 Modul - Java
// # Version: 3.65.0
// # Aciklama: Community ve Pro plan bilgilerini UI, feature listesi ve log katmanina standart model olarak aktarir
// # Bagimli Oldugu Katman: Service

package com.jhoster.desktop.models;

public final class LicensePlanSummary {
    private static final int UNLIMITED_LIMIT = -1;
    private static final String DEFAULT_TITLE = "License Status";
    private static final String DEFAULT_PLAN_KEY = "community";
    private static final String DEFAULT_PLAN_LABEL = "Community";
    private static final String UNKNOWN_USAGE = "0 / 5";
    private static final String UNLIMITED_LABEL = "Unlimited";
    private static final String DEFAULT_MESSAGE = "License status ready";
    private static final String DEFAULT_UPGRADE_HINT = "Pro unlocks unlimited active sites and advanced modules.";
    private static final String FEATURE_STATUS_INCLUDED = "Included";
    private static final String FEATURE_STATUS_PRO_LOCKED = "Pro Locked";
    private static final String LINE_SEPARATOR = System.lineSeparator();

    private final String title;
    private final boolean success;
    private final String planKey;
    private final String planLabel;
    private final int activeProjectCount;
    private final int maxActiveProjects;
    private final String usageLabel;
    private final boolean canCreateProject;
    private final String message;
    private final String upgradeHint;
    private final boolean siteLimitEnabled;
    private final boolean advancedSslEnabled;
    private final boolean automatedBackupEnabled;
    private final boolean advancedDnsEnabled;
    private final boolean aiOllamaEnabled;
    private final String rawLog;

    public LicensePlanSummary(
        String title,
        boolean success,
        String planKey,
        String planLabel,
        int activeProjectCount,
        int maxActiveProjects,
        String usageLabel,
        boolean canCreateProject,
        String message,
        String upgradeHint,
        boolean siteLimitEnabled,
        boolean advancedSslEnabled,
        boolean automatedBackupEnabled,
        boolean advancedDnsEnabled,
        boolean aiOllamaEnabled,
        String rawLog
    ) {
        this.title = fallback(title, DEFAULT_TITLE);
        this.success = success;
        this.planKey = fallback(planKey, DEFAULT_PLAN_KEY);
        this.planLabel = fallback(planLabel, DEFAULT_PLAN_LABEL);
        this.activeProjectCount = activeProjectCount;
        this.maxActiveProjects = maxActiveProjects;
        this.usageLabel = fallback(usageLabel, buildUsageLabel(activeProjectCount, maxActiveProjects));
        this.canCreateProject = canCreateProject;
        this.message = fallback(message, DEFAULT_MESSAGE);
        this.upgradeHint = fallback(upgradeHint, DEFAULT_UPGRADE_HINT);
        this.siteLimitEnabled = siteLimitEnabled;
        this.advancedSslEnabled = advancedSslEnabled;
        this.automatedBackupEnabled = automatedBackupEnabled;
        this.advancedDnsEnabled = advancedDnsEnabled;
        this.aiOllamaEnabled = aiOllamaEnabled;
        this.rawLog = fallback(rawLog, "");
    }

    public static LicensePlanSummary empty() {
        return new LicensePlanSummary(
            DEFAULT_TITLE,
            false,
            DEFAULT_PLAN_KEY,
            DEFAULT_PLAN_LABEL,
            0,
            5,
            UNKNOWN_USAGE,
            true,
            "License endpoint not ready",
            DEFAULT_UPGRADE_HINT,
            true,
            false,
            false,
            false,
            false,
            ""
        );
    }

    public String getTitle() {
        return title;
    }

    public boolean isSuccess() {
        return success;
    }

    public String getPlanKey() {
        return planKey;
    }

    public String getPlanLabel() {
        return planLabel;
    }

    public int getActiveProjectCount() {
        return activeProjectCount;
    }

    public int getMaxActiveProjects() {
        return maxActiveProjects;
    }

    public String getUsageLabel() {
        return usageLabel;
    }

    public boolean canCreateProject() {
        return canCreateProject;
    }

    public String getMessage() {
        return message;
    }

    public String getUpgradeHint() {
        return upgradeHint;
    }

    public boolean isSiteLimitEnabled() {
        return siteLimitEnabled;
    }

    public boolean isAdvancedSslEnabled() {
        return advancedSslEnabled;
    }

    public boolean isAutomatedBackupEnabled() {
        return automatedBackupEnabled;
    }

    public boolean isAdvancedDnsEnabled() {
        return advancedDnsEnabled;
    }

    public boolean isAiOllamaEnabled() {
        return aiOllamaEnabled;
    }

    public String getSiteLimitStatusLabel() {
        return featureStatus(siteLimitEnabled);
    }

    public String getAdvancedSslStatusLabel() {
        return featureStatus(advancedSslEnabled);
    }

    public String getAutomatedBackupStatusLabel() {
        return featureStatus(automatedBackupEnabled);
    }

    public String getAdvancedDnsStatusLabel() {
        return featureStatus(advancedDnsEnabled);
    }

    public String getAiOllamaStatusLabel() {
        return featureStatus(aiOllamaEnabled);
    }

    public String toStatusText() {
        if (!success) {
            return "License offline";
        }

        return planLabel + " | Sites " + usageLabel;
    }

    public String toLogBlock() {
        return title + LINE_SEPARATOR
            + "status=" + (success ? "ok" : "offline") + LINE_SEPARATOR
            + "plan=" + planLabel + LINE_SEPARATOR
            + "usage=" + usageLabel + LINE_SEPARATOR
            + "canCreateProject=" + canCreateProject + LINE_SEPARATOR
            + "advancedSsl=" + getAdvancedSslStatusLabel() + LINE_SEPARATOR
            + "automatedBackup=" + getAutomatedBackupStatusLabel() + LINE_SEPARATOR
            + "advancedDns=" + getAdvancedDnsStatusLabel() + LINE_SEPARATOR
            + "aiOllama=" + getAiOllamaStatusLabel() + LINE_SEPARATOR
            + "message=" + message + LINE_SEPARATOR
            + rawLog;
    }

    private static String buildUsageLabel(int activeProjectCount, int maxActiveProjects) {
        if (maxActiveProjects == UNLIMITED_LIMIT) {
            return activeProjectCount + " / " + UNLIMITED_LABEL;
        }

        return activeProjectCount + " / " + maxActiveProjects;
    }

    private static String featureStatus(boolean enabled) {
        return enabled ? FEATURE_STATUS_INCLUDED : FEATURE_STATUS_PRO_LOCKED;
    }

    private static String fallback(String value, String fallbackValue) {
        return value == null || value.isBlank() ? fallbackValue : value;
    }
}
