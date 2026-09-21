// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\controllers\LauncherController.java
// # 📌 Amac: JavaFX launcher buton olaylarini servis katmanina aktarir
// # 📌 Modul - Java
// # Version: 3.79.0
// # Aciklama: Agent lifecycle, dinamik UI sayfalari, dev mode gizli endpoint menusu, package downloader, sol menu normal modu, ayarlar menusu, servis secimli Start All akisi ve workflow, hosts auto ve New Site wizard aksiyonlarini ince Controller katmaninda baglar
// # Bagimli Oldugu Katman: Controller

package com.jhoster.desktop.controllers;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.models.QuickAppSummary;
import com.jhoster.desktop.models.ProvisioningApplySummary;
import com.jhoster.desktop.models.PackageDownloadSummary;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.models.DesktopServiceSelectionSettings;
import com.jhoster.desktop.models.WebServerWorkflowRequest;
import com.jhoster.desktop.models.WorkflowDesktopSummary;
import com.jhoster.desktop.models.LicensePlanSummary;
import com.jhoster.desktop.models.HostsAutoSummary;
import com.jhoster.desktop.services.AgentProcessService;
import com.jhoster.desktop.services.PanelStatusService;
import com.jhoster.desktop.services.RuntimeManagerDesktopService;
import com.jhoster.desktop.services.QuickAppDesktopService;
import com.jhoster.desktop.services.ProvisioningApplyDesktopService;
import com.jhoster.desktop.services.PackageDownloadDesktopService;
import com.jhoster.desktop.services.QuickActionDesktopService;
import com.jhoster.desktop.services.ServiceManagerDesktopService;
import com.jhoster.desktop.services.DesktopServiceSelectionService;
import com.jhoster.desktop.services.WebServerWorkflowDesktopService;
import com.jhoster.desktop.services.LicenseDesktopService;
import com.jhoster.desktop.services.HostsAutoDesktopService;
import com.jhoster.desktop.tools.BrowserTool;
import com.jhoster.desktop.views.LauncherView;
import javafx.concurrent.Task;
import javafx.scene.Parent;

public class LauncherController {
    private static final String LOG_WORKFLOW_PROFILE = "Workflow active profile";
    private static final String LOG_WORKFLOW_PLAN = "Workflow plan";
    private static final String LOG_WORKFLOW_DRY_RUN = "Workflow dry-run";
    private static final String LOG_WORKFLOW_RUNS = "Workflow runs";
    private static final String LOG_WORKFLOW_LOCKS = "Workflow locks";
    private static final String LOG_AGENT_RUNNING = "Agent status: running";
    private static final String LOG_AGENT_STOPPED = "Agent status: stopped";
    private static final String LOG_START_ALL = "Quick Action -> Start All";
    private static final String LOG_STOP_ALL = "Quick Action -> Stop All";
    private static final String LOG_START_ALL_WEB_GUARD = "Quick Action -> Start All uses selected public web server and skips the other web server to avoid 80/443 conflict";
    private static final String LOG_DASHBOARD_REFRESH = "Dashboard -> refresh overview";
    private static final String LOG_DIAGNOSTICS_OPEN = "Diagnostics -> UI page opened";
    private static final String LOG_WEB_MODE_APACHE = "Settings -> Web Server Mode -> Apache";
    private static final String LOG_WEB_MODE_NGINX = "Settings -> Web Server Mode -> Nginx";
    private static final String LOG_WEB_DECK_SWITCH = "Deck -> Web Server switch";
    private static final String LOG_SETTINGS_OPEN = "Settings -> service selection menu";
    private static final String LOG_DEV_MODE_ENABLED = "Dev Mode -> enabled by startup gate";
    private static final String LOG_LICENSE_REFRESH = "License -> refresh status";
    private static final String LOG_HOSTS_AUTO_INSPECT = "Hosts Auto -> inspect real hosts";
    private static final String LOG_HOSTS_AUTO_REPAIR_PLAN = "Hosts Auto -> repair plan";
    private static final String LOG_HOSTS_AUTO_REPAIR = "Hosts Auto -> repair real hosts";

    private final AgentProcessService agentProcessService;
    private final PanelStatusService panelStatusService;
    private final RuntimeManagerDesktopService runtimeManagerDesktopService;
    private final QuickAppDesktopService quickAppDesktopService;
    private final ProvisioningApplyDesktopService provisioningApplyDesktopService;
    private final PackageDownloadDesktopService packageDownloadDesktopService;
    private final QuickActionDesktopService quickActionDesktopService;
    private final ServiceManagerDesktopService serviceManagerDesktopService;
    private final DesktopServiceSelectionService desktopServiceSelectionService;
    private final WebServerWorkflowDesktopService webServerWorkflowDesktopService;
    private final LicenseDesktopService licenseDesktopService;
    private final HostsAutoDesktopService hostsAutoDesktopService;
    private final BrowserTool browserTool;
    private final LauncherView launcherView;
    private final boolean devModeEnabled;

    public LauncherController() {
        this(false);
    }

    public LauncherController(boolean devModeEnabled) {
        this.devModeEnabled = devModeEnabled;
        this.agentProcessService = new AgentProcessService();
        this.panelStatusService = new PanelStatusService();
        this.runtimeManagerDesktopService = new RuntimeManagerDesktopService();
        this.quickAppDesktopService = new QuickAppDesktopService();
        this.provisioningApplyDesktopService = new ProvisioningApplyDesktopService();
        this.packageDownloadDesktopService = new PackageDownloadDesktopService();
        this.quickActionDesktopService = new QuickActionDesktopService();
        this.serviceManagerDesktopService = new ServiceManagerDesktopService();
        this.desktopServiceSelectionService = new DesktopServiceSelectionService();
        this.webServerWorkflowDesktopService = new WebServerWorkflowDesktopService();
        this.licenseDesktopService = new LicenseDesktopService();
        this.hostsAutoDesktopService = new HostsAutoDesktopService();
        this.browserTool = new BrowserTool();
        this.launcherView = new LauncherView(devModeEnabled);
    }

    public Parent createView() {
        launcherView.setOnNavDashboard(event -> {
            launcherView.showOverviewPage();
            refreshDashboardOverview();
        });
        launcherView.setOnNavNewSite(event -> {
            launcherView.showNewSitePage();
            appendQuickAppSummary(quickAppDesktopService.templatesSummary());
        });
        launcherView.setOnNavServices(event -> {
            launcherView.showServicesPage();
            refreshAllServiceStatuses();
        });
        launcherView.setOnNavProjects(event -> launcherView.showProjectsPage());
        launcherView.setOnNavVirtualHosts(event -> launcherView.showVirtualHostsPage());
        launcherView.setOnNavApps(event -> launcherView.showAppsPage());
        launcherView.setOnNavVersions(event -> {
            launcherView.showRuntimeVersionsPage();
            appendRuntimeSummary(runtimeManagerDesktopService.listRuntimeSummary());
        });
        launcherView.setOnNavWorkflow(event -> {
            launcherView.showWorkflowPage();
            appendWorkflowSummary(webServerWorkflowDesktopService.getCurrentProfileSummary());
        });
        launcherView.setOnNavTools(event -> launcherView.showToolsPage());
        launcherView.setOnNavDeveloper(event -> launcherView.showDeveloperPage());
        launcherView.setOnNavLogs(event -> launcherView.showLogsPage());
        launcherView.setOnNavSettings(event -> openServiceSettingsMenu());
        launcherView.setOnOverviewTab(event -> {
            launcherView.showOverviewPage();
            refreshDashboardOverview();
        });
        launcherView.setOnRuntimeVersionsTab(event -> {
            launcherView.showRuntimeVersionsPage();
            appendRuntimeSummary(runtimeManagerDesktopService.listRuntimeSummary());
        });
        launcherView.setOnQuickAppTab(event -> {
            launcherView.showQuickAppPage();
            appendQuickAppSummary(quickAppDesktopService.templatesSummary());
        });
        launcherView.setOnPackageCatalog(event -> appendPackageDownloadSummary(packageDownloadDesktopService.catalogSummary()));
        launcherView.setOnPackagePlan(event -> appendPackageDownloadSummary(packageDownloadDesktopService.planSummary(launcherView.getPackageCodeInput())));
        launcherView.setOnPackageDownload(event -> appendPackageDownloadSummary(packageDownloadDesktopService.downloadSummary(launcherView.getPackageCodeInput())));
        launcherView.setOnPackageInstall(event -> appendPackageDownloadSummary(packageDownloadDesktopService.installSummary(launcherView.getPackageCodeInput())));
        launcherView.setOnOpenPackageCenter(event -> launcherView.showPackageCenterDialog());
        launcherView.setOnWorkflowTab(event -> {
            launcherView.showWorkflowPage();
            appendWorkflowSummary(webServerWorkflowDesktopService.getCurrentProfileSummary());
        });
        launcherView.setOnDiagnosticsTab(event -> {
            launcherView.showDiagnosticsPage();
            launcherView.appendLog(LOG_DIAGNOSTICS_OPEN);
        });
        launcherView.setOnManageServices(event -> {
            launcherView.showServicesPage();
            refreshAllServiceStatuses();
        });
        launcherView.setOnViewAllLogs(event -> launcherView.showLogsPage());
        launcherView.setOnClearCurrentLog(event -> {
            launcherView.clearSelectedLogTab();
            launcherView.appendLog("Logs -> active tab cleared");
        });
        launcherView.setOnOpenCurrentLog(event -> launcherView.appendLog(quickActionDesktopService.openLogFolder(launcherView.getSelectedSimpleLogFolder())));
        launcherView.setOnSystemSettings(event -> openServiceSettingsMenu());
        launcherView.setOnSelectApacheWebServer(event -> switchActiveWebServer(DesktopApiConfig.WEB_SERVER_PROFILE_APACHE));
        launcherView.setOnSelectNginxWebServer(event -> switchActiveWebServer(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX));
        launcherView.setOnSimpleWebServerStart(event -> startActiveWebServer());
        launcherView.setOnSimpleWebServerStop(event -> stopActiveWebServer());
        launcherView.setOnSimpleWebServerRestart(event -> restartActiveWebServer());
        launcherView.setOnSimpleWebServerSwitch(event -> switchToOtherWebServer());
        launcherView.setOnStartAgent(event -> launcherView.appendLog(agentProcessService.startAgent()));
        launcherView.setOnStopAgent(event -> launcherView.appendLog(agentProcessService.stopAgent()));
        launcherView.setOnRestartAgent(event -> launcherView.appendLog(agentProcessService.restartAgent()));
        launcherView.setOnOpenPanel(event -> browserTool.open(DesktopApiConfig.resolveUrl(DesktopApiConfig.ROOT_ROUTE)));
        launcherView.setOnQuickStartAll(event -> startAllServices());
        launcherView.setOnQuickStopAll(event -> stopAllServices());
        launcherView.setOnQuickWeb(event -> launcherView.appendLog(quickActionDesktopService.openWeb()));
        launcherView.setOnQuickDatabase(event -> launcherView.appendLog(quickActionDesktopService.openDatabase()));
        launcherView.setOnQuickMailpit(event -> launcherView.appendLog(quickActionDesktopService.openMailpit()));
        launcherView.setOnQuickTerminal(event -> launcherView.appendLog(quickActionDesktopService.openTerminal()));
        launcherView.setOnQuickRoot(event -> launcherView.appendLog(quickActionDesktopService.openRoot()));
        launcherView.setOnQuickProjects(event -> launcherView.appendLog(quickActionDesktopService.openProjects()));
        launcherView.setOnQuickLogs(event -> launcherView.appendLog(quickActionDesktopService.openLogs()));
        launcherView.setOnQuickBin(event -> launcherView.appendLog(quickActionDesktopService.openBin()));
        launcherView.setOnQuickCmder(event -> launcherView.appendLog(quickActionDesktopService.openCmder()));
        launcherView.setOnQuickGitBash(event -> launcherView.appendLog(quickActionDesktopService.openGitBash()));
        launcherView.setOnQuickNotepad(event -> launcherView.appendLog(quickActionDesktopService.openNotepad()));
        launcherView.setOnQuickNgrok(event -> launcherView.appendLog(quickActionDesktopService.openNgrok()));
        launcherView.setOnQuickComposer(event -> launcherView.appendLog(quickActionDesktopService.openComposerFolder()));
        launcherView.setOnQuickYarn(event -> launcherView.appendLog(quickActionDesktopService.openYarnFolder()));
        launcherView.setOnOpenComponents(event -> openRoute(DesktopApiConfig.COMPONENTS_ROUTE));
        launcherView.setOnOpenHistory(event -> openRoute(DesktopApiConfig.INSTALL_HISTORY_ROUTE));
        launcherView.setOnOpenCache(event -> openRoute(DesktopApiConfig.CACHE_ROUTE));
        launcherView.setOnOpenApps(event -> openRoute(DesktopApiConfig.APPS_ROUTE));
        launcherView.setOnOpenProcess(event -> openRoute(DesktopApiConfig.PROCESS_ROUTE));
        launcherView.setOnOpenLocalPackages(event -> openRoute(DesktopApiConfig.LOCAL_PACKAGES_ROUTE));
        launcherView.setOnOpenRuntimeVersions(event -> openRoute(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE));
        launcherView.setOnOpenProjects(event -> openRoute(DesktopApiConfig.PROJECTS_ROUTE));
        launcherView.setOnOpenVirtualHosts(event -> openRoute(DesktopApiConfig.VIRTUAL_HOSTS_ROUTE));
        launcherView.setOnOpenNginxReload(event -> openRoute(DesktopApiConfig.NGINX_RELOAD_ROUTE));
        launcherView.setOnOpenNginxExecutable(event -> openRoute(DesktopApiConfig.NGINX_EXECUTABLE_ROUTE));
        launcherView.setOnOpenNginxRealValidate(event -> openRoute(DesktopApiConfig.NGINX_REAL_VALIDATE_ROUTE));
        launcherView.setOnOpenNginxRealReload(event -> openRoute(DesktopApiConfig.NGINX_REAL_RELOAD_ROUTE));
        launcherView.setOnOpenNginxPreflight(event -> openRoute(DesktopApiConfig.NGINX_PREFLIGHT_ROUTE));
        launcherView.setOnOpenHostsPublish(event -> openRoute(DesktopApiConfig.HOSTS_PUBLISH_ROUTE));
        launcherView.setOnOpenHostsApply(event -> openRoute(DesktopApiConfig.HOSTS_APPLY_ROUTE));
        launcherView.setOnOpenWebServerProfiles(event -> openRoute(DesktopApiConfig.WEB_SERVER_PROFILES_ROUTE));
        launcherView.setOnOpenApacheVhosts(event -> openRoute(DesktopApiConfig.APACHE_VHOSTS_ROUTE));
        launcherView.setOnOpenApachePublish(event -> openRoute(DesktopApiConfig.APACHE_PUBLISH_ROUTE));
        launcherView.setOnOpenApacheValidate(event -> openRoute(DesktopApiConfig.APACHE_VALIDATE_ROUTE));
        launcherView.setOnOpenApacheExecutable(event -> openRoute(DesktopApiConfig.APACHE_EXECUTABLE_ROUTE));
        launcherView.setOnOpenApacheRealValidate(event -> openRoute(DesktopApiConfig.APACHE_REAL_VALIDATE_ROUTE));
        launcherView.setOnOpenApacheRealReload(event -> openRoute(DesktopApiConfig.APACHE_REAL_RELOAD_ROUTE));
        launcherView.setOnOpenServiceAdapters(event -> openRoute(DesktopApiConfig.SERVICE_ADAPTERS_ROUTE));
        launcherView.setOnServiceList(event -> refreshAllServiceStatuses());
        launcherView.setOnApacheStatus(event -> appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_APACHE)));
        launcherView.setOnApachePreflight(event -> appendServiceSummary(serviceManagerDesktopService.preflightSummary(DesktopApiConfig.SERVICE_CODE_APACHE)));
        launcherView.setOnApacheStart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_APACHE)) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
            }
        });
        launcherView.setOnApacheStop(event -> appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_APACHE)));
        launcherView.setOnApacheRestart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_APACHE)) {
                appendServiceSummary(serviceManagerDesktopService.restartSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
            }
        });
        launcherView.setOnNginxStatus(event -> appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_NGINX)));
        launcherView.setOnNginxPreflight(event -> appendServiceSummary(serviceManagerDesktopService.preflightSummary(DesktopApiConfig.SERVICE_CODE_NGINX)));
        launcherView.setOnNginxStart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_NGINX)) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
            }
        });
        launcherView.setOnNginxStop(event -> appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_NGINX)));
        launcherView.setOnNginxRestart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_NGINX)) {
                appendServiceSummary(serviceManagerDesktopService.restartSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
            }
        });
        launcherView.setOnMysqlStatus(event -> appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_MYSQL)));
        launcherView.setOnMysqlPreflight(event -> appendServiceSummary(serviceManagerDesktopService.preflightSummary(DesktopApiConfig.SERVICE_CODE_MYSQL)));
        launcherView.setOnMysqlStart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_MYSQL)) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
            }
        });
        launcherView.setOnMysqlStop(event -> appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MYSQL)));
        launcherView.setOnMysqlRestart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_MYSQL)) {
                appendServiceSummary(serviceManagerDesktopService.restartSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
            }
        });
        launcherView.setOnPhpStatus(event -> appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_PHP)));
        launcherView.setOnPhpPreflight(event -> appendServiceSummary(serviceManagerDesktopService.preflightSummary(DesktopApiConfig.SERVICE_CODE_PHP)));
        launcherView.setOnPhpStart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_PHP)) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_PHP));
            }
        });
        launcherView.setOnPhpStop(event -> appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_PHP)));
        launcherView.setOnPhpRestart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_PHP)) {
                appendServiceSummary(serviceManagerDesktopService.restartSummary(DesktopApiConfig.SERVICE_CODE_PHP));
            }
        });
        launcherView.setOnMailpitStatus(event -> appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT)));
        launcherView.setOnMailpitPreflight(event -> appendServiceSummary(serviceManagerDesktopService.preflightSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT)));
        launcherView.setOnMailpitStart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_MAILPIT)) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
            }
        });
        launcherView.setOnMailpitStop(event -> appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT)));
        launcherView.setOnMailpitRestart(event -> {
            if (guardServiceStart(DesktopApiConfig.SERVICE_CODE_MAILPIT)) {
                appendServiceSummary(serviceManagerDesktopService.restartSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
            }
        });
        launcherView.setOnRuntimeList(event -> appendRuntimeSummary(runtimeManagerDesktopService.listRuntimeSummary()));
        launcherView.setOnRuntimeScanBin(event -> appendRuntimeSummary(runtimeManagerDesktopService.portableSummary()));
        launcherView.setOnRuntimeApacheActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_APACHE)));
        launcherView.setOnRuntimeApacheActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeApacheCode())));
        launcherView.setOnRuntimeApacheActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_APACHE, launcherView.getRuntimeApacheFolder())));
        launcherView.setOnRuntimeNginxActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_NGINX)));
        launcherView.setOnRuntimeNginxActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeNginxCode())));
        launcherView.setOnRuntimeNginxActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_NGINX, launcherView.getRuntimeNginxFolder())));
        launcherView.setOnRuntimeMysqlActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_MYSQL)));
        launcherView.setOnRuntimeMysqlActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeMysqlCode())));
        launcherView.setOnRuntimeMysqlActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_MYSQL, launcherView.getRuntimeMysqlFolder())));
        launcherView.setOnRuntimePhpActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_PHP)));
        launcherView.setOnRuntimePhpActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimePhpCode())));
        launcherView.setOnRuntimePhpActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_PHP, launcherView.getRuntimePhpFolder())));
        launcherView.setOnRuntimeNodeActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_NODE)));
        launcherView.setOnRuntimeNodeActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeNodeCode())));
        launcherView.setOnRuntimeNodeActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_NODE, launcherView.getRuntimeNodeFolder())));
        launcherView.setOnRuntimePythonActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_PYTHON)));
        launcherView.setOnRuntimePythonActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimePythonCode())));
        launcherView.setOnRuntimePythonActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_PYTHON, launcherView.getRuntimePythonFolder())));
        launcherView.setOnRuntimeMemcachedActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_MEMCACHED)));
        launcherView.setOnRuntimeMemcachedActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeMemcachedCode())));
        launcherView.setOnRuntimeMemcachedActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_MEMCACHED, launcherView.getRuntimeMemcachedFolder())));
        launcherView.setOnRuntimeRedisActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_REDIS)));
        launcherView.setOnRuntimeRedisActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeRedisCode())));
        launcherView.setOnRuntimeRedisActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_REDIS, launcherView.getRuntimeRedisFolder())));
        launcherView.setOnRuntimeMailpitActive(event -> appendRuntimeSummary(runtimeManagerDesktopService.activeSummary(DesktopApiConfig.RUNTIME_FAMILY_MAILPIT)));
        launcherView.setOnRuntimeMailpitActivate(event -> appendRuntimeSummary(runtimeManagerDesktopService.activateSummary(launcherView.getRuntimeMailpitCode())));
        launcherView.setOnRuntimeMailpitActivatePortable(event -> appendRuntimeSummary(runtimeManagerDesktopService.activatePortableSummary(DesktopApiConfig.RUNTIME_FAMILY_MAILPIT, launcherView.getRuntimeMailpitFolder())));
        launcherView.setOnQuickAppTemplates(event -> appendQuickAppSummary(quickAppDesktopService.templatesSummary()));
        launcherView.setOnQuickAppPlan(event -> appendProvisioningApplySummary(buildProvisioningPlanSummary()));
        launcherView.setOnQuickAppCreate(event -> applyProvisioningFromWizard());
        launcherView.setOnHostsAutoInspect(event -> refreshHostsAutoStatus());
        launcherView.setOnHostsAutoRepairPlan(event -> appendHostsAutoSummaryWithLog(LOG_HOSTS_AUTO_REPAIR_PLAN, hostsAutoDesktopService.repairPlanSummary()));
        launcherView.setOnHostsAutoRepair(event -> appendHostsAutoSummaryWithLog(LOG_HOSTS_AUTO_REPAIR, hostsAutoDesktopService.repairSummary()));
        launcherView.setOnWorkflowProfile(event -> appendWorkflowSummary(webServerWorkflowDesktopService.getCurrentProfileSummary()));
        launcherView.setOnWorkflowPlan(event -> appendWorkflowSummary(webServerWorkflowDesktopService.planWorkflowSummary(buildWorkflowRequest())));
        launcherView.setOnWorkflowDryRun(event -> appendWorkflowSummary(webServerWorkflowDesktopService.runDryWorkflowSummary(buildWorkflowRequest())));
        launcherView.setOnWorkflowRuns(event -> appendWorkflowSummary(webServerWorkflowDesktopService.listRunsSummary()));
        launcherView.setOnWorkflowLocks(event -> appendWorkflowSummary(webServerWorkflowDesktopService.listLocksSummary()));
        launcherView.setOnCheckStatus(event -> refreshDashboardOverview());

        launcherView.applyServiceSelectionSettings(desktopServiceSelectionService.loadSettings());
        refreshLicenseStatus();
        refreshHostsAutoStatus();
        if (devModeEnabled) {
            launcherView.appendLog(LOG_DEV_MODE_ENABLED);
        }
        return launcherView.render();
    }


    private void openServiceSettingsMenu() {
        launcherView.appendLog(LOG_SETTINGS_OPEN);
        DesktopServiceSelectionSettings beforeSettings = desktopServiceSelectionService.loadSettings();
        launcherView.applyServiceSelectionSettings(beforeSettings);
        launcherView.showServiceSettingsDialog(beforeSettings).ifPresent(this::saveAndApplyServiceSettings);
    }

    private void saveAndApplyServiceSettings(DesktopServiceSelectionSettings settings) {
        DesktopServiceSelectionSettings safeSettings = settings == null ? DesktopServiceSelectionSettings.defaults() : settings.normalized();
        launcherView.appendLog(desktopServiceSelectionService.saveSettings(safeSettings));
        launcherView.applyServiceSelectionSettings(safeSettings);
        applyDisabledServiceStops(safeSettings);
        applySelectedWebServerMode(safeSettings);
    }

    private void applyDisabledServiceStops(DesktopServiceSelectionSettings settings) {
        if (!settings.isMysqlEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
        }

        if (!settings.isPhpEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_PHP));
        }

        if (!settings.isMailpitEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
        }
    }

    private void applySelectedWebServerMode(DesktopServiceSelectionSettings settings) {
        if (!settings.isApacheEnabled() && !settings.isNginxEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
            return;
        }

        if (DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(settings.getActiveWebServer())) {
            appendWorkflowSummary(webServerWorkflowDesktopService.selectProfileSummary(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX));
            appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
            if (settings.isNginxEnabled()) {
                appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
            }
            return;
        }

        appendWorkflowSummary(webServerWorkflowDesktopService.selectProfileSummary(DesktopApiConfig.WEB_SERVER_PROFILE_APACHE));
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
        if (settings.isApacheEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
        }
    }

    private boolean guardServiceStart(String serviceCode) {
        if (desktopServiceSelectionService.canStart(serviceCode)) {
            return true;
        }

        launcherView.appendLog(desktopServiceSelectionService.disabledMessage(serviceCode));
        return false;
    }

    private void refreshDashboardOverview() {
        launcherView.appendLog(LOG_DASHBOARD_REFRESH);
        appendHealthStatus();
        refreshLicenseStatus();
        refreshHostsAutoStatus();
        refreshAllServiceStatuses();
    }

    private void openDiagnostics() {
        launcherView.showDiagnosticsPage();
        launcherView.appendLog(LOG_DIAGNOSTICS_OPEN);
    }

    private void openRoute(String route) {
        browserTool.open(DesktopApiConfig.resolveUrl(route));
    }

    private WebServerWorkflowRequest buildWorkflowRequest() {
        return WebServerWorkflowRequest.safeDryRun(
            launcherView.getWorkflowProjectCode(),
            launcherView.getWorkflowDomain(),
            launcherView.getWorkflowPort(),
            launcherView.getWorkflowTargetDir()
        );
    }

    private void refreshAllServiceStatuses() {
        appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
        appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
        appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
        appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_PHP));
        appendServiceSummary(serviceManagerDesktopService.statusSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
    }

    private void startAllServices() {
        launcherView.appendLog(LOG_START_ALL);
        DesktopServiceSelectionSettings settings = desktopServiceSelectionService.loadSettings();
        launcherView.applyServiceSelectionSettings(settings);

        String activeWebServer = settings.activeWebServerServiceCode();
        if (settings.isServiceEnabled(activeWebServer)) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(activeWebServer));
            launcherView.appendLog(LOG_START_ALL_WEB_GUARD);
        } else {
            launcherView.appendLog(desktopServiceSelectionService.disabledMessage(activeWebServer));
        }

        if (settings.isMysqlEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
        }

        if (settings.isPhpEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_PHP));
        }

        if (settings.isMailpitEnabled()) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
        }

        launcherView.setStackControlRunning(true);
    }

    private void startActiveWebServer() {
        DesktopServiceSelectionSettings settings = desktopServiceSelectionService.loadSettings();
        launcherView.applyServiceSelectionSettings(settings);
        String serviceCode = settings.activeWebServerServiceCode();
        if (guardServiceStart(serviceCode)) {
            appendServiceSummary(serviceManagerDesktopService.startSummary(serviceCode));
        }
    }

    private void stopActiveWebServer() {
        DesktopServiceSelectionSettings settings = desktopServiceSelectionService.loadSettings();
        launcherView.applyServiceSelectionSettings(settings);
        appendServiceSummary(serviceManagerDesktopService.stopSummary(settings.activeWebServerServiceCode()));
    }

    private void restartActiveWebServer() {
        DesktopServiceSelectionSettings settings = desktopServiceSelectionService.loadSettings();
        launcherView.applyServiceSelectionSettings(settings);
        String serviceCode = settings.activeWebServerServiceCode();
        if (guardServiceStart(serviceCode)) {
            appendServiceSummary(serviceManagerDesktopService.restartSummary(serviceCode));
        }
    }

    private void switchToOtherWebServer() {
        DesktopServiceSelectionSettings settings = desktopServiceSelectionService.loadSettings();
        String nextWebServer = DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(settings.getActiveWebServer())
            ? DesktopApiConfig.WEB_SERVER_PROFILE_APACHE
            : DesktopApiConfig.WEB_SERVER_PROFILE_NGINX;
        launcherView.appendLog(LOG_WEB_DECK_SWITCH);
        switchActiveWebServer(nextWebServer);
    }

    private void switchActiveWebServer(String serverCode) {
        launcherView.appendLog(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(serverCode) ? LOG_WEB_MODE_NGINX : LOG_WEB_MODE_APACHE);
        DesktopServiceSelectionSettings currentSettings = desktopServiceSelectionService.loadSettings();
        DesktopServiceSelectionSettings nextSettings = new DesktopServiceSelectionSettings(
            serverCode,
            DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(serverCode),
            DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(serverCode),
            currentSettings.isMysqlEnabled(),
            currentSettings.isPhpEnabled(),
            currentSettings.isMailpitEnabled()
        );
        launcherView.appendLog(desktopServiceSelectionService.saveSettings(nextSettings));
        launcherView.applyServiceSelectionSettings(nextSettings);
        applySelectedWebServerMode(nextSettings);
        launcherView.applyServiceSelectionSettings(nextSettings);
    }

    private String getActiveWebServerCode() {
        WorkflowDesktopSummary summary = webServerWorkflowDesktopService.getCurrentProfileSummary();
        launcherView.updateWorkflowSummary(summary);
        if (summary.hasWebServer() && DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(summary.getWebServer())) {
            return DesktopApiConfig.SERVICE_CODE_NGINX;
        }
        return DesktopApiConfig.SERVICE_CODE_APACHE;
    }

    private void stopAllServices() {
        launcherView.appendLog(LOG_STOP_ALL);
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_APACHE));
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_NGINX));
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MYSQL));
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_PHP));
        appendServiceSummary(serviceManagerDesktopService.stopSummary(DesktopApiConfig.SERVICE_CODE_MAILPIT));
        launcherView.setStackControlRunning(false);
    }

    private void appendServiceSummary(ServiceManagerSummary summary) {
        launcherView.updateServiceSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendRuntimeSummary(RuntimeManagerSummary summary) {
        launcherView.updateRuntimeSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendQuickAppSummary(QuickAppSummary summary) {
        launcherView.updateQuickAppSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private ProvisioningApplySummary buildProvisioningPlanSummary() {
        return provisioningApplyDesktopService.planSummary(
            launcherView.getQuickAppProjectCode(),
            launcherView.getQuickAppProjectName(),
            launcherView.getQuickAppTemplateCode(),
            launcherView.getQuickAppDomain(),
            launcherView.getQuickAppPort(),
            launcherView.getQuickAppWebServer(),
            launcherView.isQuickAppMysqlEnabled(),
            launcherView.isQuickAppPhpEnabled(),
            launcherView.isQuickAppMailpitEnabled()
        );
    }

    private void applyProvisioningFromWizard() {
        ProvisioningApplySummary planSummary = buildProvisioningPlanSummary();
        appendProvisioningApplySummary(planSummary);
        if (!planSummary.isSuccess() || !planSummary.isReadyForApply()) {
            launcherView.showProvisioningPlanBlocked(planSummary);
            return;
        }

        if (!launcherView.showProvisioningApplyConfirmation(
            planSummary,
            launcherView.getQuickAppStackLabel(),
            launcherView.getQuickAppDomain()
        )) {
            launcherView.appendLog("Provisioning apply cancelled by user");
            return;
        }

        String mysqlPassword = "";
        if (launcherView.isQuickAppMysqlEnabled()) {
            var passwordResult = launcherView.promptMysqlAdminPassword();
            if (passwordResult.isEmpty()) {
                launcherView.appendLog("Provisioning apply cancelled before MySQL credentials");
                return;
            }
            mysqlPassword = passwordResult.get();
        }

        runProvisioningApplyAsync(mysqlPassword);
    }

    private void runProvisioningApplyAsync(String mysqlPassword) {
        String projectCode = launcherView.getQuickAppProjectCode();
        String projectName = launcherView.getQuickAppProjectName();
        String templateCode = launcherView.getQuickAppTemplateCode();
        String domain = launcherView.getQuickAppDomain();
        int port = launcherView.getQuickAppPort();
        String webServer = launcherView.getQuickAppWebServer();
        boolean includeMysql = launcherView.isQuickAppMysqlEnabled();
        boolean includePhp = launcherView.isQuickAppPhpEnabled();
        boolean includeMailpit = launcherView.isQuickAppMailpitEnabled();

        launcherView.setProvisioningApplyRunning(true);
        Task<ProvisioningApplySummary> task = new Task<>() {
            @Override
            protected ProvisioningApplySummary call() {
                return provisioningApplyDesktopService.applySummary(
                    projectCode,
                    projectName,
                    templateCode,
                    domain,
                    port,
                    webServer,
                    includeMysql,
                    includePhp,
                    includeMailpit,
                    mysqlPassword
                );
            }
        };

        task.setOnSucceeded(event -> {
            launcherView.setProvisioningApplyRunning(false);
            handleProvisioningApplyResult(task.getValue());
        });
        task.setOnFailed(event -> {
            launcherView.setProvisioningApplyRunning(false);
            ProvisioningApplySummary failed = ProvisioningApplySummary.empty(
                "Provisioning apply",
                task.getException() == null ? "unknown apply error" : task.getException().getMessage()
            );
            handleProvisioningApplyResult(failed);
        });

        Thread worker = new Thread(task, "jhoster-provisioning-apply");
        worker.setDaemon(true);
        worker.start();
    }

    private void handleProvisioningApplyResult(ProvisioningApplySummary applySummary) {
        appendProvisioningApplySummary(applySummary);
        if (!applySummary.isSuccess()) {
            if (launcherView.showProvisioningFailureDialog(applySummary)) {
                launcherView.showWorkflowPage();
                appendWorkflowSummary(webServerWorkflowDesktopService.listRunsSummary());
            }
            return;
        }
        refreshHostsAutoStatus();
    }

    private void appendProvisioningApplySummary(ProvisioningApplySummary summary) {
        launcherView.updateProvisioningApplySummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendWorkflowSummary(WorkflowDesktopSummary summary) {
        launcherView.updateWorkflowSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendPackageDownloadSummary(PackageDownloadSummary summary) {
        launcherView.appendPackageDownloadSummary(summary);
    }

    private void refreshLicenseStatus() {
        launcherView.appendLog(LOG_LICENSE_REFRESH);
        appendLicenseSummary(licenseDesktopService.currentSummary());
    }

    private void refreshHostsAutoStatus() {
        appendHostsAutoSummaryWithLog(LOG_HOSTS_AUTO_INSPECT, hostsAutoDesktopService.inspectSummary());
    }

    private void appendHostsAutoSummaryWithLog(String logTitle, HostsAutoSummary summary) {
        launcherView.appendLog(logTitle);
        launcherView.updateHostsAutoSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendLicenseSummary(LicensePlanSummary summary) {
        launcherView.updateLicensePlanSummary(summary);
        launcherView.appendLog(summary.toLogBlock());
    }

    private void appendHealthStatus() {
        boolean running = panelStatusService.isPanelRunning(DesktopApiConfig.resolveUrl(DesktopApiConfig.HEALTH_ROUTE));
        launcherView.appendLog(running ? LOG_AGENT_RUNNING : LOG_AGENT_STOPPED);
    }
}
