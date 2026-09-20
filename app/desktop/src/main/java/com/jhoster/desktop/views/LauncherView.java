// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\views\LauncherView.java
// # 📌 Amac: JHoster Desktop modern launcher ana gorunumunu olusturur
// # 📌 Modul - Java
// # Version: 3.77.0
// # Aciklama: Sol sidebar ana menu, temiz status topbar, Settings/Logs tablari ve calisan aksiyon odakli modern UI saglar
// # Bagimli Oldugu Katman: View

package com.jhoster.desktop.views;

import com.jhoster.desktop.config.DesktopApiConfig;
import com.jhoster.desktop.models.RuntimeManagerSummary;
import com.jhoster.desktop.models.QuickAppSummary;
import com.jhoster.desktop.models.PackageDownloadSummary;
import com.jhoster.desktop.models.ServiceManagerSummary;
import com.jhoster.desktop.models.DesktopServiceSelectionSettings;
import com.jhoster.desktop.models.WorkflowDesktopSummary;
import com.jhoster.desktop.models.LicensePlanSummary;
import com.jhoster.desktop.models.HostsAutoSummary;
import com.jhoster.desktop.tools.BrandingResourceTool;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.control.ButtonBar;
import javafx.scene.control.ButtonType;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ContextMenu;
import javafx.scene.control.Dialog;
import javafx.scene.control.RadioButton;
import javafx.scene.control.Label;
import javafx.scene.control.MenuItem;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.Separator;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import javafx.scene.image.ImageView;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.FlowPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.Region;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import java.util.Optional;

public class LauncherView {
    private static final String TITLE_TEXT = "JHoster";
    private static final String SUBTITLE_TEXT = "Local development control center";
    private static final String DASHBOARD_TITLE_TEXT = "Dashboard";
    private static final String DASHBOARD_SUBTITLE_TEXT = "Control and monitor your local development environment";
    private static final String PROFILE_BADGE_TEXT = "All systems operational";
    private static final String HERO_TITLE_TEXT = "JHoster Local Stack";
    private static final String HERO_SUBTITLE_TEXT = "Laragon style quick control for web server, database, mail catcher, terminal, www and unified workflow.";
    private static final String LOG_INITIAL_TEXT = "JHoster launcher ready.\n";
    private static final String COMPACT_TITLE_TEXT = "Local Stack";
    private static final String COMPACT_SUBTITLE_TEXT = "Start, stop, open and inspect your local development stack from one compact dashboard.";
    private static final String LABEL_COMPACT_SERVICES = "Services";
    private static final String LABEL_COMPACT_AGENT = "Agent";
    private static final String LABEL_COMPACT_WEB_PROFILE = "Web Profile";
    private static final String LABEL_COMPACT_ROOT = "Root";
    private static final String VALUE_COMPACT_AGENT = "127.0.0.1:8751";
    private static final String VALUE_COMPACT_WEB_PROFILE = "Apache / Nginx";
    private static final String VALUE_COMPACT_ROOT = "E:\\JHoster";
    private static final String META_APACHE = "2.4.x planned | 80/443";
    private static final String META_NGINX = "1.28.x planned | 80";
    private static final String META_MYSQL = "8.0.x planned | 3306";
    private static final String META_PHP = "8.x active | 9000";
    private static final String META_MAILPIT = "1.22.x planned | 1025/8025";
    private static final String DEV_MODE_BADGE_TEXT = "DEV MODE ACTIVE";
    private static final String DEV_MODE_NAV_TEXT = "Developer Tools";
    private static final String DEV_MODE_PAGE_TITLE = "Developer Tools";
    private static final String DEV_MODE_PAGE_SUBTITLE = "Raw agent endpoints, diagnostics and internal route shortcuts are visible only when Dev Mode is enabled at startup.";
    private static final String DEV_MODE_REQUIRED_TITLE = "Developer Mode Required";
    private static final String DEV_MODE_REQUIRED_TEXT = "Hold Shift while opening JHoster, use --dev, -Djhoster.dev=true, or JHOSTER_DEV_MODE=1 to show internal endpoint tools.";
    private static final String DEV_MODE_BANNER_TITLE = "Developer mode is active";
    private static final String DEV_MODE_BANNER_TEXT = "Internal agent endpoints, raw API shortcuts and diagnostics are visible in this session only. Normal startup hides these controls.";
    private static final String SIMPLE_MODE_MENU_TEXT = "Launchpad";
    private static final String SIMPLE_MODE_HINT_TEXT = "Menus moved to the left. Each section opens in a clean focused page.";
    private static final String DECK_TITLE_TEXT = "JHoster Desktop";
    private static final String DECK_VERSION_TEXT = "v3.77.0";
    private static final String DECK_EDITION_TEXT = "Community";
    private static final String LICENSE_DEFAULT_USAGE_TEXT = "Sites 0 / 5";
    private static final String LICENSE_DEFAULT_HINT_TEXT = "Community includes 5 active sites.";
    private static final String LICENSE_SETTINGS_TAB = "License";
    private static final String LICENSE_SETTINGS_TITLE = "JHoster License";
    private static final String LICENSE_SETTINGS_TEXT = "Community is free for up to 5 active sites. Pro unlocks unlimited active sites and advanced modules.";
    private static final String LICENSE_FEATURES_TITLE = "Feature Registry";
    private static final String LICENSE_FEATURE_SITE_LIMIT = "5 Active Sites";
    private static final String LICENSE_FEATURE_SITE_LIMIT_TEXT = "Community core limit for active local sites.";
    private static final String LICENSE_FEATURE_ADVANCED_SSL = "Advanced SSL";
    private static final String LICENSE_FEATURE_ADVANCED_SSL_TEXT = "Local certificate and advanced SSL automation.";
    private static final String LICENSE_FEATURE_AUTOMATED_BACKUP = "Automated Backup";
    private static final String LICENSE_FEATURE_AUTOMATED_BACKUP_TEXT = "Scheduled backup hooks for sites and config.";
    private static final String LICENSE_FEATURE_ADVANCED_DNS = "Advanced DNS";
    private static final String LICENSE_FEATURE_ADVANCED_DNS_TEXT = "Local DNS, aliases and host mapping workflow.";
    private static final String LICENSE_FEATURE_AI_OLLAMA = "AI / Ollama";
    private static final String LICENSE_FEATURE_AI_OLLAMA_TEXT = "Local AI helper and Ollama integration gate.";
    private static final String LICENSE_FEATURE_STATUS_INCLUDED = "Included";
    private static final String LICENSE_FEATURE_STATUS_PRO_LOCKED = "Pro Locked";
    private static final String DECK_SUBTITLE_TEXT = "Left menu local development control panel";
    private static final String LABEL_STACK_HEALTH = "Stack Health";
    private static final String LABEL_ACTIVE_ENGINE = "Active Engine";
    private static final String LABEL_PACKAGE_STATUS = "Package Status";
    private static final String LABEL_PACKAGE_CENTER = "Package Center";
    private static final String LABEL_PACKAGE_CENTER_READY = "Manifest downloader ready";
    private static final String LABEL_PACKAGE_CENTER_STACK = "Apache, Nginx, PHP, MySQL";
    private static final String LABEL_PACKAGE_CENTER_OPEN = "Open Package Center";
    private static final String LABEL_PACKAGE_CENTER_DIALOG_TITLE = "Package Center";
    private static final String LABEL_PACKAGE_CENTER_DIALOG_SUBTITLE = "Download, install and activate portable web stack packages from one focused screen.";
    private static final String LABEL_SERVICE_WEB_SERVER = "Web Server";
    private static final String LABEL_SWITCH_WEB_SERVER = "Engine ▾";
    private static final String VALUE_WEB_SERVER_PORTS = "80 / 443";
    private static final String VALUE_APACHE_DISPLAY = "Apache";
    private static final String VALUE_NGINX_DISPLAY = "Nginx";
    private static final String DEV_MODE_SETTINGS_TAB = "Developer";
    private static final String DEV_MODE_SETTINGS_TEXT = "Developer-only controls are isolated from the normal dashboard. Use this tab to inspect the local agent base URL and startup gates.";
    private static final String LABEL_STACK_PROFILE = "Stack Profile";
    private static final String LABEL_WORKSPACE_ROOT = "Workspace Root";
    private static final String LABEL_OVERALL_HEALTH = "Overall Health";
    private static final String VALUE_HEALTHY = "Healthy";
    private static final String VALUE_RUNNING = "Running";
    private static final String VALUE_HEALTH_PERCENT = "100%";
    private static final String TAB_OVERVIEW = "Overview";
    private static final String TAB_RUNTIME_VERSIONS = "Runtime Versions";
    private static final String TAB_QUICK_APP = "Quick App";
    private static final String TAB_WORKFLOW = "Workflow";
    private static final String TAB_DIAGNOSTICS = "Diagnostics";
    private static final String LABEL_ROLE = "Role";
    private static final String LABEL_VERSION = "Version";
    private static final String LABEL_PORTS = "Ports";
    private static final String LABEL_CONTROLS = "Controls";
    private static final String LABEL_MANAGE_ALL_SERVICES = "Manage all services >";
    private static final String LABEL_SYSTEM_OVERVIEW = "System Overview";
    private static final String LABEL_SYSTEM_SETTINGS = "System Settings >";
    private static final String LABEL_OS = "OS";
    private static final String LABEL_UPTIME = "Uptime";
    private static final String LABEL_WORKSPACE = "Workspace";
    private static final String LABEL_WEB_SERVER_MODE = "Web Server Mode";
    private static final String LABEL_SELECT_APACHE = "Use Apache";
    private static final String LABEL_SELECT_NGINX = "Use Nginx";
    private static final String VALUE_WEB_SERVER_APACHE = "apache";
    private static final String VALUE_WEB_SERVER_NGINX = "nginx";
    private static final String LABEL_SHARED_WWW = "Shared WWW";


    private static final String LABEL_QUICK_ACTION_BAR = "Quick Actions";
    private static final String LABEL_QUICK_ACTION_SUBTITLE = "Laragon style fast access for daily local development.";
    private static final String LABEL_QUICK_START_ALL = "Start All";
    private static final String LABEL_QUICK_STOP_ALL = "Stop All";
    private static final String LABEL_QUICK_WEB = "Web";
    private static final String LABEL_QUICK_DATABASE = "Database";
    private static final String LABEL_QUICK_MAILPIT = "Mailpit";
    private static final String LABEL_QUICK_TERMINAL = "Terminal";
    private static final String LABEL_QUICK_ROOT = "Root";
    private static final String LABEL_QUICK_PROJECTS = "Projects";
    private static final String LABEL_QUICK_LOGS = "Logs";
    private static final String LABEL_QUICK_BIN = "Bin";
    private static final String LABEL_QUICK_CMDER = "Cmder";
    private static final String LABEL_QUICK_GIT_BASH = "Git Bash";
    private static final String LABEL_QUICK_NOTEPAD = "Notepad++";
    private static final String LABEL_QUICK_NGROK = "Ngrok";
    private static final String LABEL_QUICK_COMPOSER = "Composer";
    private static final String LABEL_QUICK_YARN = "Yarn";
    private static final String LABEL_COMPACT_TOOLS = "Portable Tools";
    private static final String LABEL_COMPACT_TOOL_SUBTITLE = "Open portable tools from bin without leaving the dashboard.";

    private static final String LABEL_START_AGENT = "Start Agent";
    private static final String LABEL_STOP_AGENT = "Stop Agent";
    private static final String LABEL_RESTART_AGENT = "Restart Agent";
    private static final String LABEL_OPEN_PANEL = "Open Panel";
    private static final String LABEL_HEALTH = "Check Status";
    private static final String LABEL_COMPONENTS = "Components";
    private static final String LABEL_HISTORY = "History";
    private static final String LABEL_CACHE = "Cache";
    private static final String LABEL_APPS = "Apps";
    private static final String LABEL_PROCESS = "Process";
    private static final String LABEL_ADAPTERS = "Adapters";
    private static final String LABEL_LOCAL_PACKAGES = "Local Packages";
    private static final String LABEL_RUNTIME_VERSIONS = "Runtime Versions";
    private static final String LABEL_PROJECTS = "Projects";
    private static final String LABEL_VIRTUAL_HOSTS = "Virtual Hosts";
    private static final String LABEL_NGINX_RELOAD = "Nginx Reload";
    private static final String LABEL_NGINX_EXE = "Nginx Exe";
    private static final String LABEL_NGINX_REAL_TEST = "Nginx Real Test";
    private static final String LABEL_NGINX_REAL_RELOAD = "Nginx Real Reload";
    private static final String LABEL_NGINX_PREFLIGHT = "Nginx Preflight";
    private static final String LABEL_HOSTS_PUBLISH = "Hosts Publish";
    private static final String LABEL_HOSTS_APPLY = "Hosts Apply";
    private static final String LABEL_WEB_SERVERS = "Web Servers";
    private static final String LABEL_APACHE_VHOSTS = "Apache Vhosts";
    private static final String LABEL_APACHE_PUBLISH = "Apache Publish";
    private static final String LABEL_APACHE_VALIDATE = "Apache Validate";
    private static final String LABEL_APACHE_EXE = "Apache Exe";
    private static final String LABEL_APACHE_REAL_TEST = "Apache Real Test";
    private static final String LABEL_APACHE_REAL_RELOAD = "Apache Real Reload";
    private static final String LABEL_WORKFLOW_PROFILE = "Active Profile";
    private static final String LABEL_WORKFLOW_PLAN = "Plan Workflow";
    private static final String LABEL_WORKFLOW_DRY_RUN = "Dry Run Workflow";
    private static final String LABEL_WORKFLOW_RUNS = "Workflow Runs";
    private static final String LABEL_WORKFLOW_LOCKS = "Workflow Locks";
    private static final String LABEL_WORKFLOW_CARD = "Unified Workflow Bridge";
    private static final String LABEL_PROJECT_CODE = "Project Code";
    private static final String LABEL_DOMAIN = "Domain";
    private static final String LABEL_PORT = "Port";
    private static final String LABEL_TARGET_DIR = "Target Dir";
    private static final String LABEL_LOG_TITLE = "Activity Log";
    private static final String LABEL_SERVICE_MANAGER_CARD = "Service Manager";
    private static final String LABEL_SERVICE_MANAGER_SUBTITLE = "Safe state control for local Apache, Nginx, MySQL, PHP and Mailpit services.";
    private static final String LABEL_SERVICE_LIST = "Refresh Services";
    private static final String LABEL_SERVICE_STATUS = "Status";
    private static final String LABEL_SERVICE_PREFLIGHT = "Preflight";
    private static final String LABEL_SERVICE_START = "Start";
    private static final String LABEL_SERVICE_STOP = "Stop";
    private static final String LABEL_SERVICE_RESTART = "Restart";
    private static final String LABEL_SERVICE_APACHE = "Apache";
    private static final String LABEL_SERVICE_NGINX = "Nginx";
    private static final String LABEL_SERVICE_MYSQL = "MySQL";
    private static final String LABEL_SERVICE_PHP = "PHP";
    private static final String LABEL_SERVICE_MAILPIT = "Mailpit";
    private static final String LABEL_RUNTIME_MANAGER_CARD = "Portable Version Manager";
    private static final String LABEL_RUNTIME_MANAGER_SUBTITLE = "Laragon style version selection for web servers, database, PHP, Node, Python and cache services.";
    private static final String LABEL_RUNTIME_LIST = "Refresh Runtimes";
    private static final String LABEL_RUNTIME_SCAN_BIN = "Scan Bin";
    private static final String LABEL_RUNTIME_ACTIVE = "Active";
    private static final String LABEL_RUNTIME_ACTIVATE = "Activate";
    private static final String LABEL_RUNTIME_USE_FOLDER = "Use Folder";
    private static final String LABEL_RUNTIME_APACHE = "Apache";
    private static final String LABEL_RUNTIME_NGINX = "Nginx";
    private static final String LABEL_RUNTIME_MYSQL = "MySQL";
    private static final String LABEL_RUNTIME_PHP = "PHP";
    private static final String LABEL_RUNTIME_NODE = "Node";
    private static final String LABEL_RUNTIME_PYTHON = "Python";
    private static final String LABEL_RUNTIME_MEMCACHED = "Memcached";
    private static final String LABEL_RUNTIME_REDIS = "Redis";
    private static final String LABEL_RUNTIME_MAILPIT = "Mailpit";
    private static final String LABEL_PACKAGE_INSTALLER_CARD = "Package Downloader";
    private static final String LABEL_PACKAGE_INSTALLER_SUBTITLE = "Download portable runtimes and tools into cache, then install into bin folders.";
    private static final String LABEL_PACKAGE_CODE = "Package Code";
    private static final String LABEL_PACKAGE_CATALOG = "Refresh Catalog";
    private static final String LABEL_PACKAGE_PLAN = "Plan";
    private static final String LABEL_PACKAGE_DOWNLOAD = "Download";
    private static final String LABEL_PACKAGE_INSTALL = "Install";
    private static final String LABEL_RUNTIME_CODE = "Runtime Code";
    private static final String LABEL_RUNTIME_FOLDER = "Folder Name";
    private static final String LABEL_RUNTIME_COUNT = "Families";
    private static final String LABEL_RUNTIME_PHP_ACTIVE = "PHP Active";
    private static final String LABEL_RUNTIME_NODE_ACTIVE = "Node Active";
    private static final String LABEL_RUNTIME_PYTHON_ACTIVE = "Python Active";
    private static final String TAB_NEW_TEST_SITE = "New Site";
    private static final String NAV_NEW_SITE_TEXT = "New Site";
    private static final String LABEL_SITE_WIZARD_CARD = "Site Wizard";
    private static final String LABEL_SITE_WIZARD_SUBTITLE = "Project, local domain and hosts automation in one focused creation flow.";
    private static final String LABEL_SITE_WIZARD_BADGE = "Community Ready";
    private static final String LABEL_MODERN_HERO_BADGE = "Modern Command Center";
    private static final String LABEL_MODERN_HERO_TITLE = "Build local sites from one clean control center";
    private static final String LABEL_MODERN_HERO_SUBTITLE = "Choose the web server, database, PHP runtime and mail catcher before creating the site. JHoster keeps the domain, hosts file and workspace preview visible.";
    private static final String LABEL_MODERN_HERO_STEP_STACK = "1. Stack";
    private static final String LABEL_MODERN_HERO_STEP_DOMAIN = "2. Domain";
    private static final String LABEL_MODERN_HERO_STEP_CREATE = "3. Create";
    private static final String LABEL_MODERN_STATUS_TITLE = "Environment Snapshot";
    private static final String LABEL_MODERN_STATUS_SUBTITLE = "Fast read for the active local stack.";
    private static final String LABEL_MODERN_STATUS_ACTIVE_PLAN = "Plan";
    private static final String LABEL_MODERN_STATUS_ACTIVE_SITES = "Sites";
    private static final String LABEL_MODERN_STATUS_HOSTS = "Hosts";
    private static final String LABEL_MODERN_STATUS_STACK = "Default Stack";
    private static final String LABEL_MODERN_STACK_PRESET_TITLE = "Recommended Preset";
    private static final String LABEL_MODERN_STACK_PRESET_TEXT = "Apache + MySQL + PHP + Mailpit is best for OpenCart, WordPress and classic PHP testing.";
    private static final String LABEL_MODERN_PACKAGE_TITLE = "Portable Runtime Layer";
    private static final String LABEL_MODERN_PACKAGE_TEXT = "Keep Apache, Nginx, PHP, MySQL and tools versioned under bin/ without touching the system install.";
    private static final String LABEL_SITE_WIZARD_STEP_PROJECT = "Project";
    private static final String LABEL_SITE_WIZARD_STEP_PROJECT_TEXT = "Choose the project code, display name and template.";
    private static final String LABEL_SITE_WIZARD_STEP_DOMAIN = "Domain";
    private static final String LABEL_SITE_WIZARD_STEP_DOMAIN_TEXT = "Preview the local URL and keep hosts automation visible.";
    private static final String LABEL_SITE_WIZARD_STEP_CREATE = "Create";
    private static final String LABEL_SITE_WIZARD_STEP_CREATE_TEXT = "Plan first, then create the test site when the setup is ready.";
    private static final String LABEL_SITE_WIZARD_URL_PREVIEW = "Local URL";
    private static final String LABEL_SITE_WIZARD_FOLDER_PREVIEW = "Project Folder";
    private static final String LABEL_SITE_WIZARD_HOSTS_PREVIEW = "Hosts Mode";
    private static final String VALUE_SITE_WIZARD_DEFAULT_URL = "http://demo-quick-app.test:80";
    private static final String VALUE_SITE_WIZARD_DEFAULT_FOLDER = "www\\demo-quick-app";
    private static final String VALUE_SITE_WIZARD_HOSTS_AUTO = "JHoster Managed";
    private static final String VALUE_SITE_WIZARD_STEP_ONE = "1";
    private static final String VALUE_SITE_WIZARD_STEP_TWO = "2";
    private static final String VALUE_SITE_WIZARD_STEP_THREE = "3";
    private static final String LABEL_QUICK_APP_CARD = "Create New Local Site";
    private static final String LABEL_QUICK_APP_SUBTITLE = "Create a local site with project folder, runtime template, domain, selected stack and automatic hosts mapping.";
    private static final String LABEL_QUICK_APP_TEMPLATES = "Templates";
    private static final String LABEL_QUICK_APP_PLAN = "Plan Site";
    private static final String LABEL_QUICK_APP_CREATE = "Create Test Site";
    private static final String LABEL_QUICK_APP_PROJECT_CODE = "Project Code";
    private static final String LABEL_QUICK_APP_PROJECT_NAME = "Project Name";
    private static final String LABEL_QUICK_APP_TEMPLATE_CODE = "Template Code";
    private static final String LABEL_QUICK_APP_DOMAIN = "Local Domain";
    private static final String LABEL_QUICK_APP_PORT = "Web Port";
    private static final String LABEL_QUICK_APP_STACK = "Stack";
    private static final String LABEL_QUICK_APP_WEB_SERVER = "Web Server";
    private static final String LABEL_QUICK_APP_USE_APACHE = "Apache";
    private static final String LABEL_QUICK_APP_USE_NGINX = "Nginx";
    private static final String LABEL_QUICK_APP_INCLUDE_MYSQL = "MySQL";
    private static final String LABEL_QUICK_APP_INCLUDE_PHP = "PHP";
    private static final String LABEL_QUICK_APP_INCLUDE_MAILPIT = "Mailpit";
    private static final String LABEL_QUICK_APP_STACK_HINT = "Choose the web server and services before creating the site. The selected stack is stored in plan/create metadata and project registry.";
    private static final String LABEL_SITE_WIZARD_STACK_PREVIEW = "Selected Stack";
    private static final String LABEL_QUICK_APP_TEMPLATE_COUNT = "Templates";
    private static final String LABEL_QUICK_APP_LAST_PROJECT = "Last Project";
    private static final String LABEL_QUICK_APP_LAST_TEMPLATE = "Last Template";
    private static final String LABEL_QUICK_APP_LAST_STATUS = "Status";
    private static final String LABEL_QUICK_APP_HOSTS_AUTO = "Auto Hosts: writes domain.test to the JHoster managed hosts block when JHoster runs as admin.";
    private static final String LABEL_HOSTS_AUTO_CARD = "Hosts Auto";
    private static final String LABEL_HOSTS_AUTO_SUBTITLE = "Inspect and repair the JHoster managed Windows hosts block without touching Docker, Laragon or manual lines.";
    private static final String LABEL_HOSTS_AUTO_STATUS = "Hosts";
    private static final String LABEL_HOSTS_AUTO_MANAGED = "Managed";
    private static final String LABEL_HOSTS_AUTO_ISSUES = "Issues";
    private static final String LABEL_HOSTS_AUTO_MESSAGE = "Message";
    private static final String LABEL_HOSTS_AUTO_TARGET = "Target File";
    private static final String LABEL_HOSTS_AUTO_MODE = "Apply Mode";
    private static final String LABEL_HOSTS_AUTO_INSPECT = "Inspect Hosts";
    private static final String LABEL_HOSTS_AUTO_REPAIR_PLAN = "Repair Plan";
    private static final String LABEL_HOSTS_AUTO_REPAIR = "Repair Hosts";
    private static final String LABEL_HOSTS_AUTO_SETTINGS_TAB = "Hosts";
    private static final String VALUE_HOSTS_AUTO_NOT_CHECKED = "Not Checked";
    private static final String LABEL_SERVICE_APACHE_STATUS = "Apache";
    private static final String LABEL_SERVICE_NGINX_STATUS = "Nginx";
    private static final String LABEL_SERVICE_MYSQL_STATUS = "MySQL";
    private static final String LABEL_SERVICE_PHP_STATUS = "PHP";
    private static final String LABEL_SERVICE_MAILPIT_STATUS = "Mailpit";
    private static final String LABEL_SUMMARY_PROFILE = "Profile";
    private static final String LABEL_SUMMARY_STATUS = "Status";
    private static final String LABEL_SUMMARY_RUN_COUNT = "Run Count";
    private static final String LABEL_SUMMARY_LOCK_COUNT = "Locks";
    private static final String LABEL_SUMMARY_STEP_COUNT = "Steps";
    private static final String LABEL_SUMMARY_RUN_ID = "Last Run";
    private static final String SUMMARY_VALUE_EMPTY = "-";
    private static final String SUMMARY_RUNS_TITLE = "Workflow runs";
    private static final String SUMMARY_LOCKS_TITLE = "Workflow locks";
    private static final int RUN_ID_MAX_VISIBLE_LENGTH = 28;


    private static final String STYLE_ROOT = "jhoster-root";
    private static final String STYLE_SIDEBAR = "jhoster-sidebar";
    private static final String STYLE_BRAND_MARK = "jhoster-brand-mark";
    private static final String STYLE_BRAND_TITLE = "jhoster-brand-title";
    private static final String STYLE_BRAND_SUBTITLE = "jhoster-brand-subtitle";
    private static final String STYLE_SIDEBAR_GROUP = "jhoster-sidebar-group";
    private static final String STYLE_SIDEBAR_TITLE = "jhoster-sidebar-title";
    private static final String STYLE_NAV_BUTTON = "jhoster-nav-button";
    private static final String STYLE_CONTENT = "jhoster-content";
    private static final String STYLE_TOPBAR = "jhoster-topbar";
    private static final String STYLE_BADGE = "jhoster-badge";
    private static final String STYLE_PREMIUM_BADGE = "jhoster-premium-badge";
    private static final String STYLE_HERO = "jhoster-hero";
    private static final String STYLE_HERO_TITLE = "jhoster-hero-title";
    private static final String STYLE_HERO_SUBTITLE = "jhoster-hero-subtitle";
    private static final String STYLE_PRIMARY_BUTTON = "jhoster-primary-button";
    private static final String STYLE_SECONDARY_BUTTON = "jhoster-secondary-button";
    private static final String STYLE_CARD = "jhoster-card";
    private static final String STYLE_CARD_TITLE = "jhoster-card-title";
    private static final String STYLE_CARD_TEXT = "jhoster-card-text";
    private static final String STYLE_LINK_BUTTON = "jhoster-link-button";
    private static final String STYLE_ACTION_GRID = "jhoster-action-grid";
    private static final String STYLE_ACTION_BUTTON = "jhoster-action-button";
    private static final String STYLE_DANGER_BUTTON = "jhoster-danger-button";
    private static final String STYLE_LOG = "jhoster-log";
    private static final String STYLE_SECTION_TITLE = "jhoster-section-title";
    private static final String STYLE_FIELD_LABEL = "jhoster-field-label";
    private static final String STYLE_INPUT = "jhoster-input";
    private static final String STYLE_FORM_GRID = "jhoster-form-grid";
    private static final String STYLE_SUMMARY_STRIP = "jhoster-summary-strip";
    private static final String STYLE_SUMMARY_PILL = "jhoster-summary-pill";
    private static final String STYLE_SUMMARY_LABEL = "jhoster-summary-label";
    private static final String STYLE_SUMMARY_VALUE = "jhoster-summary-value";
    private static final String STYLE_COMPACT_DASHBOARD = "jhoster-compact-dashboard";
    private static final String STYLE_COMPACT_HEADER = "jhoster-compact-header";
    private static final String STYLE_COMPACT_TITLE = "jhoster-compact-title";
    private static final String STYLE_COMPACT_SUBTITLE = "jhoster-compact-subtitle";
    private static final String STYLE_COMPACT_GRID = "jhoster-compact-grid";
    private static final String STYLE_COMPACT_SERVICE_PANEL = "jhoster-compact-service-panel";
    private static final String STYLE_COMPACT_SERVICE_ROW = "jhoster-compact-service-row";
    private static final String STYLE_COMPACT_SERVICE_DOT = "jhoster-compact-service-dot";
    private static final String STYLE_COMPACT_SERVICE_NAME = "jhoster-compact-service-name";
    private static final String STYLE_COMPACT_SERVICE_META = "jhoster-compact-service-meta";
    private static final String STYLE_COMPACT_SERVICE_STATUS = "jhoster-compact-service-status";
    private static final String STYLE_COMPACT_SERVICE_ACTIONS = "jhoster-compact-service-actions";
    private static final String STYLE_COMPACT_SERVICE_START = "jhoster-compact-service-start";
    private static final String STYLE_COMPACT_SERVICE_STOP = "jhoster-compact-service-stop";
    private static final String STYLE_COMPACT_SERVICE_RESTART = "jhoster-compact-service-restart";
    private static final String STYLE_COMPACT_QUICK_DOCK = "jhoster-compact-quick-dock";
    private static final String STYLE_COMPACT_TOOL_DOCK = "jhoster-compact-tool-dock";
    private static final String STYLE_SEARCH_BOX = "jhoster-search-box";
    private static final String STYLE_SEARCH_FIELD = "jhoster-search-field";
    private static final String STYLE_SHORTCUT_BADGE = "jhoster-shortcut-badge";
    private static final String STYLE_HEADER_ICON = "jhoster-header-icon";
    private static final String STYLE_PROFILE_PILL = "jhoster-profile-pill";
    private static final String STYLE_SIDEBAR_ACTIVE = "jhoster-sidebar-active";
    private static final String STYLE_SIDEBAR_FOOTER = "jhoster-sidebar-footer";
    private static final String STYLE_DASHBOARD_METRIC = "jhoster-dashboard-metric";
    private static final String STYLE_METRIC_ICON = "jhoster-metric-icon";
    private static final String STYLE_STATUS_PILL = "jhoster-status-pill";
    private static final String STYLE_DASHBOARD_TABS = "jhoster-dashboard-tabs";
    private static final String STYLE_DASHBOARD_TAB = "jhoster-dashboard-tab";
    private static final String STYLE_DASHBOARD_TAB_ACTIVE = "jhoster-dashboard-tab-active";
    private static final String STYLE_SERVICE_TABLE = "jhoster-service-table";
    private static final String STYLE_SERVICE_HEADER_ROW = "jhoster-service-header-row";
    private static final String STYLE_SERVICE_TABLE_ROW = "jhoster-service-table-row";
    private static final String STYLE_SERVICE_ICON = "jhoster-service-icon";
    private static final String STYLE_SERVICE_COL = "jhoster-service-col";
    private static final String STYLE_BOTTOM_GRID = "jhoster-bottom-grid";
    private static final String STYLE_QUICK_TILE = "jhoster-quick-tile";
    private static final String STYLE_INFO_ROW = "jhoster-info-row";
    private static final String STYLE_DASHBOARD_BODY = "jhoster-dashboard-body";
    private static final String STYLE_PAGE_HEADER = "jhoster-page-header";
    private static final String STYLE_PAGE_SUBTITLE = "jhoster-page-subtitle";
    private static final String STYLE_SETTINGS_DIALOG = "jhoster-settings-dialog";
    private static final String STYLE_SETTINGS_ROW = "jhoster-settings-row";
    private static final String STYLE_SETTINGS_PORT = "jhoster-settings-port";
    private static final String STYLE_DEV_BADGE = "jhoster-dev-badge";
    private static final String STYLE_DEV_CARD = "jhoster-dev-card";
    private static final String STYLE_DEV_SIDEBAR_GROUP = "jhoster-dev-sidebar-group";
    private static final String STYLE_DEV_SIDEBAR_BUTTON = "jhoster-dev-sidebar-button";
    private static final String STYLE_DEV_FOOTER = "jhoster-dev-footer";
    private static final String STYLE_DEV_BANNER = "jhoster-dev-banner";
    private static final String STYLE_DEV_NOTICE_TITLE = "jhoster-dev-notice-title";
    private static final String STYLE_DEV_NOTICE_TEXT = "jhoster-dev-notice-text";
    private static final String STYLE_LICENSE_FEATURE_GRID = "jhoster-license-feature-grid";
    private static final String STYLE_LICENSE_FEATURE_ROW = "jhoster-license-feature-row";
    private static final String STYLE_LICENSE_FEATURE_NAME = "jhoster-license-feature-name";
    private static final String STYLE_LICENSE_FEATURE_STATUS = "jhoster-license-feature-status";
    private static final String STYLE_LICENSE_FEATURE_STATUS_LOCKED = "jhoster-license-feature-status-locked";
    private static final String STYLE_HOSTS_AUTO_STATUS = "jhoster-hosts-auto-status";
    private static final String STYLE_HOSTS_AUTO_STATUS_WARNING = "jhoster-hosts-auto-status-warning";
    private static final String STYLE_HOSTS_AUTO_STATUS_OK = "jhoster-hosts-auto-status-ok";
    private static final String STYLE_HOSTS_AUTO_GRID = "jhoster-hosts-auto-grid";
    private static final String STYLE_SITE_WIZARD_LAYOUT = "jhoster-site-wizard-layout";
    private static final String STYLE_SITE_WIZARD_MAIN = "jhoster-site-wizard-main";
    private static final String STYLE_SITE_WIZARD_PREVIEW = "jhoster-site-wizard-preview";
    private static final String STYLE_SITE_WIZARD_STEP = "jhoster-site-wizard-step";
    private static final String STYLE_SITE_WIZARD_STEP_BADGE = "jhoster-site-wizard-step-badge";
    private static final String STYLE_SITE_WIZARD_PREVIEW_CARD = "jhoster-site-wizard-preview-card";
    private static final String STYLE_FULLSCREEN_STACK = "jhoster-fullscreen-stack";
    private static final String STYLE_STACK_SELECTOR = "jhoster-stack-selector";
    private static final String STYLE_MODERN_HERO_SHELL = "jhoster-modern-hero-shell";
    private static final String STYLE_MODERN_HERO_CARD = "jhoster-modern-hero-card";
    private static final String STYLE_MODERN_HERO_BADGE = "jhoster-modern-hero-badge";
    private static final String STYLE_MODERN_HERO_TITLE = "jhoster-modern-hero-title";
    private static final String STYLE_MODERN_HERO_SUBTITLE = "jhoster-modern-hero-subtitle";
    private static final String STYLE_MODERN_FLOW_ROW = "jhoster-modern-flow-row";
    private static final String STYLE_MODERN_FLOW_PILL = "jhoster-modern-flow-pill";
    private static final String STYLE_MODERN_STATUS_RAIL = "jhoster-modern-status-rail";
    private static final String STYLE_MODERN_STATUS_CARD = "jhoster-modern-status-card";
    private static final String STYLE_MODERN_STATUS_TITLE = "jhoster-modern-status-title";
    private static final String STYLE_MODERN_STATUS_VALUE = "jhoster-modern-status-value";
    private static final String STYLE_MODERN_PRESET_CARD = "jhoster-modern-preset-card";
    private static final String STYLE_STACK_OPTION = "jhoster-stack-option";
    private static final String STYLE_STACK_HINT = "jhoster-stack-hint";


    private final Button navDashboardButton = new Button(DASHBOARD_TITLE_TEXT);
    private final Button navNewSiteButton = new Button(NAV_NEW_SITE_TEXT);
    private final Button navServicesButton = new Button(LABEL_SERVICE_MANAGER_CARD);
    private final Button navProjectsButton = new Button(LABEL_PROJECTS);
    private final Button navVirtualHostsButton = new Button(LABEL_VIRTUAL_HOSTS);
    private final Button navAppsButton = new Button(LABEL_APPS);
    private final Button navVersionsButton = new Button(LABEL_RUNTIME_VERSIONS);
    private final Button navWorkflowButton = new Button(LABEL_WORKFLOW_CARD);
    private final Button navToolsButton = new Button(LABEL_COMPACT_TOOLS);
    private final Button navLogsButton = new Button(LABEL_LOG_TITLE);
    private final Button navDeveloperButton = new Button(DEV_MODE_NAV_TEXT);
    private final Button navSettingsButton = new Button("Settings");
    private final Label topbarPlanValue = new Label(DECK_EDITION_TEXT);
    private final Label topbarSitesValue = new Label(LICENSE_DEFAULT_USAGE_TEXT);
    private final Label topbarHostsValue = new Label(VALUE_HOSTS_AUTO_NOT_CHECKED);
    private final Label topbarEngineValue = new Label(VALUE_APACHE_DISPLAY);
    private final Label licenseBadgeLabel = new Label(DECK_EDITION_TEXT);
    private final Label licenseUsageLabel = new Label(LICENSE_DEFAULT_USAGE_TEXT);
    private final Label licenseHintLabel = new Label(LICENSE_DEFAULT_HINT_TEXT);
    private final Label licenseSiteLimitStatusLabel = new Label(LICENSE_FEATURE_STATUS_INCLUDED);
    private final Label licenseAdvancedSslStatusLabel = new Label(LICENSE_FEATURE_STATUS_PRO_LOCKED);
    private final Label licenseAutomatedBackupStatusLabel = new Label(LICENSE_FEATURE_STATUS_PRO_LOCKED);
    private final Label licenseAdvancedDnsStatusLabel = new Label(LICENSE_FEATURE_STATUS_PRO_LOCKED);
    private final Label licenseAiOllamaStatusLabel = new Label(LICENSE_FEATURE_STATUS_PRO_LOCKED);
    private final Label hostsAutoHealthValue = new Label(VALUE_HOSTS_AUTO_NOT_CHECKED);
    private final Label hostsAutoManagedValue = new Label("0 / 0");
    private final Label hostsAutoIssuesValue = new Label("0");
    private final Label hostsAutoMessageValue = new Label("Hosts auto not checked yet.");
    private final Label hostsAutoTargetValue = new Label("-");
    private final Label hostsAutoModeValue = new Label("-");
    private final Label quickHostsAutoHealthValue = new Label(VALUE_HOSTS_AUTO_NOT_CHECKED);
    private final Label settingsHostsAutoHealthValue = new Label(VALUE_HOSTS_AUTO_NOT_CHECKED);
    private final Label settingsHostsAutoManagedValue = new Label("0 / 0");
    private final Label settingsHostsAutoIssuesValue = new Label("0");
    private final Label settingsHostsAutoMessageValue = new Label("Hosts auto not checked yet.");
    private final Label settingsHostsAutoTargetValue = new Label("-");
    private final Label settingsHostsAutoModeValue = new Label("-");
    private final Label siteWizardUrlPreviewValue = new Label(VALUE_SITE_WIZARD_DEFAULT_URL);
    private final Label siteWizardFolderPreviewValue = new Label(VALUE_SITE_WIZARD_DEFAULT_FOLDER);
    private final Label siteWizardStackPreviewValue = new Label("Apache + MySQL + PHP");
    private final Label siteWizardHostsStatusPreviewValue = new Label(VALUE_HOSTS_AUTO_NOT_CHECKED);
    private final Label siteWizardHostsIssuesPreviewValue = new Label("0");
    private final Button quickHostsAutoInspectButton = new Button(LABEL_HOSTS_AUTO_INSPECT);
    private final Button settingsHostsAutoInspectButton = new Button(LABEL_HOSTS_AUTO_INSPECT);
    private final Button settingsHostsAutoRepairPlanButton = new Button(LABEL_HOSTS_AUTO_REPAIR_PLAN);
    private final Button settingsHostsAutoRepairButton = new Button(LABEL_HOSTS_AUTO_REPAIR);
    private final Button overviewTabButton = new Button(TAB_OVERVIEW);
    private final Button runtimeVersionsTabButton = new Button(TAB_RUNTIME_VERSIONS);
    private final Button quickAppTabButton = new Button(TAB_QUICK_APP);
    private final Button workflowTabButton = new Button(TAB_WORKFLOW);
    private final Button diagnosticsTabButton = new Button(TAB_DIAGNOSTICS);
    private final Button manageServicesButton = new Button(LABEL_MANAGE_ALL_SERVICES);
    private final Button viewAllLogsButton = new Button("View all logs >");
    private final Button systemSettingsButton = new Button(LABEL_SYSTEM_SETTINGS);
    private final Button startAgentButton = new Button(LABEL_START_AGENT);
    private final Button stopAgentButton = new Button(LABEL_STOP_AGENT);
    private final Button restartAgentButton = new Button(LABEL_RESTART_AGENT);
    private final Button openPanelButton = new Button(LABEL_OPEN_PANEL);
    private final Button openComponentsButton = new Button(LABEL_COMPONENTS);
    private final Button openHistoryButton = new Button(LABEL_HISTORY);
    private final Button openCacheButton = new Button(LABEL_CACHE);
    private final Button openAppsButton = new Button(LABEL_APPS);
    private final Button openProcessButton = new Button(LABEL_PROCESS);
    private final Button openServiceAdaptersButton = new Button(LABEL_ADAPTERS);
    private final Button openLocalPackagesButton = new Button(LABEL_LOCAL_PACKAGES);
    private final Button openRuntimeVersionsButton = new Button(LABEL_RUNTIME_VERSIONS);
    private final Button openProjectsButton = new Button(LABEL_PROJECTS);
    private final Button openVirtualHostsButton = new Button(LABEL_VIRTUAL_HOSTS);
    private final Button openNginxReloadButton = new Button(LABEL_NGINX_RELOAD);
    private final Button openNginxExecutableButton = new Button(LABEL_NGINX_EXE);
    private final Button openNginxRealValidateButton = new Button(LABEL_NGINX_REAL_TEST);
    private final Button openNginxRealReloadButton = new Button(LABEL_NGINX_REAL_RELOAD);
    private final Button openNginxPreflightButton = new Button(LABEL_NGINX_PREFLIGHT);
    private final Button openHostsPublishButton = new Button(LABEL_HOSTS_PUBLISH);
    private final Button openHostsApplyButton = new Button(LABEL_HOSTS_APPLY);
    private final Button openWebServerProfilesButton = new Button(LABEL_WEB_SERVERS);
    private final Button openApacheVhostsButton = new Button(LABEL_APACHE_VHOSTS);
    private final Button openApachePublishButton = new Button(LABEL_APACHE_PUBLISH);
    private final Button openApacheValidateButton = new Button(LABEL_APACHE_VALIDATE);
    private final Button openApacheExecutableButton = new Button(LABEL_APACHE_EXE);
    private final Button openApacheRealValidateButton = new Button(LABEL_APACHE_REAL_TEST);
    private final Button openApacheRealReloadButton = new Button(LABEL_APACHE_REAL_RELOAD);
    private final Button serviceListButton = new Button(LABEL_SERVICE_LIST);
    private final Button compactServiceRefreshButton = new Button(LABEL_SERVICE_LIST);
    private final Button apacheStatusButton = new Button(LABEL_SERVICE_STATUS);
    private final Button apachePreflightButton = new Button(LABEL_SERVICE_PREFLIGHT);
    private final Button apacheStartButton = new Button(LABEL_SERVICE_START);
    private final Button apacheStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button apacheRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button nginxStatusButton = new Button(LABEL_SERVICE_STATUS);
    private final Button nginxPreflightButton = new Button(LABEL_SERVICE_PREFLIGHT);
    private final Button nginxStartButton = new Button(LABEL_SERVICE_START);
    private final Button nginxStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button nginxRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button mysqlStatusButton = new Button(LABEL_SERVICE_STATUS);
    private final Button mysqlPreflightButton = new Button(LABEL_SERVICE_PREFLIGHT);
    private final Button mysqlStartButton = new Button(LABEL_SERVICE_START);
    private final Button mysqlStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button mysqlRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button phpStatusButton = new Button(LABEL_SERVICE_STATUS);
    private final Button phpPreflightButton = new Button(LABEL_SERVICE_PREFLIGHT);
    private final Button phpStartButton = new Button(LABEL_SERVICE_START);
    private final Button phpStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button phpRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button mailpitStatusButton = new Button(LABEL_SERVICE_STATUS);
    private final Button mailpitPreflightButton = new Button(LABEL_SERVICE_PREFLIGHT);
    private final Button mailpitStartButton = new Button(LABEL_SERVICE_START);
    private final Button mailpitStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button mailpitRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button runtimeListButton = new Button(LABEL_RUNTIME_LIST);
    private final Button runtimeScanBinButton = new Button(LABEL_RUNTIME_SCAN_BIN);
    private final Button runtimeApacheActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeApacheActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeApacheActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeNginxActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeNginxActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeNginxActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeMysqlActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeMysqlActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeMysqlActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimePhpActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimePhpActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimePhpActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeNodeActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeNodeActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeNodeActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimePythonActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimePythonActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimePythonActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeMemcachedActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeMemcachedActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeMemcachedActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeRedisActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeRedisActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeRedisActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button runtimeMailpitActiveButton = new Button(LABEL_RUNTIME_ACTIVE);
    private final Button runtimeMailpitActivateButton = new Button(LABEL_RUNTIME_ACTIVATE);
    private final Button runtimeMailpitActivatePortableButton = new Button(LABEL_RUNTIME_USE_FOLDER);
    private final Button quickAppTemplatesButton = new Button(LABEL_QUICK_APP_TEMPLATES);
    private final Button quickAppPlanButton = new Button(LABEL_QUICK_APP_PLAN);
    private final Button quickAppCreateButton = new Button(LABEL_QUICK_APP_CREATE);
    private final Button workflowProfileButton = new Button(LABEL_WORKFLOW_PROFILE);
    private final Button workflowPlanButton = new Button(LABEL_WORKFLOW_PLAN);
    private final Button workflowDryRunButton = new Button(LABEL_WORKFLOW_DRY_RUN);
    private final Button workflowRunsButton = new Button(LABEL_WORKFLOW_RUNS);
    private final Button workflowLocksButton = new Button(LABEL_WORKFLOW_LOCKS);
    private final Button checkStatusButton = new Button(LABEL_HEALTH);
    private final Button quickStartAllButton = new Button(LABEL_QUICK_START_ALL);
    private final Button quickStopAllButton = new Button(LABEL_QUICK_STOP_ALL);
    private final Button quickWebButton = new Button(LABEL_QUICK_WEB);
    private final Button quickDatabaseButton = new Button(LABEL_QUICK_DATABASE);
    private final Button quickMailpitButton = new Button(LABEL_QUICK_MAILPIT);
    private final Button quickTerminalButton = new Button(LABEL_QUICK_TERMINAL);
    private final Button quickRootButton = new Button(LABEL_QUICK_ROOT);
    private final Button quickProjectsButton = new Button(LABEL_QUICK_PROJECTS);
    private final Button quickLogsButton = new Button(LABEL_QUICK_LOGS);
    private final Button quickBinButton = new Button(LABEL_QUICK_BIN);
    private final Button quickCmderButton = new Button(LABEL_QUICK_CMDER);
    private final Button quickGitBashButton = new Button(LABEL_QUICK_GIT_BASH);
    private final Button quickNotepadButton = new Button(LABEL_QUICK_NOTEPAD);
    private final Button quickNgrokButton = new Button(LABEL_QUICK_NGROK);
    private final Button quickComposerButton = new Button(LABEL_QUICK_COMPOSER);
    private final Button quickYarnButton = new Button(LABEL_QUICK_YARN);
    private final Button selectApacheWebServerButton = new Button(LABEL_SELECT_APACHE);
    private final Button selectNginxWebServerButton = new Button(LABEL_SELECT_NGINX);
    private String activeWebServerCode = VALUE_WEB_SERVER_APACHE;
    private final Label activeWebServerValue = new Label(VALUE_APACHE_DISPLAY);
    private final Label simpleWebServerNameValue = new Label(VALUE_APACHE_DISPLAY);
    private final Label simpleWebServerStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Button simpleWebServerStartButton = new Button(LABEL_SERVICE_START);
    private final Button simpleWebServerStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button simpleWebServerRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button simpleWebServerSwitchButton = new Button(LABEL_SWITCH_WEB_SERVER);
    private final Label serviceApacheStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label serviceNginxStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label serviceMysqlStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label servicePhpStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label serviceMailpitStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label compactApacheStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label compactNginxStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label compactMysqlStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label compactPhpStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label compactMailpitStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Button compactApacheStartButton = new Button(LABEL_SERVICE_START);
    private final Button compactApacheStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button compactApacheRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button compactNginxStartButton = new Button(LABEL_SERVICE_START);
    private final Button compactNginxStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button compactNginxRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button compactMysqlStartButton = new Button(LABEL_SERVICE_START);
    private final Button compactMysqlStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button compactMysqlRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button compactPhpStartButton = new Button(LABEL_SERVICE_START);
    private final Button compactPhpStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button compactPhpRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Button compactMailpitStartButton = new Button(LABEL_SERVICE_START);
    private final Button compactMailpitStopButton = new Button(LABEL_SERVICE_STOP);
    private final Button compactMailpitRestartButton = new Button(LABEL_SERVICE_RESTART);
    private final Label runtimeCountValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label runtimePhpActiveValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label runtimeNodeActiveValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label runtimePythonActiveValue = new Label(SUMMARY_VALUE_EMPTY);
    private final TextField runtimeApacheCodeField = new TextField(DesktopApiConfig.DEFAULT_APACHE_RUNTIME_CODE);
    private final TextField runtimeNginxCodeField = new TextField(DesktopApiConfig.DEFAULT_NGINX_RUNTIME_CODE);
    private final TextField runtimeMysqlCodeField = new TextField(DesktopApiConfig.DEFAULT_MYSQL_RUNTIME_CODE);
    private final TextField runtimePhpCodeField = new TextField(DesktopApiConfig.DEFAULT_PHP_RUNTIME_CODE);
    private final TextField runtimeNodeCodeField = new TextField(DesktopApiConfig.DEFAULT_NODE_RUNTIME_CODE);
    private final TextField runtimePythonCodeField = new TextField(DesktopApiConfig.DEFAULT_PYTHON_RUNTIME_CODE);
    private final TextField runtimeMemcachedCodeField = new TextField(DesktopApiConfig.DEFAULT_MEMCACHED_RUNTIME_CODE);
    private final TextField runtimeRedisCodeField = new TextField(DesktopApiConfig.DEFAULT_REDIS_RUNTIME_CODE);
    private final TextField runtimeMailpitCodeField = new TextField(DesktopApiConfig.DEFAULT_MAILPIT_RUNTIME_CODE);
    private final TextField runtimeApacheFolderField = new TextField(DesktopApiConfig.DEFAULT_APACHE_RUNTIME_FOLDER);
    private final TextField runtimeNginxFolderField = new TextField(DesktopApiConfig.DEFAULT_NGINX_RUNTIME_FOLDER);
    private final TextField runtimeMysqlFolderField = new TextField(DesktopApiConfig.DEFAULT_MYSQL_RUNTIME_FOLDER);
    private final TextField runtimePhpFolderField = new TextField(DesktopApiConfig.DEFAULT_PHP_RUNTIME_FOLDER);
    private final TextField runtimeNodeFolderField = new TextField(DesktopApiConfig.DEFAULT_NODE_RUNTIME_FOLDER);
    private final TextField runtimePythonFolderField = new TextField(DesktopApiConfig.DEFAULT_PYTHON_RUNTIME_FOLDER);
    private final TextField runtimeMemcachedFolderField = new TextField(DesktopApiConfig.DEFAULT_MEMCACHED_RUNTIME_FOLDER);
    private final TextField runtimeRedisFolderField = new TextField(DesktopApiConfig.DEFAULT_REDIS_RUNTIME_FOLDER);
    private final TextField runtimeMailpitFolderField = new TextField(DesktopApiConfig.DEFAULT_MAILPIT_RUNTIME_FOLDER);
    private final TextField packageCodeField = new TextField(DesktopApiConfig.DEFAULT_PACKAGE_DOWNLOAD_CODE);
    private final Button packageCatalogButton = new Button(LABEL_PACKAGE_CATALOG);
    private final Button packagePlanButton = new Button(LABEL_PACKAGE_PLAN);
    private final Button packageDownloadButton = new Button(LABEL_PACKAGE_DOWNLOAD);
    private final Button packageInstallButton = new Button(LABEL_PACKAGE_INSTALL);
    private final Button packageCenterOpenButton = new Button(LABEL_PACKAGE_CENTER_OPEN);
    private final Label packageSelectedTitleValue = new Label("No package selected");
    private final Label packageSelectedCodeValue = new Label("Select a package card");
    private final Label packageSelectedStatusValue = new Label("Idle");
    private final TextArea packageResultArea = new TextArea();
    private final Label quickAppTemplateCountValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label quickAppLastProjectValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label quickAppLastTemplateValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label quickAppLastStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label quickAppStackSummaryValue = new Label("Apache + MySQL + PHP");
    private final Label quickAppProvisioningSummaryValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label quickAppDatabaseSummaryValue = new Label(SUMMARY_VALUE_EMPTY);
    private final TextField quickAppProjectCodeField = new TextField(DesktopApiConfig.DEFAULT_QUICK_APP_PROJECT_CODE);
    private final TextField quickAppProjectNameField = new TextField(DesktopApiConfig.DEFAULT_QUICK_APP_PROJECT_NAME);
    private final TextField quickAppTemplateCodeField = new TextField(DesktopApiConfig.DEFAULT_QUICK_APP_TEMPLATE_CODE);
    private final TextField quickAppDomainField = new TextField(DesktopApiConfig.DEFAULT_QUICK_APP_DOMAIN);
    private final TextField quickAppPortField = new TextField(String.valueOf(DesktopApiConfig.DEFAULT_QUICK_APP_PORT));
    private final ToggleGroup quickAppWebServerToggleGroup = new ToggleGroup();
    private final RadioButton quickAppApacheRadio = new RadioButton(LABEL_QUICK_APP_USE_APACHE);
    private final RadioButton quickAppNginxRadio = new RadioButton(LABEL_QUICK_APP_USE_NGINX);
    private final CheckBox quickAppMysqlCheckBox = new CheckBox(LABEL_QUICK_APP_INCLUDE_MYSQL);
    private final CheckBox quickAppPhpCheckBox = new CheckBox(LABEL_QUICK_APP_INCLUDE_PHP);
    private final CheckBox quickAppMailpitCheckBox = new CheckBox(LABEL_QUICK_APP_INCLUDE_MAILPIT);
    private final Label summaryProfileValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label summaryStatusValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label summaryRunCountValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label summaryLockCountValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label summaryStepCountValue = new Label(SUMMARY_VALUE_EMPTY);
    private final Label summaryRunIdValue = new Label(SUMMARY_VALUE_EMPTY);
    private final TextField workflowProjectCodeField = new TextField(DesktopApiConfig.DEFAULT_WORKFLOW_PROJECT_CODE);
    private final TextField workflowDomainField = new TextField(DesktopApiConfig.DEFAULT_WORKFLOW_DOMAIN);
    private final TextField workflowPortField = new TextField(String.valueOf(DesktopApiConfig.DEFAULT_WORKFLOW_PORT));
    private final TextField workflowTargetDirField = new TextField(DesktopApiConfig.DEFAULT_WORKFLOW_TARGET_DIR);
    private final TabPane applicationLogsTabPane = new TabPane();
    private final TextArea logArea = new TextArea();
    private final TextArea agentLogArea = new TextArea();
    private final TextArea apacheLogArea = new TextArea();
    private final TextArea nginxLogArea = new TextArea();
    private final TextArea phpLogArea = new TextArea();
    private final TextArea mysqlLogArea = new TextArea();
    private final TextArea mailpitLogArea = new TextArea();
    private final TextArea systemLogArea = new TextArea();
    private final Button clearCurrentLogButton = new Button("Clear");
    private final Button openCurrentLogButton = new Button("Open File");
    private final VBox dashboardBody = new VBox(14);
    private EventHandler<ActionEvent> selectApacheWebServerHandler;
    private EventHandler<ActionEvent> selectNginxWebServerHandler;
    private final BrandingResourceTool brandingResourceTool = new BrandingResourceTool();
    private final boolean devModeEnabled;

    public LauncherView() {
        this(false);
    }

    public LauncherView(boolean devModeEnabled) {
        this.devModeEnabled = devModeEnabled;
        configureQuickAppStackOptions();
        bindSiteWizardPreviewFields();
    }

    public Parent render() {
        BorderPane root = new BorderPane();
        root.getStyleClass().add(STYLE_ROOT);
        root.setLeft(buildSidebar());
        root.setCenter(buildSidebarModeContent());
        return root;
    }

    private void configureQuickAppStackOptions() {
        quickAppApacheRadio.setToggleGroup(quickAppWebServerToggleGroup);
        quickAppNginxRadio.setToggleGroup(quickAppWebServerToggleGroup);
        quickAppApacheRadio.setSelected(DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(DesktopApiConfig.DEFAULT_QUICK_APP_WEB_SERVER));
        quickAppNginxRadio.setSelected(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(DesktopApiConfig.DEFAULT_QUICK_APP_WEB_SERVER));
        quickAppMysqlCheckBox.setSelected(DesktopApiConfig.DEFAULT_QUICK_APP_INCLUDE_MYSQL);
        quickAppPhpCheckBox.setSelected(DesktopApiConfig.DEFAULT_QUICK_APP_INCLUDE_PHP);
        quickAppMailpitCheckBox.setSelected(DesktopApiConfig.DEFAULT_QUICK_APP_INCLUDE_MAILPIT);
    }

    private void bindSiteWizardPreviewFields() {
        quickAppProjectCodeField.textProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppDomainField.textProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppPortField.textProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppWebServerToggleGroup.selectedToggleProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppMysqlCheckBox.selectedProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppPhpCheckBox.selectedProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        quickAppMailpitCheckBox.selectedProperty().addListener((observable, oldValue, newValue) -> updateSiteWizardPreview());
        updateSiteWizardPreview();
    }

    private void updateSiteWizardPreview() {
        String domain = safePreviewValue(quickAppDomainField.getText(), DesktopApiConfig.DEFAULT_QUICK_APP_DOMAIN);
        String port = safePreviewValue(quickAppPortField.getText(), String.valueOf(DesktopApiConfig.DEFAULT_QUICK_APP_PORT));
        String projectCode = safePreviewValue(quickAppProjectCodeField.getText(), DesktopApiConfig.DEFAULT_QUICK_APP_PROJECT_CODE);
        siteWizardUrlPreviewValue.setText("http://" + domain + ":" + port);
        siteWizardFolderPreviewValue.setText(DesktopApiConfig.WEB_SERVER_SHARED_DOCUMENT_ROOT + "\\" + projectCode);
        String stackLabel = buildQuickAppStackLabel();
        siteWizardStackPreviewValue.setText(stackLabel);
        quickAppStackSummaryValue.setText(stackLabel);
    }

    private String safePreviewValue(String value, String fallback) {
        if (value == null || value.isBlank()) {
            return fallback;
        }
        return value.trim();
    }

    private String buildQuickAppStackLabel() {
        StringBuilder builder = new StringBuilder();
        builder.append(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(getQuickAppWebServer()) ? LABEL_QUICK_APP_USE_NGINX : LABEL_QUICK_APP_USE_APACHE);
        if (isQuickAppMysqlEnabled()) {
            builder.append(" + ").append(LABEL_QUICK_APP_INCLUDE_MYSQL);
        }
        if (isQuickAppPhpEnabled()) {
            builder.append(" + ").append(LABEL_QUICK_APP_INCLUDE_PHP);
        }
        if (isQuickAppMailpitEnabled()) {
            builder.append(" + ").append(LABEL_QUICK_APP_INCLUDE_MAILPIT);
        }
        return builder.toString();
    }


    private Node buildBrandMark(double size) {
        Optional<ImageView> logoView = brandingResourceTool.createFxLogoView(size);
        if (logoView.isPresent()) {
            ImageView view = logoView.get();
            view.getStyleClass().add("jhoster-brand-image");
            return view;
        }

        Label fallback = new Label("J");
        fallback.getStyleClass().add(STYLE_BRAND_MARK);
        return fallback;
    }

    private Parent buildSidebar() {
        VBox sidebar = new VBox(18);
        sidebar.getStyleClass().add(STYLE_SIDEBAR);
        sidebar.setPrefWidth(260);

        HBox brand = new HBox(12);
        brand.setAlignment(Pos.CENTER_LEFT);

        Node mark = buildBrandMark(48);

        VBox brandText = new VBox(2);
        Label title = new Label(TITLE_TEXT);
        title.getStyleClass().add(STYLE_BRAND_TITLE);

        Label subtitle = new Label(SUBTITLE_TEXT);
        subtitle.getStyleClass().add(STYLE_BRAND_SUBTITLE);

        brandText.getChildren().addAll(title, subtitle);
        brand.getChildren().addAll(mark, brandText);

        Region spacer = new Region();
        VBox.setVgrow(spacer, Priority.ALWAYS);

        sidebar.getChildren().addAll(
            brand,
            buildSidebarGroup("CREATE", navNewSiteButton, navProjectsButton, navAppsButton),
            buildSidebarGroup("OPERATE", navServicesButton, navVirtualHostsButton, navWorkflowButton),
            buildSidebarGroup("RESOURCES", navVersionsButton, navToolsButton),
            buildSidebarGroup("OBSERVE", navDashboardButton, navLogsButton)
        );

        if (devModeEnabled) {
            sidebar.getChildren().add(buildDeveloperSidebarGroup());
        }

        sidebar.getChildren().addAll(
            buildSidebarGroup("SETTINGS", navSettingsButton),
            spacer,
            buildSidebarFooter()
        );

        return sidebar;
    }

    private VBox buildSidebarGroup(String title, Button... items) {
        VBox group = new VBox(8);
        group.getStyleClass().add(STYLE_SIDEBAR_GROUP);

        Label groupTitle = new Label(title);
        groupTitle.getStyleClass().add(STYLE_SIDEBAR_TITLE);
        group.getChildren().add(groupTitle);

        for (Button navItem : items) {
            navItem.getStyleClass().add(STYLE_NAV_BUTTON);
            navItem.setMaxWidth(Double.MAX_VALUE);
            if (navItem == navNewSiteButton) {
                navItem.getStyleClass().add(STYLE_SIDEBAR_ACTIVE);
            }
            group.getChildren().add(navItem);
        }

        return group;
    }

    private VBox buildDeveloperSidebarGroup() {
        VBox group = buildSidebarGroup("DEVELOPER", navDeveloperButton);
        group.getStyleClass().add(STYLE_DEV_SIDEBAR_GROUP);
        navDeveloperButton.getStyleClass().add(STYLE_DEV_SIDEBAR_BUTTON);
        return group;
    }

    private Parent buildSidebarFooter() {
        VBox footer = new VBox(6);
        footer.getStyleClass().add(STYLE_SIDEBAR_FOOTER);

        Label title = new Label("JHoster Desktop");
        title.getStyleClass().add(STYLE_SUMMARY_VALUE);

        Label version = new Label(devModeEnabled ? DECK_VERSION_TEXT + "  -  DEV MODE ACTIVE" : DECK_VERSION_TEXT + "  -  Deck Mode");
        version.getStyleClass().add(STYLE_CARD_TEXT);

        if (devModeEnabled) {
            footer.getStyleClass().add(STYLE_DEV_FOOTER);
        }

        footer.getChildren().addAll(title, version);
        return footer;
    }

    private Parent buildMainContent() {
        return buildSidebarModeContent();
    }

    private Parent buildSidebarModeContent() {
        ensureDefaultStatusLabels();

        ScrollPane scrollPane = new ScrollPane();
        scrollPane.setFitToWidth(true);
        scrollPane.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
        scrollPane.setVbarPolicy(ScrollPane.ScrollBarPolicy.AS_NEEDED);

        VBox content = new VBox(16);
        content.getStyleClass().add(STYLE_CONTENT);
        content.getStyleClass().add("jhoster-left-menu-content");
        if (!dashboardBody.getStyleClass().contains(STYLE_DASHBOARD_BODY)) {
            dashboardBody.getStyleClass().add(STYLE_DASHBOARD_BODY);
        }
        showNewSitePage();
        content.getChildren().addAll(
            buildTopbar(),
            dashboardBody
        );

        scrollPane.setContent(content);
        return scrollPane;
    }

    private void ensureDefaultStatusLabels() {
        setDefaultStatus(compactApacheStatusValue);
        setDefaultStatus(compactNginxStatusValue);
        setDefaultStatus(compactMysqlStatusValue);
        setDefaultStatus(compactPhpStatusValue);
        setDefaultStatus(compactMailpitStatusValue);
        setDefaultStatus(simpleWebServerStatusValue);
    }

    private void setDefaultStatus(Label label) {
        if (SUMMARY_VALUE_EMPTY.equals(label.getText())) {
            label.setText(VALUE_RUNNING);
        }
        applyStatusStyle(label, label.getText());
    }
    private Parent buildSimpleModeContent() {
        ensureDefaultStatusLabels();

        ScrollPane scrollPane = new ScrollPane();
        scrollPane.setFitToWidth(true);
        scrollPane.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
        scrollPane.setVbarPolicy(ScrollPane.ScrollBarPolicy.AS_NEEDED);

        VBox content = new VBox(18);
        content.getStyleClass().add(STYLE_CONTENT);
        content.getStyleClass().add("jhoster-simple-mode");
        content.getChildren().addAll(
            buildSimpleModeHeader(),
            buildModernCommandHeroPanel(),
            buildSimpleModeBottomBar(),
            buildSimpleModeMainTabs()
        );

        scrollPane.setContent(content);
        return scrollPane;
    }

    private Parent buildModernCommandHeroPanel() {
        HBox shell = new HBox(16);
        shell.getStyleClass().add(STYLE_MODERN_HERO_SHELL);

        VBox hero = new VBox(14);
        hero.getStyleClass().add(STYLE_MODERN_HERO_CARD);
        HBox.setHgrow(hero, Priority.ALWAYS);

        HBox badgeRow = new HBox(10);
        badgeRow.setAlignment(Pos.CENTER_LEFT);
        Label badge = new Label(LABEL_MODERN_HERO_BADGE);
        badge.getStyleClass().add(STYLE_MODERN_HERO_BADGE);
        Label edition = new Label(DECK_EDITION_TEXT + " / " + LICENSE_DEFAULT_USAGE_TEXT);
        edition.getStyleClass().add(STYLE_PREMIUM_BADGE);
        badgeRow.getChildren().addAll(badge, edition);

        Label title = new Label(LABEL_MODERN_HERO_TITLE);
        title.getStyleClass().add(STYLE_MODERN_HERO_TITLE);
        title.setWrapText(true);

        Label subtitle = new Label(LABEL_MODERN_HERO_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_MODERN_HERO_SUBTITLE);
        subtitle.setWrapText(true);

        HBox flow = new HBox(10);
        flow.getStyleClass().add(STYLE_MODERN_FLOW_ROW);
        flow.getChildren().addAll(
            buildModernFlowPill(LABEL_MODERN_HERO_STEP_STACK, buildQuickAppStackLabel()),
            buildModernFlowPill(LABEL_MODERN_HERO_STEP_DOMAIN, DesktopApiConfig.DEFAULT_QUICK_APP_DOMAIN),
            buildModernFlowPill(LABEL_MODERN_HERO_STEP_CREATE, "Plan before create")
        );

        hero.getChildren().addAll(badgeRow, title, subtitle, flow);

        VBox statusRail = new VBox(12);
        statusRail.getStyleClass().add(STYLE_MODERN_STATUS_RAIL);
        statusRail.setPrefWidth(360);
        statusRail.setMinWidth(320);

        Label statusTitle = new Label(LABEL_MODERN_STATUS_TITLE);
        statusTitle.getStyleClass().add(STYLE_CARD_TITLE);
        Label statusSubtitle = new Label(LABEL_MODERN_STATUS_SUBTITLE);
        statusSubtitle.getStyleClass().add(STYLE_CARD_TEXT);

        statusRail.getChildren().addAll(
            statusTitle,
            statusSubtitle,
            buildModernStatusMetric(LABEL_MODERN_STATUS_ACTIVE_PLAN, DECK_EDITION_TEXT),
            buildModernStatusMetric(LABEL_MODERN_STATUS_ACTIVE_SITES, LICENSE_DEFAULT_USAGE_TEXT),
            buildModernStatusMetric(LABEL_MODERN_STATUS_HOSTS, VALUE_HOSTS_AUTO_NOT_CHECKED),
            buildModernPresetCard(LABEL_MODERN_STACK_PRESET_TITLE, LABEL_MODERN_STACK_PRESET_TEXT),
            buildModernPresetCard(LABEL_MODERN_PACKAGE_TITLE, LABEL_MODERN_PACKAGE_TEXT)
        );

        shell.getChildren().addAll(hero, statusRail);
        return shell;
    }

    private Parent buildModernFlowPill(String titleText, String valueText) {
        VBox pill = new VBox(4);
        pill.getStyleClass().add(STYLE_MODERN_FLOW_PILL);
        HBox.setHgrow(pill, Priority.ALWAYS);

        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_CARD_TEXT);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_SUMMARY_VALUE);
        value.setWrapText(true);

        pill.getChildren().addAll(title, value);
        return pill;
    }

    private Parent buildModernStatusMetric(String labelText, String valueText) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_MODERN_STATUS_CARD);

        Label label = new Label(labelText);
        label.getStyleClass().add(STYLE_MODERN_STATUS_TITLE);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_MODERN_STATUS_VALUE);

        row.getChildren().addAll(label, spacer, value);
        return row;
    }

    private Parent buildModernPresetCard(String titleText, String text) {
        VBox card = new VBox(6);
        card.getStyleClass().add(STYLE_MODERN_PRESET_CARD);

        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SUMMARY_VALUE);
        Label description = new Label(text);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);

        card.getChildren().addAll(title, description);
        return card;
    }

    private Parent buildSimpleModeHeader() {
        VBox wrapper = new VBox(12);
        wrapper.getStyleClass().add("jhoster-deck-header-card");

        HBox topRow = new HBox(12);
        topRow.setAlignment(Pos.CENTER_LEFT);

        Node mark = buildBrandMark(56);

        VBox titleBox = new VBox(2);
        HBox titleLine = new HBox(10);
        titleLine.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(DECK_TITLE_TEXT);
        title.getStyleClass().add(STYLE_BRAND_TITLE);
        title.setMinWidth(220);
        Label version = new Label(DECK_VERSION_TEXT);
        version.getStyleClass().add("jhoster-version-badge");
        licenseBadgeLabel.getStyleClass().add("jhoster-community-badge");
        titleLine.getChildren().addAll(title, version, licenseBadgeLabel);
        Label subtitle = new Label(DECK_SUBTITLE_TEXT);
        subtitle.getStyleClass().add(STYLE_BRAND_SUBTITLE);
        titleBox.setMinWidth(360);
        titleBox.getChildren().addAll(titleLine, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        Label stackProfile = new Label("Local PHP Stack");
        stackProfile.getStyleClass().add(STYLE_BADGE);

        navSettingsButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        navSettingsButton.getStyleClass().add("jhoster-deck-settings-button");

        topRow.getChildren().addAll(mark, titleBox, spacer, stackProfile, navSettingsButton);

        HBox metaRow = new HBox(16);
        metaRow.setAlignment(Pos.CENTER_LEFT);

        Label workspace = new Label("Shared WWW: " + DesktopApiConfig.WEB_SERVER_SHARED_DOCUMENT_ROOT);
        workspace.getStyleClass().add(STYLE_CARD_TEXT);

        Label profile = new Label(PROFILE_BADGE_TEXT);
        profile.getStyleClass().add(STYLE_BADGE);

        licenseUsageLabel.getStyleClass().add("jhoster-license-usage-badge");

        Label hint = new Label(SIMPLE_MODE_HINT_TEXT);
        hint.getStyleClass().add(STYLE_CARD_TEXT);
        hint.setWrapText(true);

        metaRow.getChildren().addAll(workspace, profile, licenseUsageLabel);
        wrapper.getChildren().addAll(topRow, metaRow, hint);
        return wrapper;
    }

    private Parent buildSimpleModeMainTabs() {
        VBox stack = new VBox(18);
        stack.getStyleClass().add(STYLE_FULLSCREEN_STACK);
        stack.getChildren().addAll(
            buildSiteWizardPanel(),
            buildSimpleModeCenterGrid(),
            buildPackageCenterInlinePanel(),
            buildSimpleModeLogTabs()
        );
        return stack;
    }

    private Parent buildSiteWizardPanel() {
        HBox layout = new HBox(16);
        layout.getStyleClass().add(STYLE_SITE_WIZARD_LAYOUT);

        Parent mainPanel = buildQuickAppPanel();
        if (mainPanel instanceof VBox mainBox) {
            mainBox.getStyleClass().add(STYLE_SITE_WIZARD_MAIN);
            mainBox.setPrefWidth(680);
            HBox.setHgrow(mainBox, Priority.ALWAYS);
        }

        Parent previewPanel = buildSiteWizardPreviewPanel();
        layout.getChildren().addAll(mainPanel, previewPanel);
        return layout;
    }

    private Parent buildSiteWizardPreviewPanel() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add(STYLE_SITE_WIZARD_PREVIEW);
        card.setPrefWidth(320);
        card.setMinWidth(300);

        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_SITE_WIZARD_CARD);
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label badge = new Label(LABEL_SITE_WIZARD_BADGE);
        badge.getStyleClass().add(STYLE_PREMIUM_BADGE);
        header.getChildren().addAll(title, badge);

        Label subtitle = new Label(LABEL_SITE_WIZARD_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);

        VBox preview = new VBox(8);
        preview.getStyleClass().add(STYLE_SITE_WIZARD_PREVIEW_CARD);
        siteWizardUrlPreviewValue.getStyleClass().add(STYLE_SUMMARY_VALUE);
        siteWizardFolderPreviewValue.getStyleClass().add(STYLE_SUMMARY_VALUE);
        siteWizardStackPreviewValue.getStyleClass().add(STYLE_SUMMARY_VALUE);
        preview.getChildren().addAll(
            buildInfoRowWithValue(LABEL_SITE_WIZARD_URL_PREVIEW, siteWizardUrlPreviewValue),
            buildInfoRowWithValue(LABEL_SITE_WIZARD_FOLDER_PREVIEW, siteWizardFolderPreviewValue),
            buildInfoRowWithValue(LABEL_SITE_WIZARD_STACK_PREVIEW, siteWizardStackPreviewValue),
            buildInfoRow(LABEL_SITE_WIZARD_HOSTS_PREVIEW, VALUE_SITE_WIZARD_HOSTS_AUTO),
            buildInfoRowWithValue(LABEL_HOSTS_AUTO_STATUS, siteWizardHostsStatusPreviewValue),
            buildInfoRowWithValue(LABEL_HOSTS_AUTO_ISSUES, siteWizardHostsIssuesPreviewValue)
        );

        card.getChildren().addAll(
            header,
            subtitle,
            buildSiteWizardStep(VALUE_SITE_WIZARD_STEP_ONE, LABEL_SITE_WIZARD_STEP_PROJECT, LABEL_SITE_WIZARD_STEP_PROJECT_TEXT),
            buildSiteWizardStep(VALUE_SITE_WIZARD_STEP_TWO, LABEL_SITE_WIZARD_STEP_DOMAIN, LABEL_SITE_WIZARD_STEP_DOMAIN_TEXT),
            buildSiteWizardStep(VALUE_SITE_WIZARD_STEP_THREE, LABEL_SITE_WIZARD_STEP_CREATE, LABEL_SITE_WIZARD_STEP_CREATE_TEXT),
            preview
        );
        return card;
    }

    private Parent buildSiteWizardStep(String numberText, String titleText, String descriptionText) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_SITE_WIZARD_STEP);

        Label badge = new Label(numberText);
        badge.getStyleClass().add(STYLE_SITE_WIZARD_STEP_BADGE);

        VBox textBox = new VBox(2);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SUMMARY_VALUE);
        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);
        textBox.getChildren().addAll(title, description);

        row.getChildren().addAll(badge, textBox);
        return row;
    }

    private Parent buildPackageCenterInlinePanel() {
        VBox wrapper = new VBox(14);
        wrapper.getStyleClass().add("jhoster-package-center-inline");

        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_PACKAGE_CENTER);
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label badge = new Label("Manifest downloader ready");
        badge.getStyleClass().add(STYLE_PREMIUM_BADGE);
        header.getChildren().addAll(title, badge);

        Label subtitle = new Label(LABEL_PACKAGE_CENTER_DIALOG_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);

        wrapper.getChildren().addAll(header, subtitle, buildPackageSelectionPanel(), buildPackagePathStrip(), buildPackageCategoryTabs(), buildPackageDownloaderPanel());
        return wrapper;
    }

    private Parent buildSimpleModeCenterGrid() {
        HBox grid = new HBox(16);
        grid.getStyleClass().add("jhoster-deck-center-grid");

        Parent services = buildSimpleModeServiceList();
        HBox.setHgrow(services, Priority.ALWAYS);
        if (services instanceof VBox servicesBox) {
            servicesBox.setPrefWidth(860);
            servicesBox.setMinWidth(740);
        }

        Parent insight = buildSimpleModeInsightPanel();
        grid.getChildren().addAll(services, insight);
        return grid;
    }

    private Parent buildSimpleModeInsightPanel() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-deck-insight-panel");
        card.setPrefWidth(280);
        card.setMinWidth(260);

        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_SYSTEM_OVERVIEW);
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label badge = new Label("Live");
        badge.getStyleClass().add(STYLE_PREMIUM_BADGE);
        header.getChildren().addAll(title, badge);

        Label subtitle = new Label("Live stack metrics and workspace insights.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);

        card.getChildren().addAll(
            header,
            subtitle,
            buildSimpleModeInsightMetric(LABEL_STACK_HEALTH, VALUE_HEALTHY, 1.0),
            buildSimpleModeInsightMetric(LABEL_ACTIVE_ENGINE, simpleWebServerNameValue.getText(), 0.72),
            buildSimpleModeInsightMetric(LABEL_PACKAGE_STATUS, "Ready", 0.58),
            buildInfoRow(LABEL_WORKSPACE, VALUE_COMPACT_ROOT),
            buildInfoRow(LABEL_SHARED_WWW, DesktopApiConfig.WEB_SERVER_SHARED_DOCUMENT_ROOT)
        );
        return card;
    }

    private Parent buildSimplePackageCenterMiniCard() {
        VBox card = new VBox(5);
        card.getStyleClass().add("jhoster-package-mini-card");

        Label title = new Label(LABEL_PACKAGE_CENTER);
        title.getStyleClass().add(STYLE_SUMMARY_VALUE);
        Label status = new Label(LABEL_PACKAGE_CENTER_READY);
        status.getStyleClass().add(STYLE_CARD_TEXT);
        Label stack = new Label(LABEL_PACKAGE_CENTER_STACK);
        stack.getStyleClass().add("jhoster-package-mini-stack");
        packageCenterOpenButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        packageCenterOpenButton.getStyleClass().add("jhoster-package-mini-open");
        packageCenterOpenButton.setMaxWidth(Double.MAX_VALUE);

        card.getChildren().addAll(title, status, stack, packageCenterOpenButton);
        return card;
    }

    private Parent buildSimpleModeInsightMetric(String titleText, String valueText, double progressValue) {
        VBox box = new VBox(6);
        box.getStyleClass().add("jhoster-deck-insight-metric");

        HBox row = new HBox(8);
        row.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_CARD_TEXT);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_SUMMARY_VALUE);
        row.getChildren().addAll(title, spacer, value);

        ProgressBar progressBar = new ProgressBar(progressValue);
        progressBar.setMaxWidth(Double.MAX_VALUE);
        progressBar.getStyleClass().add("jhoster-deck-progress");
        box.getChildren().addAll(row, progressBar);
        return box;
    }

    private Parent buildSimpleModeServiceList() {
        VBox card = new VBox(10);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-simple-service-card");

        Label title = new Label("Services");
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label subtitle = new Label("Daily service controls for your active local stack.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);

        card.getChildren().addAll(
            title,
            subtitle,
            buildSimpleModeWebServerRow(),
            buildSimpleModeServiceRow("Database", LABEL_SERVICE_MYSQL, "3306", compactMysqlStatusValue, compactMysqlStartButton, compactMysqlStopButton, compactMysqlRestartButton),
            buildSimpleModeServiceRow("Runtime", LABEL_SERVICE_PHP, "9000", compactPhpStatusValue, compactPhpStartButton, compactPhpStopButton, compactPhpRestartButton),
            buildSimpleModeServiceRow("Mail", LABEL_SERVICE_MAILPIT, "1025 / 8025", compactMailpitStatusValue, compactMailpitStartButton, compactMailpitStopButton, compactMailpitRestartButton)
        );

        return card;
    }

    private Parent buildSimpleModeWebServerRow() {
        HBox row = new HBox(12);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add("jhoster-deck-web-row");

        Label toggle = new Label("●");
        toggle.getStyleClass().add("jhoster-compact-service-dot");
        toggle.setMinWidth(20);

        Label roleLabel = new Label(LABEL_SERVICE_WEB_SERVER);
        roleLabel.getStyleClass().add("jhoster-service-role-badge");

        simpleWebServerNameValue.getStyleClass().add("jhoster-simple-service-name");
        simpleWebServerNameValue.getStyleClass().add("jhoster-service-name-pill");

        StackPane identityBox = buildServiceIdentityBox(roleLabel, simpleWebServerNameValue, 132);

        Label portLabel = new Label(VALUE_WEB_SERVER_PORTS);
        portLabel.getStyleClass().add(STYLE_CARD_TEXT);
        portLabel.setMinWidth(86);

        simpleWebServerStatusValue.getStyleClass().add(STYLE_BADGE);
        simpleWebServerStatusValue.setMinWidth(90);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        simpleWebServerSwitchButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        simpleWebServerStartButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        simpleWebServerStartButton.getStyleClass().add(STYLE_COMPACT_SERVICE_START);
        simpleWebServerStopButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        simpleWebServerStopButton.getStyleClass().add(STYLE_COMPACT_SERVICE_STOP);
        simpleWebServerRestartButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        simpleWebServerRestartButton.getStyleClass().add(STYLE_COMPACT_SERVICE_RESTART);

        normalizeDeckActionButton(simpleWebServerStatusValue, 88);
        normalizeDeckActionButton(simpleWebServerSwitchButton, 68);
        normalizeDeckActionButton(simpleWebServerStartButton, 68);
        normalizeDeckActionButton(simpleWebServerStopButton, 68);
        normalizeDeckActionButton(simpleWebServerRestartButton, 72);

        row.getChildren().addAll(
            toggle,
            identityBox,
            portLabel,
            simpleWebServerStatusValue,
            spacer,
            simpleWebServerSwitchButton,
            simpleWebServerStartButton,
            simpleWebServerStopButton,
            simpleWebServerRestartButton
        );
        return row;
    }

    private Parent buildSimpleModeServiceRow(String role, String name, String ports, Label statusLabel, Button startButton, Button stopButton, Button restartButton) {
        HBox row = new HBox(12);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add("jhoster-simple-service-row");

        Label toggle = new Label("○");
        toggle.getStyleClass().add("jhoster-compact-service-dot");
        toggle.setMinWidth(20);

        Label roleLabel = new Label(role);
        roleLabel.getStyleClass().add("jhoster-service-role-badge");

        Label nameLabel = new Label(name);
        nameLabel.getStyleClass().add("jhoster-simple-service-name");
        nameLabel.getStyleClass().add("jhoster-service-name-pill");

        StackPane identityBox = buildServiceIdentityBox(roleLabel, nameLabel, 132);

        Label portLabel = new Label(ports);
        portLabel.getStyleClass().add(STYLE_CARD_TEXT);
        portLabel.setMinWidth(86);

        statusLabel.getStyleClass().add(STYLE_BADGE);
        statusLabel.setMinWidth(90);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        startButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        startButton.getStyleClass().add(STYLE_COMPACT_SERVICE_START);
        stopButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        stopButton.getStyleClass().add(STYLE_COMPACT_SERVICE_STOP);
        restartButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        restartButton.getStyleClass().add(STYLE_COMPACT_SERVICE_RESTART);

        normalizeDeckActionButton(startButton, 68);
        normalizeDeckActionButton(stopButton, 68);
        normalizeDeckActionButton(restartButton, 72);
        normalizeDeckActionButton(statusLabel, 88);

        row.getChildren().addAll(toggle, identityBox, portLabel, statusLabel, spacer, startButton, stopButton, restartButton);
        return row;
    }

    private StackPane buildServiceIdentityBox(Label roleLabel, Label nameLabel, double width) {
        StackPane identityBox = new StackPane();
        identityBox.getStyleClass().add("jhoster-service-identity-box");
        identityBox.setAlignment(Pos.CENTER_LEFT);
        identityBox.setMinWidth(width);
        identityBox.setPrefWidth(width);
        identityBox.setMaxWidth(width);
        identityBox.setMinHeight(54);
        identityBox.setPrefHeight(54);

        normalizeDeckActionButton(roleLabel, width - 32);
        normalizeDeckActionButton(nameLabel, width);

        StackPane.setAlignment(nameLabel, Pos.CENTER_LEFT);
        StackPane.setAlignment(roleLabel, Pos.TOP_LEFT);
        nameLabel.setTranslateY(8);
        roleLabel.setTranslateY(-12);

        identityBox.getChildren().addAll(nameLabel, roleLabel);
        return identityBox;
    }

    private void normalizeDeckActionButton(Button button, double width) {
        button.setMinWidth(width);
        button.setPrefWidth(width);
        button.setMaxWidth(width);
    }

    private void normalizeDeckActionButton(Label label, double width) {
        label.setMinWidth(width);
        label.setPrefWidth(width);
        label.setMaxWidth(width);
        label.setAlignment(Pos.CENTER);
    }

    public void setStackControlRunning(boolean running) {
        quickStartAllButton.setVisible(!running);
        quickStartAllButton.setManaged(!running);
        quickStopAllButton.setVisible(running);
        quickStopAllButton.setManaged(running);
    }

    private Parent buildSimpleModeLogTabs() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-deck-log-card");

        Label title = new Label("Application Logs");
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label subtitle = new Label("Each application keeps its own log tab for faster troubleshooting.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);

        TabPane previewTabs = buildApplicationLogPreviewTabPane();
        previewTabs.setPrefHeight(260);

        card.getChildren().addAll(title, subtitle, previewTabs);
        return card;
    }

    private Parent buildSimpleModeBottomBar() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-simple-bottom-bar");

        Label title = new Label(LABEL_QUICK_ACTION_BAR);
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label subtitle = new Label("Fast access for stack actions and daily tools.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);

        HBox dock = new HBox(14);
        dock.setAlignment(Pos.CENTER_LEFT);

        HBox stackActions = new HBox(10);
        stackActions.setAlignment(Pos.CENTER_LEFT);
        stackActions.getStyleClass().add("jhoster-deck-action-group");

        quickStartAllButton.setText("▶ Start Stack");
        quickStopAllButton.setText("■ Stop Stack");
        quickWebButton.setText("🌐 Web");
        quickDatabaseButton.setText("🗄 Database");
        quickTerminalButton.setText("⌨ Terminal");
        quickRootButton.setText("📁 Root");

        quickStartAllButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickStartAllButton.getStyleClass().add("jhoster-deck-start-stack");
        quickStopAllButton.getStyleClass().add(STYLE_DANGER_BUTTON);
        quickStopAllButton.getStyleClass().add("jhoster-deck-stop-stack");
        quickStartAllButton.setPrefHeight(46);
        quickStopAllButton.setPrefHeight(46);
        quickStartAllButton.setMinWidth(150);
        quickStopAllButton.setMinWidth(150);
        setStackControlRunning(false);
        stackActions.getChildren().addAll(quickStartAllButton, quickStopAllButton);

        HBox openActions = new HBox(10);
        openActions.setAlignment(Pos.CENTER_LEFT);
        openActions.getStyleClass().add("jhoster-deck-action-group");

        for (Button button : new Button[]{quickWebButton, quickDatabaseButton, quickTerminalButton, quickRootButton}) {
            button.getStyleClass().add(STYLE_SECONDARY_BUTTON);
            button.getStyleClass().add("jhoster-deck-open-action");
            button.setMaxWidth(Double.MAX_VALUE);
            button.setPrefHeight(42);
            HBox.setHgrow(button, Priority.ALWAYS);
        }
        openActions.getChildren().addAll(quickWebButton, quickDatabaseButton, quickTerminalButton, quickRootButton);

        HBox.setHgrow(openActions, Priority.ALWAYS);
        dock.getChildren().addAll(stackActions, openActions);
        card.getChildren().addAll(title, subtitle, dock);
        return card;
    }

    public void showNewSitePage() {
        activateSidebar(navNewSiteButton);
        activateDashboardTab(quickAppTabButton);
        setDashboardBody(
            buildPageHeader("New Site", "Create a local test site with Apache or Nginx, MySQL, PHP, Mailpit and automatic hosts mapping."),
            buildSiteWizardPanel()
        );
    }

    public void showOverviewPage() {
        activateSidebar(navDashboardButton);
        activateDashboardTab(overviewTabButton);
        setDashboardBody(
            buildCleanQuickActionsPanel(),
            buildCleanServiceOverview(),
            buildDashboardBottomGrid()
        );
    }

    public void showServicesPage() {
        activateSidebar(navServicesButton);
        activateDashboardTab(overviewTabButton);
        setDashboardBody(
            buildPageHeader("Services", "Start, stop, restart and inspect local stack services."),
            buildCleanQuickActionsPanel(),
            buildCleanServiceOverview(),
            buildServiceManagerPanel()
        );
    }

    public void showRuntimeVersionsPage() {
        activateSidebar(navVersionsButton);
        activateDashboardTab(runtimeVersionsTabButton);
        setDashboardBody(
            buildPageHeader("Runtime Versions", "Select portable Apache, Nginx, MySQL, PHP, Node, Python and cache runtimes."),
            buildRuntimeManagerPanel(),
            buildPackageDownloaderPanel()
        );
    }

    public void showQuickAppPage() {
        activateSidebar(navNewSiteButton);
        activateDashboardTab(quickAppTabButton);
        setDashboardBody(
            buildPageHeader("Quick App", "Create scaffold-only local www projects from safe templates."),
            buildQuickAppPanel()
        );
    }

    public void showWorkflowPage() {
        activateSidebar(navWorkflowButton);
        activateDashboardTab(workflowTabButton);
        setDashboardBody(
            buildPageHeader("Workflow", "Plan, dry-run and publish Apache or Nginx virtual host workflows."),
            buildWorkflowPanel(),
            buildWorkflowOperationsPanel()
        );
    }

    public void showDiagnosticsPage() {
        if (!devModeEnabled) {
            showDeveloperModeRequiredPage("Diagnostics");
            return;
        }

        showDeveloperPage();
    }

    public void showDeveloperPage() {
        if (!devModeEnabled) {
            showDeveloperModeRequiredPage(DEV_MODE_PAGE_TITLE);
            return;
        }

        activateSidebar(navDeveloperButton);
        activateDashboardTab(diagnosticsTabButton);
        setDashboardBody(
            buildDeveloperModeBanner(),
            buildPageHeader(DEV_MODE_PAGE_TITLE, DEV_MODE_PAGE_SUBTITLE),
            buildDeveloperOperationsPanel()
        );
    }

    private void showDeveloperModeRequiredPage(String sourceTitle) {
        activateSidebar(navToolsButton);
        setDashboardBody(
            buildPageHeader(sourceTitle, DEV_MODE_REQUIRED_TITLE),
            buildInfoCard(DEV_MODE_REQUIRED_TITLE, DEV_MODE_REQUIRED_TEXT)
        );
    }

    public void showProjectsPage() {
        activateSidebar(navProjectsButton);
        setDashboardBody(
            buildPageHeader("Projects", "Open workspace projects and publish local hosts from one place."),
            buildProjectDeliveryPanel()
        );
    }

    public void showVirtualHostsPage() {
        activateSidebar(navVirtualHostsButton);
        setDashboardBody(
            buildPageHeader("Virtual Hosts", "Manage Apache and Nginx virtual host actions without crowding the dashboard."),
            buildVirtualHostOperationsPanel()
        );
    }

    public void showAppsPage() {
        activateSidebar(navAppsButton);
        activateDashboardTab(quickAppTabButton);
        setDashboardBody(
            buildPageHeader("Apps", "Use quick app templates and app module shortcuts."),
            buildQuickAppPanel(),
            buildAppsOperationsPanel()
        );
    }

    public void showToolsPage() {
        activateSidebar(navToolsButton);
        setDashboardBody(
            buildPageHeader("Tools", "Open portable developer tools from the JHoster bin folder."),
            buildCompactToolDock()
        );
    }

    public void showLogsPage() {
        activateSidebar(navLogsButton);
        setDashboardBody(
            buildPageHeader("Logs", "Review launcher activity and open service log folders when needed."),
            buildLogSection()
        );
    }

    private void setDashboardBody(Parent... nodes) {
        dashboardBody.getChildren().setAll(nodes);
    }

    private Parent buildPageHeader(String titleText, String subtitleText) {
        VBox header = new VBox(5);
        header.getStyleClass().add(STYLE_PAGE_HEADER);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(subtitleText);
        subtitle.getStyleClass().add(STYLE_PAGE_SUBTITLE);
        subtitle.setWrapText(true);
        header.getChildren().addAll(title, subtitle);
        return header;
    }

    private void activateSidebar(Button activeButton) {
        Button[] buttons = {
            navDashboardButton, navNewSiteButton, navServicesButton, navProjectsButton, navVirtualHostsButton,
            navAppsButton, navVersionsButton, navWorkflowButton, navToolsButton, navDeveloperButton, navLogsButton, navSettingsButton
        };
        for (Button button : buttons) {
            button.getStyleClass().removeAll(STYLE_SIDEBAR_ACTIVE);
        }
        if (activeButton != null && !activeButton.getStyleClass().contains(STYLE_SIDEBAR_ACTIVE)) {
            activeButton.getStyleClass().add(STYLE_SIDEBAR_ACTIVE);
        }
    }

    private void activateDashboardTab(Button activeButton) {
        Button[] buttons = {overviewTabButton, runtimeVersionsTabButton, quickAppTabButton, workflowTabButton, diagnosticsTabButton};
        for (Button button : buttons) {
            button.getStyleClass().removeAll(STYLE_DASHBOARD_TAB_ACTIVE);
        }
        if (activeButton != null && !activeButton.getStyleClass().contains(STYLE_DASHBOARD_TAB_ACTIVE)) {
            activeButton.getStyleClass().add(STYLE_DASHBOARD_TAB_ACTIVE);
        }
    }

    private void ensureLogInitialized() {
        if (logArea.getText() == null || logArea.getText().isBlank()) {
            logArea.setText(LOG_INITIAL_TEXT);
        }
    }

    private Parent buildTopbar() {
        HBox topbar = new HBox(14);
        topbar.setAlignment(Pos.CENTER_LEFT);
        topbar.getStyleClass().add(STYLE_TOPBAR);

        VBox titleBox = new VBox(3);
        Label title = new Label("Workspace Control");
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label("Create sites, control services and inspect local runtime status from the left menu.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        HBox statusStrip = new HBox(10);
        statusStrip.setAlignment(Pos.CENTER_RIGHT);
        statusStrip.getStyleClass().add("jhoster-topbar-status-strip");
        statusStrip.getChildren().addAll(
            buildTopbarStatusPill("Plan", topbarPlanValue),
            buildTopbarStatusPill("Sites", topbarSitesValue),
            buildTopbarStatusPill("Hosts", topbarHostsValue),
            buildTopbarStatusPill("Engine", topbarEngineValue)
        );

        topbar.getChildren().addAll(titleBox, spacer, statusStrip);
        if (devModeEnabled) {
            Label devBadge = new Label(DEV_MODE_BADGE_TEXT);
            devBadge.getStyleClass().add(STYLE_DEV_BADGE);
            topbar.getChildren().add(devBadge);
        }
        return topbar;
    }

    private Parent buildTopbarStatusPill(String labelText, Label valueLabel) {
        VBox pill = new VBox(2);
        pill.getStyleClass().add("jhoster-topbar-status-pill");

        Label label = new Label(labelText);
        label.getStyleClass().add("jhoster-topbar-status-label");
        valueLabel.getStyleClass().add("jhoster-topbar-status-value");

        pill.getChildren().addAll(label, valueLabel);
        return pill;
    }

    private Parent buildDashboardSummaryCards() {
        HBox cards = new HBox(14);
        cards.getChildren().addAll(
            buildDashboardMetricCard("S", LABEL_COMPACT_AGENT, VALUE_COMPACT_AGENT, "FastAPI control bridge", VALUE_RUNNING),
            buildDashboardMetricCard("W", LABEL_STACK_PROFILE, VALUE_COMPACT_WEB_PROFILE, "Unified publish workflow", null),
            buildDashboardMetricCard("R", LABEL_WORKSPACE_ROOT, VALUE_COMPACT_ROOT, "Portable workspace", null),
            buildDashboardMetricCard("H", LABEL_OVERALL_HEALTH, VALUE_HEALTHY, "All services operational", VALUE_HEALTH_PERCENT)
        );
        return cards;
    }

    private Parent buildDashboardMetricCard(String iconText, String titleText, String valueText, String descriptionText, String badgeText) {
        HBox card = new HBox(14);
        card.setAlignment(Pos.CENTER_LEFT);
        card.getStyleClass().add(STYLE_DASHBOARD_METRIC);
        HBox.setHgrow(card, Priority.ALWAYS);
        card.setMaxWidth(Double.MAX_VALUE);

        Label icon = new Label(iconText);
        icon.getStyleClass().add(STYLE_METRIC_ICON);

        VBox textBox = new VBox(5);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_CARD_TEXT);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_CARD_TITLE);
        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        textBox.getChildren().addAll(title, value, description);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        card.getChildren().addAll(icon, textBox, spacer);
        if (badgeText != null) {
            Label badge = new Label(badgeText);
            badge.getStyleClass().add(STYLE_STATUS_PILL);
            card.getChildren().add(badge);
        }

        return card;
    }

    private Parent buildDashboardTabs() {
        HBox tabs = new HBox(16);
        tabs.getStyleClass().add(STYLE_DASHBOARD_TABS);
        tabs.getChildren().addAll(
            buildDashboardTab(overviewTabButton, true),
            buildDashboardTab(runtimeVersionsTabButton, false),
            buildDashboardTab(quickAppTabButton, false),
            buildDashboardTab(workflowTabButton, false)
        );
        if (devModeEnabled) {
            tabs.getChildren().add(buildDashboardTab(diagnosticsTabButton, false));
        }
        return tabs;
    }

    private Button buildDashboardTab(Button tab, boolean active) {
        tab.getStyleClass().add(STYLE_DASHBOARD_TAB);
        if (active) {
            tab.getStyleClass().add(STYLE_DASHBOARD_TAB_ACTIVE);
        }
        tab.setMaxWidth(Double.MAX_VALUE);
        HBox.setHgrow(tab, Priority.ALWAYS);
        return tab;
    }

    private Parent buildCleanServiceOverview() {
        VBox card = new VBox(10);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add(STYLE_SERVICE_TABLE);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);
        VBox titleBox = new VBox(3);
        Label title = new Label(LABEL_COMPACT_SERVICES);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label("Core local development services");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        titleBox.getChildren().addAll(title, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        compactServiceRefreshButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(titleBox, spacer, compactServiceRefreshButton);

        card.getChildren().addAll(
            header,
            buildServiceHeaderRow(),
            buildCleanServiceRow(LABEL_SERVICE_APACHE, "Web Server", compactApacheStatusValue, "2.4.x", "80, 443", compactApacheStartButton, compactApacheStopButton, compactApacheRestartButton),
            buildCleanServiceRow(LABEL_SERVICE_NGINX, "Web Server", compactNginxStatusValue, "1.28.x", "80", compactNginxStartButton, compactNginxStopButton, compactNginxRestartButton),
            buildCleanServiceRow(LABEL_SERVICE_MYSQL, "Database", compactMysqlStatusValue, "8.0.x", "3306", compactMysqlStartButton, compactMysqlStopButton, compactMysqlRestartButton),
            buildCleanServiceRow(LABEL_SERVICE_PHP, "Runtime", compactPhpStatusValue, "8.x", "9000", compactPhpStartButton, compactPhpStopButton, compactPhpRestartButton),
            buildCleanServiceRow(LABEL_SERVICE_MAILPIT, "Mail Testing", compactMailpitStatusValue, "1.22.x", "1025, 8025", compactMailpitStartButton, compactMailpitStopButton, compactMailpitRestartButton),
            buildManageServicesLink()
        );
        return card;
    }

    private Parent buildServiceHeaderRow() {
        HBox row = new HBox(10);
        row.getStyleClass().add(STYLE_SERVICE_HEADER_ROW);
        row.getChildren().addAll(
            buildTableLabel("Service", 250),
            buildTableLabel(LABEL_ROLE, 150),
            buildTableLabel(LABEL_SERVICE_STATUS, 150),
            buildTableLabel(LABEL_VERSION, 120),
            buildTableLabel(LABEL_PORTS, 150),
            buildTableLabel(LABEL_CONTROLS, 170)
        );
        return row;
    }

    private Label buildTableLabel(String text, double width) {
        Label label = new Label(text);
        label.getStyleClass().add(STYLE_FIELD_LABEL);
        label.setMinWidth(width);
        label.setPrefWidth(width);
        return label;
    }

    private Parent buildCleanServiceRow(String serviceName, String role, Label statusLabel, String version, String ports, Button startButton, Button stopButton, Button restartButton) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_SERVICE_TABLE_ROW);

        HBox serviceBox = new HBox(10);
        serviceBox.setAlignment(Pos.CENTER_LEFT);
        serviceBox.setMinWidth(250);
        serviceBox.setPrefWidth(250);
        Label icon = new Label(serviceName.substring(0, 1));
        icon.getStyleClass().add(STYLE_SERVICE_ICON);
        VBox serviceText = new VBox(2);
        Label name = new Label(serviceName);
        name.getStyleClass().add(STYLE_COMPACT_SERVICE_NAME);
        Label sub = new Label(role);
        sub.getStyleClass().add(STYLE_COMPACT_SERVICE_META);
        serviceText.getChildren().addAll(name, sub);
        serviceBox.getChildren().addAll(icon, serviceText);

        Label roleLabel = new Label(role);
        roleLabel.getStyleClass().add(STYLE_SERVICE_COL);
        roleLabel.setMinWidth(150);
        roleLabel.setPrefWidth(150);

        statusLabel.getStyleClass().add(STYLE_COMPACT_SERVICE_STATUS);
        statusLabel.setMinWidth(150);
        statusLabel.setPrefWidth(150);

        Label versionLabel = new Label(version);
        versionLabel.getStyleClass().add(STYLE_SERVICE_COL);
        versionLabel.setMinWidth(120);
        versionLabel.setPrefWidth(120);

        Label portsLabel = new Label(ports);
        portsLabel.getStyleClass().add(STYLE_SERVICE_COL);
        portsLabel.setMinWidth(150);
        portsLabel.setPrefWidth(150);

        HBox actions = new HBox(8);
        actions.setMinWidth(170);
        actions.setPrefWidth(170);
        actions.setAlignment(Pos.CENTER_LEFT);
        styleCompactServiceButton(startButton, STYLE_COMPACT_SERVICE_START);
        styleCompactServiceButton(stopButton, STYLE_COMPACT_SERVICE_STOP);
        styleCompactServiceButton(restartButton, STYLE_COMPACT_SERVICE_RESTART);
        startButton.setText("Start");
        stopButton.setText("Stop");
        restartButton.setText("Restart");
        actions.getChildren().addAll(startButton, stopButton, restartButton);

        row.getChildren().addAll(serviceBox, roleLabel, statusLabel, versionLabel, portsLabel, actions);
        return row;
    }

    private Parent buildManageServicesLink() {
        HBox box = new HBox();
        box.setAlignment(Pos.CENTER);
        manageServicesButton.getStyleClass().add(STYLE_BADGE);
        box.getChildren().add(manageServicesButton);
        return box;
    }

    private Parent buildDashboardBottomGrid() {
        HBox grid = new HBox(14);
        grid.getStyleClass().add(STYLE_BOTTOM_GRID);
        grid.getChildren().addAll(
            buildCleanActivityLogPanel(),
            buildSystemOverviewPanel()
        );
        return grid;
    }

    private Parent buildCleanQuickActionsPanel() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        HBox.setHgrow(card, Priority.ALWAYS);
        card.setMaxWidth(Double.MAX_VALUE);

        Label title = new Label(LABEL_QUICK_ACTION_BAR);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label("Common tasks to speed up your workflow");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);

        FlowPane actions = new FlowPane();
        actions.setHgap(10);
        actions.setVgap(10);
        styleQuickTile(quickStartAllButton, STYLE_PRIMARY_BUTTON);
        styleQuickTile(quickStopAllButton, STYLE_DANGER_BUTTON);
        styleQuickTile(quickWebButton, STYLE_SECONDARY_BUTTON);
        styleQuickTile(quickDatabaseButton, STYLE_SECONDARY_BUTTON);
        styleQuickTile(quickTerminalButton, STYLE_SECONDARY_BUTTON);
        styleQuickTile(quickRootButton, STYLE_SECONDARY_BUTTON);
        styleQuickTile(quickLogsButton, STYLE_SECONDARY_BUTTON);
        actions.getChildren().addAll(quickStartAllButton, quickStopAllButton, quickWebButton, quickDatabaseButton, quickTerminalButton, quickRootButton, quickLogsButton);

        card.getChildren().addAll(title, subtitle, actions);
        return card;
    }

    private void styleQuickTile(Button button, String styleClass) {
        button.getStyleClass().add(STYLE_QUICK_TILE);
        button.getStyleClass().add(styleClass);
        button.setMinWidth(104);
    }

    private Parent buildCleanActivityLogPanel() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        HBox.setHgrow(card, Priority.ALWAYS);
        card.setMaxWidth(Double.MAX_VALUE);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_LOG_TITLE);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        viewAllLogsButton.getStyleClass().add(STYLE_LINK_BUTTON);
        header.getChildren().addAll(title, spacer, viewAllLogsButton);

        logArea.getStyleClass().add(STYLE_LOG);
        logArea.setEditable(false);
        logArea.setPrefHeight(145);
        ensureLogInitialized();

        card.getChildren().addAll(header, logArea);
        return card;
    }

    private Parent buildSystemOverviewPanel() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        HBox.setHgrow(card, Priority.ALWAYS);
        card.setMaxWidth(Double.MAX_VALUE);

        Label title = new Label(LABEL_SYSTEM_OVERVIEW);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        card.getChildren().addAll(
            title,
            buildInfoRow(LABEL_OS, "Windows 11 Pro"),
            buildInfoRow(LABEL_UPTIME, "0d 02h 18m"),
            buildInfoRow(LABEL_WORKSPACE, VALUE_COMPACT_ROOT),
            buildInfoRowWithValue(LABEL_WEB_SERVER_MODE, activeWebServerValue),
            buildInfoRow(LABEL_SHARED_WWW, DesktopApiConfig.WEB_SERVER_SHARED_DOCUMENT_ROOT),
            buildWebServerModeActions(),
            buildInfoRow(LABEL_COMPACT_AGENT, VALUE_COMPACT_AGENT),
            buildInfoLink(LABEL_SYSTEM_SETTINGS)
        );
        return card;
    }

    private Parent buildInfoRow(String labelText, String valueText) {
        HBox row = new HBox(12);
        row.getStyleClass().add(STYLE_INFO_ROW);
        Label label = new Label(labelText);
        label.getStyleClass().add(STYLE_CARD_TEXT);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_SUMMARY_VALUE);
        row.getChildren().addAll(label, spacer, value);
        return row;
    }

    private Parent buildInfoRowWithValue(String labelText, Label value) {
        HBox row = new HBox(12);
        row.getStyleClass().add(STYLE_INFO_ROW);
        Label label = new Label(labelText);
        label.getStyleClass().add(STYLE_CARD_TEXT);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        value.getStyleClass().add(STYLE_SUMMARY_VALUE);
        row.getChildren().addAll(label, spacer, value);
        return row;
    }

    private Parent buildWebServerModeActions() {
        HBox row = new HBox(8);
        row.setAlignment(Pos.CENTER_LEFT);
        selectApacheWebServerButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        selectNginxWebServerButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        row.getChildren().addAll(selectApacheWebServerButton, selectNginxWebServerButton);
        return row;
    }

    private Parent buildInfoLink(String text) {
        HBox row = new HBox();
        row.setAlignment(Pos.CENTER_LEFT);
        systemSettingsButton.setText(text);
        systemSettingsButton.getStyleClass().add(STYLE_BADGE);
        row.getChildren().add(systemSettingsButton);
        return row;
    }

    private Parent buildCompactServicePanel() {
        VBox panel = new VBox(10);
        panel.getStyleClass().add(STYLE_COMPACT_SERVICE_PANEL);
        HBox.setHgrow(panel, Priority.ALWAYS);
        panel.setMaxWidth(Double.MAX_VALUE);

        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_COMPACT_SERVICES);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        compactServiceRefreshButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(title, spacer, compactServiceRefreshButton);

        panel.getChildren().addAll(
            header,
            buildCompactServiceRow(LABEL_SERVICE_APACHE, META_APACHE, compactApacheStatusValue, compactApacheStartButton, compactApacheStopButton, compactApacheRestartButton),
            buildCompactServiceRow(LABEL_SERVICE_NGINX, META_NGINX, compactNginxStatusValue, compactNginxStartButton, compactNginxStopButton, compactNginxRestartButton),
            buildCompactServiceRow(LABEL_SERVICE_MYSQL, META_MYSQL, compactMysqlStatusValue, compactMysqlStartButton, compactMysqlStopButton, compactMysqlRestartButton),
            buildCompactServiceRow(LABEL_SERVICE_PHP, META_PHP, compactPhpStatusValue, compactPhpStartButton, compactPhpStopButton, compactPhpRestartButton),
            buildCompactServiceRow(LABEL_SERVICE_MAILPIT, META_MAILPIT, compactMailpitStatusValue, compactMailpitStartButton, compactMailpitStopButton, compactMailpitRestartButton)
        );
        return panel;
    }

    private Parent buildCompactServiceRow(
        String serviceName,
        String meta,
        Label statusLabel,
        Button startButton,
        Button stopButton,
        Button restartButton
    ) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_COMPACT_SERVICE_ROW);

        Label dot = new Label("●");
        dot.getStyleClass().add(STYLE_COMPACT_SERVICE_DOT);

        VBox textBox = new VBox(2);
        Label name = new Label(serviceName);
        name.getStyleClass().add(STYLE_COMPACT_SERVICE_NAME);
        Label metaLabel = new Label(meta);
        metaLabel.getStyleClass().add(STYLE_COMPACT_SERVICE_META);
        textBox.getChildren().addAll(name, metaLabel);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        statusLabel.getStyleClass().add(STYLE_COMPACT_SERVICE_STATUS);

        HBox actions = new HBox(8);
        actions.setAlignment(Pos.CENTER_RIGHT);
        actions.getStyleClass().add(STYLE_COMPACT_SERVICE_ACTIONS);
        styleCompactServiceButton(startButton, STYLE_COMPACT_SERVICE_START);
        styleCompactServiceButton(stopButton, STYLE_COMPACT_SERVICE_STOP);
        styleCompactServiceButton(restartButton, STYLE_COMPACT_SERVICE_RESTART);
        actions.getChildren().addAll(startButton, stopButton, restartButton);

        row.getChildren().addAll(dot, textBox, spacer, statusLabel, actions);
        return row;
    }

    private void styleCompactServiceButton(Button button, String styleClass) {
        button.getStyleClass().add(STYLE_ACTION_BUTTON);
        button.getStyleClass().add(styleClass);
        button.setMinWidth(72);
    }

    private Parent buildCompactQuickDock() {
        VBox dock = new VBox(10);
        dock.getStyleClass().add(STYLE_COMPACT_QUICK_DOCK);
        dock.setMaxWidth(Double.MAX_VALUE);

        Label title = new Label(LABEL_QUICK_ACTION_BAR);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_QUICK_ACTION_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);

        FlowPane actions = new FlowPane();
        actions.setHgap(10);
        actions.setVgap(10);

        quickStartAllButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickStopAllButton.getStyleClass().add(STYLE_DANGER_BUTTON);
        quickWebButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickDatabaseButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickMailpitButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickTerminalButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickRootButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickProjectsButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickLogsButton.getStyleClass().add(STYLE_ACTION_BUTTON);

        actions.getChildren().addAll(
            quickStartAllButton,
            quickStopAllButton,
            quickWebButton,
            quickDatabaseButton,
            quickMailpitButton,
            quickTerminalButton,
            quickRootButton,
            quickProjectsButton,
            quickLogsButton
        );

        dock.getChildren().addAll(title, subtitle, actions);
        return dock;
    }

    private Parent buildCompactToolDock() {
        VBox dock = new VBox(10);
        dock.getStyleClass().add(STYLE_COMPACT_TOOL_DOCK);
        dock.setMaxWidth(Double.MAX_VALUE);

        Label title = new Label(LABEL_COMPACT_TOOLS);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_COMPACT_TOOL_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);

        FlowPane actions = new FlowPane();
        actions.setHgap(10);
        actions.setVgap(10);

        quickBinButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickCmderButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickGitBashButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickNotepadButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickNgrokButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickComposerButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        quickYarnButton.getStyleClass().add(STYLE_ACTION_BUTTON);

        actions.getChildren().addAll(
            quickBinButton,
            quickCmderButton,
            quickGitBashButton,
            quickNotepadButton,
            quickNgrokButton,
            quickComposerButton,
            quickYarnButton
        );

        dock.getChildren().addAll(title, subtitle, actions);
        return dock;
    }

    private Parent buildHero() {
        VBox hero = new VBox(14);
        hero.getStyleClass().add(STYLE_HERO);

        Label title = new Label(HERO_TITLE_TEXT);
        title.getStyleClass().add(STYLE_HERO_TITLE);

        Label subtitle = new Label(HERO_SUBTITLE_TEXT);
        subtitle.getStyleClass().add(STYLE_HERO_SUBTITLE);
        subtitle.setWrapText(true);

        HBox actions = new HBox(10);
        startAgentButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        stopAgentButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        stopAgentButton.getStyleClass().add(STYLE_DANGER_BUTTON);
        restartAgentButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        openPanelButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        checkStatusButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        actions.getChildren().addAll(startAgentButton, stopAgentButton, restartAgentButton, openPanelButton, checkStatusButton);

        hero.getChildren().addAll(title, subtitle, actions);
        return hero;
    }

    private Parent buildStatusCards() {
        HBox cards = new HBox(14);
        cards.getChildren().addAll(
            buildMetricCard("Agent", "127.0.0.1:8751", "Local FastAPI bridge"),
            buildMetricCard("Workflow", "Plan + Dry Run", "Profile based Nginx or Apache action"),
            buildMetricCard("Safety", "Locks + Rollback", "Run tracking and guard layer")
        );
        return cards;
    }

    private VBox buildMetricCard(String titleText, String valueText, String descriptionText) {
        VBox card = new VBox(8);
        card.getStyleClass().add(STYLE_CARD);
        HBox.setHgrow(card, Priority.ALWAYS);
        card.setMaxWidth(Double.MAX_VALUE);

        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_CARD_TEXT);

        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_CARD_TITLE);

        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);

        card.getChildren().addAll(title, value, description);
        return card;
    }

    private Parent buildQuickActionPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);

        VBox titleBox = new VBox(4);
        Label title = new Label(LABEL_QUICK_ACTION_BAR);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_QUICK_ACTION_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);
        header.getChildren().add(titleBox);

        FlowPane actions = new FlowPane();
        actions.getStyleClass().add(STYLE_ACTION_GRID);
        actions.setHgap(10);
        actions.setVgap(10);

        quickStartAllButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickStopAllButton.getStyleClass().add(STYLE_DANGER_BUTTON);
        quickWebButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickDatabaseButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        quickMailpitButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickTerminalButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickRootButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickProjectsButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickLogsButton.getStyleClass().add(STYLE_ACTION_BUTTON);

        actions.getChildren().addAll(
            quickStartAllButton,
            quickStopAllButton,
            quickWebButton,
            quickDatabaseButton,
            quickMailpitButton,
            quickTerminalButton,
            quickRootButton,
            quickProjectsButton,
            quickLogsButton
        );

        card.getChildren().addAll(header, actions);
        return card;
    }

    private Parent buildServiceManagerPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);

        VBox titleBox = new VBox(4);
        Label title = new Label(LABEL_SERVICE_MANAGER_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_SERVICE_MANAGER_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        serviceListButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(titleBox, spacer, serviceListButton);

        FlowPane serviceStrip = new FlowPane();
        serviceStrip.getStyleClass().add(STYLE_SUMMARY_STRIP);
        serviceStrip.setHgap(10);
        serviceStrip.setVgap(10);
        serviceStrip.getChildren().addAll(
            buildSummaryPill(LABEL_SERVICE_APACHE_STATUS, serviceApacheStatusValue),
            buildSummaryPill(LABEL_SERVICE_NGINX_STATUS, serviceNginxStatusValue),
            buildSummaryPill(LABEL_SERVICE_MYSQL_STATUS, serviceMysqlStatusValue),
            buildSummaryPill(LABEL_SERVICE_PHP_STATUS, servicePhpStatusValue),
            buildSummaryPill(LABEL_SERVICE_MAILPIT_STATUS, serviceMailpitStatusValue)
        );

        VBox rows = new VBox(10);
        rows.getChildren().addAll(
            buildServiceRow(LABEL_SERVICE_APACHE, apacheStatusButton, apachePreflightButton, apacheStartButton, apacheStopButton, apacheRestartButton),
            buildServiceRow(LABEL_SERVICE_NGINX, nginxStatusButton, nginxPreflightButton, nginxStartButton, nginxStopButton, nginxRestartButton),
            buildServiceRow(LABEL_SERVICE_MYSQL, mysqlStatusButton, mysqlPreflightButton, mysqlStartButton, mysqlStopButton, mysqlRestartButton),
            buildServiceRow(LABEL_SERVICE_PHP, phpStatusButton, phpPreflightButton, phpStartButton, phpStopButton, phpRestartButton),
            buildServiceRow(LABEL_SERVICE_MAILPIT, mailpitStatusButton, mailpitPreflightButton, mailpitStartButton, mailpitStopButton, mailpitRestartButton)
        );

        card.getChildren().addAll(header, serviceStrip, rows);
        return card;
    }

    private Parent buildServiceRow(String serviceName, Button statusButton, Button preflightButton, Button startButton, Button stopButton, Button restartButton) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);

        Label name = new Label(serviceName);
        name.getStyleClass().add(STYLE_CARD_TITLE);
        name.setMinWidth(110);

        statusButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        preflightButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        startButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        stopButton.getStyleClass().add(STYLE_DANGER_BUTTON);
        restartButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);

        row.getChildren().addAll(name, statusButton, preflightButton, startButton, stopButton, restartButton);
        return row;
    }

    private Parent buildRuntimeManagerPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);

        VBox titleBox = new VBox(4);
        Label title = new Label(LABEL_RUNTIME_MANAGER_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_RUNTIME_MANAGER_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        runtimeListButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        runtimeScanBinButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(titleBox, spacer, runtimeScanBinButton, runtimeListButton);

        FlowPane runtimeStrip = new FlowPane();
        runtimeStrip.getStyleClass().add(STYLE_SUMMARY_STRIP);
        runtimeStrip.setHgap(10);
        runtimeStrip.setVgap(10);
        runtimeStrip.getChildren().addAll(
            buildSummaryPill(LABEL_RUNTIME_COUNT, runtimeCountValue),
            buildSummaryPill(LABEL_RUNTIME_PHP_ACTIVE, runtimePhpActiveValue),
            buildSummaryPill(LABEL_RUNTIME_NODE_ACTIVE, runtimeNodeActiveValue),
            buildSummaryPill(LABEL_RUNTIME_PYTHON_ACTIVE, runtimePythonActiveValue)
        );

        VBox rows = new VBox(10);
        rows.getChildren().addAll(
            buildRuntimeRow(LABEL_RUNTIME_APACHE, runtimeApacheCodeField, runtimeApacheFolderField, runtimeApacheActiveButton, runtimeApacheActivateButton, runtimeApacheActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_NGINX, runtimeNginxCodeField, runtimeNginxFolderField, runtimeNginxActiveButton, runtimeNginxActivateButton, runtimeNginxActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_MYSQL, runtimeMysqlCodeField, runtimeMysqlFolderField, runtimeMysqlActiveButton, runtimeMysqlActivateButton, runtimeMysqlActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_PHP, runtimePhpCodeField, runtimePhpFolderField, runtimePhpActiveButton, runtimePhpActivateButton, runtimePhpActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_NODE, runtimeNodeCodeField, runtimeNodeFolderField, runtimeNodeActiveButton, runtimeNodeActivateButton, runtimeNodeActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_PYTHON, runtimePythonCodeField, runtimePythonFolderField, runtimePythonActiveButton, runtimePythonActivateButton, runtimePythonActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_MEMCACHED, runtimeMemcachedCodeField, runtimeMemcachedFolderField, runtimeMemcachedActiveButton, runtimeMemcachedActivateButton, runtimeMemcachedActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_REDIS, runtimeRedisCodeField, runtimeRedisFolderField, runtimeRedisActiveButton, runtimeRedisActivateButton, runtimeRedisActivatePortableButton),
            buildRuntimeRow(LABEL_RUNTIME_MAILPIT, runtimeMailpitCodeField, runtimeMailpitFolderField, runtimeMailpitActiveButton, runtimeMailpitActivateButton, runtimeMailpitActivatePortableButton)
        );

        card.getChildren().addAll(header, runtimeStrip, rows);
        return card;
    }

    private Parent buildRuntimeRow(String runtimeName, TextField codeField, TextField folderField, Button activeButton, Button activateButton, Button activatePortableButton) {
        HBox row = new HBox(10);
        row.setAlignment(Pos.CENTER_LEFT);

        Label name = new Label(runtimeName);
        name.getStyleClass().add(STYLE_CARD_TITLE);
        name.setMinWidth(110);

        VBox codeBox = buildInputBox(LABEL_RUNTIME_CODE, codeField, 150);
        VBox folderBox = buildInputBox(LABEL_RUNTIME_FOLDER, folderField, 240);
        activeButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        activateButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        activatePortableButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);

        row.getChildren().addAll(name, codeBox, folderBox, activeButton, activateButton, activatePortableButton);
        return row;
    }


    public void showPackageCenterDialog() {
        Dialog<Void> dialog = new Dialog<>();
        dialog.setTitle(LABEL_PACKAGE_CENTER_DIALOG_TITLE);
        dialog.getDialogPane().getStyleClass().add("jhoster-settings-dialog");

        ButtonType closeButton = new ButtonType("Close", ButtonBar.ButtonData.CANCEL_CLOSE);
        dialog.getDialogPane().getButtonTypes().add(closeButton);
        dialog.getDialogPane().setContent(buildPackageCenterInlinePanel());
        dialog.showAndWait();
    }

    private Parent buildPackageSelectionPanel() {
        HBox panel = new HBox(12);
        panel.getStyleClass().add("jhoster-package-selection-panel");
        panel.setAlignment(Pos.CENTER_LEFT);

        VBox titleBox = new VBox(3);
        Label title = new Label("Selected Package");
        title.getStyleClass().add(STYLE_FIELD_LABEL);
        packageSelectedTitleValue.getStyleClass().add(STYLE_SUMMARY_VALUE);
        titleBox.getChildren().addAll(title, packageSelectedTitleValue);

        VBox codeBox = new VBox(3);
        Label code = new Label("Package Code");
        code.getStyleClass().add(STYLE_FIELD_LABEL);
        packageSelectedCodeValue.getStyleClass().add(STYLE_CARD_TEXT);
        packageSelectedCodeValue.setWrapText(true);
        codeBox.getChildren().addAll(code, packageSelectedCodeValue);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        setPackageStatusBadge(packageSelectedStatusValue, packageSelectedStatusValue.getText());

        HBox actions = new HBox(8);
        actions.setAlignment(Pos.CENTER_RIGHT);
        packagePlanButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        packageDownloadButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        packageInstallButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        packagePlanButton.setText("1 Plan");
        packageDownloadButton.setText("2 Download");
        packageInstallButton.setText("3 Install");
        actions.getChildren().addAll(packagePlanButton, packageDownloadButton, packageInstallButton);

        panel.getChildren().addAll(titleBox, codeBox, spacer, packageSelectedStatusValue, actions);
        return panel;
    }

    private Parent buildPackagePathStrip() {
        FlowPane strip = new FlowPane(10, 8);
        strip.getStyleClass().add("jhoster-package-path-strip");
        strip.getChildren().addAll(
            buildPackageInfoPill("Install Target", "E:\\JHoster\\bin"),
            buildPackageInfoPill("Download Cache", "E:\\JHoster\\cache\\downloads"),
            buildPackageInfoPill("Registry", "data/jhoster/package_download_registry.json"),
            buildPackageInfoPill("Mode", "Manifest driven")
        );
        return strip;
    }

    private Parent buildPackageInfoPill(String titleText, String valueText) {
        VBox pill = new VBox(3);
        pill.getStyleClass().add("jhoster-package-info-pill");
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_FIELD_LABEL);
        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_CARD_TEXT);
        value.setWrapText(true);
        pill.getChildren().addAll(title, value);
        return pill;
    }

    private Parent buildPackageCategoryTabs() {
        VBox sections = new VBox(14);
        sections.getStyleClass().add("jhoster-package-category-sections");
        sections.getChildren().addAll(
            buildPackageCategorySection("Web Servers",
                buildPackageCenterCard("Apache", "apache-httpd-vs17", "Public 80/443 web engine", "apache-httpd-vs17", "Ready"),
                buildPackageCenterCard("Nginx", "nginx-windows-stable", "Alternative public web engine", "nginx-windows-stable", "Ready")
            ),
            buildPackageCategorySection("Languages",
                buildPackageCenterCard("PHP", "php-8.3-windows-x64", "Runtime for PHP projects", "php-8.3-windows-x64", "Ready"),
                buildPackageCenterCard("Node.js", "nodejs-windows-x64", "JavaScript runtime package", "nodejs-windows-x64", "Planned"),
                buildPackageCenterCard("Python", "python-windows-x64", "Python runtime package", "python-windows-x64", "Planned")
            ),
            buildPackageCategorySection("Databases",
                buildPackageCenterCard("MySQL", "mysql-windows-x64", "Database service package", "mysql-windows-x64", "Disabled"),
                buildPackageCenterCard("Redis", "redis-windows-x64", "Cache service package", "redis-windows-x64", "Planned")
            ),
            buildPackageCategorySection("Tools",
                buildPackageCenterCard("Mailpit", "mailpit-windows-amd64", "Local mail testing service", "mailpit-windows-amd64", "Ready"),
                buildPackageCenterCard("HeidiSQL", "heidisql-portable", "Portable database client", "heidisql-portable", "Disabled"),
                buildPackageCenterCard("Composer", "composer-portable", "PHP dependency manager", "composer-portable", "Planned")
            )
        );
        return sections;
    }

    private Parent buildPackageCategorySection(String titleText, Parent... cards) {
        VBox section = new VBox(8);
        section.getStyleClass().add("jhoster-package-category-section");
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        FlowPane packageGrid = new FlowPane(10, 10);
        packageGrid.getStyleClass().add("jhoster-package-center-grid");
        packageGrid.getChildren().addAll(cards);
        section.getChildren().addAll(title, packageGrid);
        return section;
    }

    private Parent buildPackageCenterCard(String titleText, String valueText, String descriptionText, String packageCode, String statusText) {
        VBox card = new VBox(7);
        card.getStyleClass().add("jhoster-package-center-card");
        card.setPrefWidth(230);
        card.setOnMouseClicked(event -> selectPackageCode(packageCode, titleText));

        HBox titleRow = new HBox(8);
        titleRow.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SUMMARY_LABEL);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        Label status = new Label(statusText);
        status.getStyleClass().add("jhoster-package-card-status");
        status.getStyleClass().add(packageStatusStyle(statusText));
        titleRow.getChildren().addAll(title, spacer, status);

        Label value = new Label(valueText);
        value.getStyleClass().add(STYLE_SUMMARY_VALUE);
        value.setWrapText(true);
        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);

        Label action = new Label("Click card to select");
        action.getStyleClass().add("jhoster-package-card-action");
        card.getChildren().addAll(titleRow, value, description, action);
        return card;
    }

    private void selectPackageCode(String packageCode, String titleText) {
        packageCodeField.setText(packageCode);
        packageSelectedTitleValue.setText(titleText);
        packageSelectedCodeValue.setText(packageCode);
        setPackageStatusBadge(packageSelectedStatusValue, "Selected");
        packageResultArea.appendText("Selected package: " + titleText + " -> " + packageCode + "\n");
    }

    private void setPackageStatusBadge(Label label, String statusText) {
        label.setText(statusText == null || statusText.isBlank() ? "Idle" : statusText);
        label.getStyleClass().removeAll(
            "jhoster-package-status-ready",
            "jhoster-package-status-planned",
            "jhoster-package-status-disabled",
            "jhoster-package-status-selected",
            "jhoster-package-status-downloaded",
            "jhoster-package-status-installed",
            "jhoster-package-status-updated"
        );
        if (!label.getStyleClass().contains("jhoster-package-status-badge")) {
            label.getStyleClass().add("jhoster-package-status-badge");
        }
        label.getStyleClass().add(packageStatusStyle(label.getText()));
    }

    private String packageStatusStyle(String statusText) {
        String normalized = statusText == null ? "" : statusText.toLowerCase();
        if (normalized.contains("install")) {
            return "jhoster-package-status-installed";
        }
        if (normalized.contains("download")) {
            return "jhoster-package-status-downloaded";
        }
        if (normalized.contains("select")) {
            return "jhoster-package-status-selected";
        }
        if (normalized.contains("disable")) {
            return "jhoster-package-status-disabled";
        }
        if (normalized.contains("plan")) {
            return "jhoster-package-status-planned";
        }
        if (normalized.contains("ready")) {
            return "jhoster-package-status-ready";
        }
        return "jhoster-package-status-updated";
    }

    private void updateSelectedPackageStatusFromSummary(PackageDownloadSummary summary) {
        String title = summary.getTitle().toLowerCase();
        String description = summary.getDescription().toLowerCase();
        String combined = title + " " + description;
        if (combined.contains("install")) {
            setPackageStatusBadge(packageSelectedStatusValue, "Installed");
            return;
        }
        if (combined.contains("download")) {
            setPackageStatusBadge(packageSelectedStatusValue, "Downloaded");
            return;
        }
        if (combined.contains("plan")) {
            setPackageStatusBadge(packageSelectedStatusValue, "Planned");
            return;
        }
        if (combined.contains("catalog")) {
            setPackageStatusBadge(packageSelectedStatusValue, "Ready");
        }
    }

    private Parent buildPackageDownloaderPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);
        VBox titleBox = new VBox(4);
        Label title = new Label(LABEL_PACKAGE_INSTALLER_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_PACKAGE_INSTALLER_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);
        header.getChildren().add(titleBox);

        HBox form = new HBox(10);
        form.setAlignment(Pos.CENTER_LEFT);
        VBox codeBox = new VBox(4);
        Label codeLabel = new Label(LABEL_PACKAGE_CODE);
        codeLabel.getStyleClass().add(STYLE_FIELD_LABEL);
        packageCodeField.getStyleClass().add(STYLE_INPUT);
        packageCodeField.setPromptText("Select a card or type package code");
        packageCodeField.setPrefWidth(320);
        codeBox.getChildren().addAll(codeLabel, packageCodeField);

        packageCatalogButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        packageCatalogButton.setText("Refresh Catalog");
        form.getChildren().addAll(codeBox, packageCatalogButton);

        packageResultArea.getStyleClass().add(STYLE_LOG);
        packageResultArea.setEditable(false);
        packageResultArea.setPrefHeight(165);
        if (packageResultArea.getText() == null || packageResultArea.getText().isBlank()) {
            packageResultArea.setText("Select a package code, then plan, download or install.\nDefault: nginx-windows-stable\n");
        }

        card.getChildren().addAll(header, form, packageResultArea);
        return card;
    }

    private Parent buildQuickAppPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-quick-app-card");

        HBox header = new HBox(12);
        header.setAlignment(Pos.CENTER_LEFT);

        VBox titleBox = new VBox(4);
        Label title = new Label(LABEL_QUICK_APP_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label(LABEL_QUICK_APP_SUBTITLE);
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        subtitle.setWrapText(true);
        titleBox.getChildren().addAll(title, subtitle);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        quickAppTemplatesButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(titleBox, spacer, quickAppTemplatesButton);

        FlowPane strip = new FlowPane();
        strip.getStyleClass().add(STYLE_SUMMARY_STRIP);
        strip.setHgap(10);
        strip.setVgap(10);
        strip.getChildren().addAll(
            buildSummaryPill(LABEL_QUICK_APP_TEMPLATE_COUNT, quickAppTemplateCountValue),
            buildSummaryPill(LABEL_QUICK_APP_LAST_PROJECT, quickAppLastProjectValue),
            buildSummaryPill(LABEL_QUICK_APP_LAST_TEMPLATE, quickAppLastTemplateValue),
            buildSummaryPill(LABEL_QUICK_APP_LAST_STATUS, quickAppLastStatusValue),
            buildSummaryPill(LABEL_QUICK_APP_STACK, quickAppStackSummaryValue),
            buildSummaryPill("Provisioning", quickAppProvisioningSummaryValue),
            buildSummaryPill("Database", quickAppDatabaseSummaryValue),
            buildSummaryPill(LABEL_HOSTS_AUTO_STATUS, quickHostsAutoHealthValue)
        );

        FlowPane formGrid = new FlowPane();
        formGrid.getStyleClass().add(STYLE_FORM_GRID);
        formGrid.setHgap(10);
        formGrid.setVgap(10);
        formGrid.getChildren().addAll(
            buildInputBox(LABEL_QUICK_APP_PROJECT_CODE, quickAppProjectCodeField, 160),
            buildInputBox(LABEL_QUICK_APP_PROJECT_NAME, quickAppProjectNameField, 180),
            buildInputBox(LABEL_QUICK_APP_TEMPLATE_CODE, quickAppTemplateCodeField, 150),
            buildInputBox(LABEL_QUICK_APP_DOMAIN, quickAppDomainField, 180),
            buildInputBox(LABEL_QUICK_APP_PORT, quickAppPortField, 80)
        );

        Label hostsAutoHint = new Label(LABEL_QUICK_APP_HOSTS_AUTO);
        hostsAutoHint.getStyleClass().add(STYLE_CARD_TEXT);
        hostsAutoHint.setWrapText(true);

        FlowPane actions = new FlowPane();
        actions.getStyleClass().add(STYLE_ACTION_GRID);
        actions.setHgap(10);
        actions.setVgap(10);
        quickHostsAutoInspectButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickAppPlanButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        quickAppCreateButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        actions.getChildren().addAll(quickHostsAutoInspectButton, quickAppPlanButton, quickAppCreateButton);

        card.getChildren().addAll(header, strip, formGrid, buildQuickAppStackSelectionPanel(), hostsAutoHint, actions);
        return card;
    }

    private Parent buildQuickAppStackSelectionPanel() {
        VBox wrapper = new VBox(10);
        wrapper.getStyleClass().add(STYLE_STACK_SELECTOR);

        HBox titleRow = new HBox(10);
        titleRow.setAlignment(Pos.CENTER_LEFT);
        Label title = new Label(LABEL_QUICK_APP_STACK);
        title.getStyleClass().add(STYLE_CARD_TITLE);
        Label hint = new Label(LABEL_QUICK_APP_STACK_HINT);
        hint.getStyleClass().add(STYLE_STACK_HINT);
        hint.setWrapText(true);
        titleRow.getChildren().add(title);

        HBox webServerRow = new HBox(10);
        webServerRow.setAlignment(Pos.CENTER_LEFT);
        webServerRow.getStyleClass().add("jhoster-stack-webserver-row");
        Label webServerLabel = new Label(LABEL_QUICK_APP_WEB_SERVER);
        webServerLabel.getStyleClass().add(STYLE_FIELD_LABEL);
        quickAppApacheRadio.getStyleClass().add(STYLE_STACK_OPTION);
        quickAppNginxRadio.getStyleClass().add(STYLE_STACK_OPTION);
        webServerRow.getChildren().addAll(webServerLabel, quickAppApacheRadio, quickAppNginxRadio);

        FlowPane serviceRow = new FlowPane();
        serviceRow.getStyleClass().add("jhoster-stack-service-row");
        serviceRow.setHgap(10);
        serviceRow.setVgap(10);
        quickAppMysqlCheckBox.getStyleClass().add(STYLE_STACK_OPTION);
        quickAppPhpCheckBox.getStyleClass().add(STYLE_STACK_OPTION);
        quickAppMailpitCheckBox.getStyleClass().add(STYLE_STACK_OPTION);
        serviceRow.getChildren().addAll(quickAppMysqlCheckBox, quickAppPhpCheckBox, quickAppMailpitCheckBox);

        wrapper.getChildren().addAll(titleRow, hint, webServerRow, serviceRow);
        return wrapper;
    }

    private Parent buildWorkflowPanel() {
        VBox card = new VBox(14);
        card.getStyleClass().add(STYLE_CARD);

        Label title = new Label(LABEL_WORKFLOW_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        FlowPane formGrid = new FlowPane();
        formGrid.getStyleClass().add(STYLE_FORM_GRID);
        formGrid.setHgap(10);
        formGrid.setVgap(10);
        formGrid.getChildren().addAll(
            buildInputBox(LABEL_PROJECT_CODE, workflowProjectCodeField, 170),
            buildInputBox(LABEL_DOMAIN, workflowDomainField, 190),
            buildInputBox(LABEL_PORT, workflowPortField, 90),
            buildInputBox(LABEL_TARGET_DIR, workflowTargetDirField, 260)
        );

        FlowPane actions = new FlowPane();
        actions.getStyleClass().add(STYLE_ACTION_GRID);
        actions.setHgap(10);
        actions.setVgap(10);
        workflowDryRunButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);
        workflowPlanButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        workflowProfileButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        workflowRunsButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        workflowLocksButton.getStyleClass().add(STYLE_ACTION_BUTTON);
        actions.getChildren().addAll(workflowDryRunButton, workflowPlanButton, workflowProfileButton, workflowRunsButton, workflowLocksButton);

        card.getChildren().addAll(title, buildWorkflowSummaryStrip(), formGrid, actions);
        return card;
    }

    private Parent buildWorkflowSummaryStrip() {
        FlowPane strip = new FlowPane();
        strip.getStyleClass().add(STYLE_SUMMARY_STRIP);
        strip.setHgap(10);
        strip.setVgap(10);
        strip.getChildren().addAll(
            buildSummaryPill(LABEL_SUMMARY_PROFILE, summaryProfileValue),
            buildSummaryPill(LABEL_SUMMARY_STATUS, summaryStatusValue),
            buildSummaryPill(LABEL_SUMMARY_RUN_COUNT, summaryRunCountValue),
            buildSummaryPill(LABEL_SUMMARY_LOCK_COUNT, summaryLockCountValue),
            buildSummaryPill(LABEL_SUMMARY_STEP_COUNT, summaryStepCountValue),
            buildSummaryPill(LABEL_SUMMARY_RUN_ID, summaryRunIdValue)
        );
        return strip;
    }

    private VBox buildSummaryPill(String labelText, Label valueLabel) {
        VBox pill = new VBox(3);
        pill.getStyleClass().add(STYLE_SUMMARY_PILL);

        Label label = new Label(labelText);
        label.getStyleClass().add(STYLE_SUMMARY_LABEL);

        valueLabel.getStyleClass().add(STYLE_SUMMARY_VALUE);
        pill.getChildren().addAll(label, valueLabel);
        return pill;
    }

    private VBox buildInputBox(String labelText, TextField field, double width) {
        VBox box = new VBox(6);
        Label label = new Label(labelText);
        label.getStyleClass().add(STYLE_FIELD_LABEL);
        field.getStyleClass().add(STYLE_INPUT);
        field.setPrefWidth(width);
        box.getChildren().addAll(label, field);
        return box;
    }

    private Parent buildProjectDeliveryPanel() {
        VBox wrapper = new VBox(14);
        wrapper.getChildren().addAll(
            buildInfoCard("Project Delivery", "Open the workspace, inspect project records and repair hosts mappings from one focused page."),
            buildActionCard("Project Actions", quickProjectsButton, quickRootButton, openProjectsButton)
        );
        return wrapper;
    }

    private Parent buildVirtualHostOperationsPanel() {
        VBox wrapper = new VBox(14);
        wrapper.getChildren().addAll(
            buildInfoCard("Virtual Hosts", "Use safe workflow actions first. Raw Apache and Nginx endpoint buttons stay hidden unless Dev Mode is active."),
            buildActionCard("Safe Host Actions", workflowProfileButton, workflowPlanButton, workflowDryRunButton, openVirtualHostsButton)
        );
        return wrapper;
    }

    private Parent buildAppsOperationsPanel() {
        VBox wrapper = new VBox(14);
        wrapper.getChildren().addAll(
            buildInfoCard("App Modules", "Create scaffold apps from the New Site wizard, then inspect the app registry when needed."),
            buildActionCard("App Actions", quickAppTemplatesButton, quickAppPlanButton, openAppsButton)
        );
        return wrapper;
    }

    private Parent buildWorkflowOperationsPanel() {
        return buildInfoCard("Workflow Shortcuts", "Plan and dry-run controls are active in this page. Real publish/reload actions remain isolated from normal mode until the runtime installer layer is complete.");
    }

    private Parent buildToolsOperationsPanel() {
        return buildActionCard("Tool Folders", quickBinButton, quickCmderButton, quickGitBashButton, quickNotepadButton, quickNgrokButton, quickComposerButton, quickYarnButton);
    }

    private Parent buildDiagnosticsOperationsPanel() {
        if (!devModeEnabled) {
            return buildInfoCard(DEV_MODE_REQUIRED_TITLE, DEV_MODE_REQUIRED_TEXT);
        }
        return buildDeveloperOperationsPanel();
    }

    private Parent buildDeveloperModeBanner() {
        VBox banner = new VBox(6);
        banner.getStyleClass().add(STYLE_DEV_BANNER);

        Label title = new Label(DEV_MODE_BANNER_TITLE);
        title.getStyleClass().add(STYLE_DEV_NOTICE_TITLE);

        Label text = new Label(DEV_MODE_BANNER_TEXT);
        text.getStyleClass().add(STYLE_DEV_NOTICE_TEXT);
        text.setWrapText(true);

        banner.getChildren().addAll(title, text);
        return banner;
    }

    private Parent buildDeveloperOperationsPanel() {
        VBox wrapper = new VBox(14);
        wrapper.getChildren().addAll(
            buildActionCard("Core Agent API", openPanelButton, openComponentsButton, openHistoryButton, openCacheButton, openAppsButton, openProcessButton, openServiceAdaptersButton, openLocalPackagesButton),
            buildActionCard("Project and Host API", openProjectsButton, openVirtualHostsButton, openHostsPublishButton, openHostsApplyButton, openWebServerProfilesButton),
            buildActionCard("Nginx Developer API", openNginxExecutableButton, openNginxPreflightButton, openNginxRealValidateButton, openNginxRealReloadButton, openNginxReloadButton),
            buildActionCard("Apache Developer API", openApacheVhostsButton, openApachePublishButton, openApacheValidateButton, openApacheExecutableButton, openApacheRealValidateButton, openApacheRealReloadButton),
            buildActionCard("Runtime and Diagnostics API", openRuntimeVersionsButton, checkStatusButton)
        );
        return wrapper;
    }

    private Parent buildActionSections() {
        return devModeEnabled ? buildDeveloperOperationsPanel() : buildInfoCard(DEV_MODE_REQUIRED_TITLE, DEV_MODE_REQUIRED_TEXT);
    }

    private Parent buildInfoCard(String titleText, String descriptionText) {
        VBox card = new VBox(8);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add(STYLE_DEV_CARD);
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);
        card.getChildren().addAll(title, description);
        return card;
    }

    private VBox buildActionCard(String titleText, Button... buttons) {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);

        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        FlowPane actionGrid = new FlowPane();
        actionGrid.getStyleClass().add(STYLE_ACTION_GRID);
        actionGrid.setHgap(10);
        actionGrid.setVgap(10);

        for (Button button : buttons) {
            if (!button.getStyleClass().contains(STYLE_PRIMARY_BUTTON) && !button.getStyleClass().contains(STYLE_SECONDARY_BUTTON)) {
                button.getStyleClass().add(STYLE_ACTION_BUTTON);
            }
            if (button == openNginxRealReloadButton || button == openApacheRealReloadButton) {
                button.getStyleClass().add(STYLE_DANGER_BUTTON);
            }
            actionGrid.getChildren().add(button);
        }

        card.getChildren().addAll(title, actionGrid);
        return card;
    }

    private Parent buildLogSection() {
        VBox card = new VBox(12);
        card.getStyleClass().add(STYLE_CARD);
        card.getStyleClass().add("jhoster-application-log-card");

        HBox header = new HBox(10);
        header.setAlignment(Pos.CENTER_LEFT);
        VBox titleBox = new VBox(3);
        Label title = new Label(LABEL_LOG_TITLE);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        Label subtitle = new Label("Application based tabs: Desktop, Agent, Apache, Nginx, MySQL, PHP, Mailpit and System.");
        subtitle.getStyleClass().add(STYLE_CARD_TEXT);
        titleBox.getChildren().addAll(title, subtitle);
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        clearCurrentLogButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        openCurrentLogButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        header.getChildren().addAll(titleBox, spacer, clearCurrentLogButton, openCurrentLogButton);

        TabPane tabs = buildApplicationLogTabPane(true);
        tabs.setPrefHeight(430);

        card.getChildren().addAll(header, tabs);
        return card;
    }

    private TabPane buildApplicationLogTabPane(boolean bindSelection) {
        ensureLogInitialized();
        initializeStaticLogAreas();

        TabPane tabs = bindSelection ? applicationLogsTabPane : new TabPane();
        if (!tabs.getStyleClass().contains("jhoster-application-log-tabs")) {
            tabs.getStyleClass().add("jhoster-application-log-tabs");
        }
        tabs.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);
        tabs.getTabs().setAll(
            buildLogTab("Desktop", logArea),
            buildLogTab("Agent", agentLogArea),
            buildLogTab("Apache", apacheLogArea),
            buildLogTab("Nginx", nginxLogArea),
            buildLogTab("MySQL", mysqlLogArea),
            buildLogTab("PHP", phpLogArea),
            buildLogTab("Mailpit", mailpitLogArea),
            buildLogTab("System", systemLogArea)
        );
        return tabs;
    }

    private Tab buildLogTab(String titleText, TextArea area) {
        configureLogArea(area);
        Tab tab = new Tab(titleText);
        tab.setContent(area);
        return tab;
    }

    private TabPane buildApplicationLogPreviewTabPane() {
        TabPane tabs = new TabPane();
        if (!tabs.getStyleClass().contains("jhoster-application-log-tabs")) {
            tabs.getStyleClass().add("jhoster-application-log-tabs");
        }
        tabs.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);
        tabs.getTabs().setAll(
            buildPreviewLogTab("Desktop", "JHoster launcher ready.\n"),
            buildPreviewLogTab("Apache", "Apache log ready.\n"),
            buildPreviewLogTab("Nginx", "Nginx log ready.\n"),
            buildPreviewLogTab("MySQL", "MySQL log ready.\n"),
            buildPreviewLogTab("PHP", "PHP log ready.\n"),
            buildPreviewLogTab("Mailpit", "Mailpit log ready.\n")
        );
        return tabs;
    }

    private Tab buildPreviewLogTab(String titleText, String content) {
        TextArea area = new TextArea(content);
        configureLogArea(area);
        Tab tab = new Tab(titleText);
        tab.setContent(area);
        return tab;
    }

    private void configureLogArea(TextArea area) {
        if (!area.getStyleClass().contains(STYLE_LOG)) {
            area.getStyleClass().add(STYLE_LOG);
        }
        if (!area.getStyleClass().contains("jhoster-application-log-area")) {
            area.getStyleClass().add("jhoster-application-log-area");
        }
        area.setEditable(false);
        area.setWrapText(true);
        area.setPrefHeight(360);
    }

    private void initializeStaticLogAreas() {
        setInitialLogText(agentLogArea, "JHoster agent log ready.\n");
        setInitialLogText(apacheLogArea, "Apache log ready.\n");
        setInitialLogText(nginxLogArea, "Nginx log ready.\n");
        setInitialLogText(mysqlLogArea, "MySQL log ready.\n");
        setInitialLogText(phpLogArea, "PHP log ready.\n");
        setInitialLogText(mailpitLogArea, "Mailpit log ready.\n");
        setInitialLogText(systemLogArea, "System log ready.\n");
    }

    private void setInitialLogText(TextArea area, String value) {
        if (area.getText() == null || area.getText().isBlank()) {
            area.setText(value);
        }
    }

    public String getQuickAppProjectCode() {
        return quickAppProjectCodeField.getText();
    }

    public String getQuickAppProjectName() {
        return quickAppProjectNameField.getText();
    }

    public String getQuickAppTemplateCode() {
        return quickAppTemplateCodeField.getText();
    }

    public String getQuickAppDomain() {
        return quickAppDomainField.getText();
    }

    public int getQuickAppPort() {
        try {
            return Integer.parseInt(quickAppPortField.getText().trim());
        } catch (NumberFormatException exception) {
            return DesktopApiConfig.DEFAULT_QUICK_APP_PORT;
        }
    }

    public String getQuickAppWebServer() {
        return quickAppNginxRadio.isSelected() ? DesktopApiConfig.WEB_SERVER_PROFILE_NGINX : DesktopApiConfig.WEB_SERVER_PROFILE_APACHE;
    }

    public boolean isQuickAppMysqlEnabled() {
        return quickAppMysqlCheckBox.isSelected();
    }

    public boolean isQuickAppPhpEnabled() {
        return quickAppPhpCheckBox.isSelected();
    }

    public boolean isQuickAppMailpitEnabled() {
        return quickAppMailpitCheckBox.isSelected();
    }

    public String getRuntimeApacheCode() {
        return runtimeApacheCodeField.getText();
    }

    public String getRuntimeNginxCode() {
        return runtimeNginxCodeField.getText();
    }

    public String getRuntimeMysqlCode() {
        return runtimeMysqlCodeField.getText();
    }

    public String getRuntimePhpCode() {
        return runtimePhpCodeField.getText();
    }

    public String getRuntimeNodeCode() {
        return runtimeNodeCodeField.getText();
    }

    public String getRuntimePythonCode() {
        return runtimePythonCodeField.getText();
    }

    public String getRuntimeMemcachedCode() {
        return runtimeMemcachedCodeField.getText();
    }

    public String getRuntimeRedisCode() {
        return runtimeRedisCodeField.getText();
    }

    public String getRuntimeMailpitCode() {
        return runtimeMailpitCodeField.getText();
    }

    public String getRuntimeApacheFolder() {
        return runtimeApacheFolderField.getText();
    }

    public String getRuntimeNginxFolder() {
        return runtimeNginxFolderField.getText();
    }

    public String getRuntimeMysqlFolder() {
        return runtimeMysqlFolderField.getText();
    }

    public String getRuntimePhpFolder() {
        return runtimePhpFolderField.getText();
    }

    public String getRuntimeNodeFolder() {
        return runtimeNodeFolderField.getText();
    }

    public String getRuntimePythonFolder() {
        return runtimePythonFolderField.getText();
    }

    public String getRuntimeMemcachedFolder() {
        return runtimeMemcachedFolderField.getText();
    }

    public String getRuntimeRedisFolder() {
        return runtimeRedisFolderField.getText();
    }

    public String getRuntimeMailpitFolder() {
        return runtimeMailpitFolderField.getText();
    }

    public String getWorkflowProjectCode() {
        return workflowProjectCodeField.getText();
    }

    public String getWorkflowDomain() {
        return workflowDomainField.getText();
    }

    public int getWorkflowPort() {
        try {
            return Integer.parseInt(workflowPortField.getText().trim());
        } catch (NumberFormatException exception) {
            return DesktopApiConfig.DEFAULT_WORKFLOW_PORT;
        }
    }

    public String getWorkflowTargetDir() {
        return workflowTargetDirField.getText();
    }


    public Optional<DesktopServiceSelectionSettings> showServiceSettingsDialog(DesktopServiceSelectionSettings currentSettings) {
        DesktopServiceSelectionSettings settings = currentSettings == null ? DesktopServiceSelectionSettings.defaults() : currentSettings.normalized();

        Dialog<DesktopServiceSelectionSettings> dialog = new Dialog<>();
        dialog.setTitle("JHoster Settings");
        dialog.setHeaderText("Service and port selection");
        dialog.getDialogPane().getStyleClass().add(STYLE_SETTINGS_DIALOG);

        ButtonType saveButtonType = new ButtonType("Save", ButtonBar.ButtonData.OK_DONE);
        dialog.getDialogPane().getButtonTypes().addAll(saveButtonType, ButtonType.CANCEL);

        RadioButton apacheModeRadio = new RadioButton("Apache");
        RadioButton nginxModeRadio = new RadioButton("Nginx");
        ToggleGroup webServerGroup = new ToggleGroup();
        apacheModeRadio.setToggleGroup(webServerGroup);
        nginxModeRadio.setToggleGroup(webServerGroup);
        apacheModeRadio.setSelected(DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(settings.getActiveWebServer()));
        nginxModeRadio.setSelected(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(settings.getActiveWebServer()));

        CheckBox apacheCheckBox = new CheckBox("Apache public web server");
        CheckBox nginxCheckBox = new CheckBox("Nginx public web server");
        CheckBox mysqlCheckBox = new CheckBox("MySQL database");
        CheckBox phpCheckBox = new CheckBox("PHP FastCGI runtime");
        CheckBox mailpitCheckBox = new CheckBox("Mailpit mail catcher");

        apacheCheckBox.setSelected(settings.isApacheEnabled());
        nginxCheckBox.setSelected(settings.isNginxEnabled());
        mysqlCheckBox.setSelected(settings.isMysqlEnabled());
        phpCheckBox.setSelected(settings.isPhpEnabled());
        mailpitCheckBox.setSelected(settings.isMailpitEnabled());

        apacheModeRadio.setOnAction(event -> {
            apacheCheckBox.setSelected(true);
            nginxCheckBox.setSelected(false);
        });
        nginxModeRadio.setOnAction(event -> {
            nginxCheckBox.setSelected(true);
            apacheCheckBox.setSelected(false);
        });
        apacheCheckBox.setOnAction(event -> {
            if (apacheCheckBox.isSelected()) {
                apacheModeRadio.setSelected(true);
                nginxCheckBox.setSelected(false);
            }
        });
        nginxCheckBox.setOnAction(event -> {
            if (nginxCheckBox.isSelected()) {
                nginxModeRadio.setSelected(true);
                apacheCheckBox.setSelected(false);
            }
        });

        VBox generalBox = new VBox(12);
        CheckBox launchOnWindowsCheckBox = new CheckBox("Run JHoster when Windows starts");
        CheckBox minimizedCheckBox = new CheckBox("Start minimized to tray");
        CheckBox autoStartSelectedCheckBox = new CheckBox("Start selected services automatically");
        autoStartSelectedCheckBox.setSelected(true);
        generalBox.getChildren().addAll(
            new Label("JHoster starts selected services from one shared workspace."),
            launchOnWindowsCheckBox,
            minimizedCheckBox,
            autoStartSelectedCheckBox,
            new Separator(),
            buildInfoRow("Document Root", "E:\\JHoster\\www"),
            buildInfoRow("Data Folder", "E:\\JHoster\\data"),
            buildInfoRow("Config Folder", "E:\\JHoster\\etc\\jhoster")
        );

        HBox webModeBox = new HBox(18);
        webModeBox.setAlignment(Pos.CENTER_LEFT);
        webModeBox.getChildren().addAll(apacheModeRadio, nginxModeRadio);

        VBox serviceBox = new VBox(12);
        serviceBox.getChildren().addAll(
            new Label("Active Web Server"),
            webModeBox,
            new Separator(),
            new Label("Select services used by Start All"),
            buildServiceSelectionRow(apacheCheckBox, "80", "443", "Public web server"),
            buildServiceSelectionRow(nginxCheckBox, "80", "443", "Public web server"),
            buildServiceSelectionRow(mysqlCheckBox, "3306", "-", "Database"),
            buildServiceSelectionRow(phpCheckBox, "9000", "-", "FastCGI runtime"),
            buildServiceSelectionRow(mailpitCheckBox, "1025", "8025", "SMTP and web UI"),
            new Separator(),
            new Label("Apache and Nginx share E:\\JHoster\\www. Only one public web server can own 80/443.")
        );

        TabPane settingsTabPane = new TabPane();
        settingsTabPane.getStyleClass().add("jhoster-settings-tab-pane");
        settingsTabPane.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);
        settingsTabPane.getTabs().addAll(
            buildSettingsTab("General", generalBox),
            buildSettingsTab("Services", serviceBox),
            buildSettingsTab(LICENSE_SETTINGS_TAB, buildLicenseSettingsContent()),
            buildSettingsTab(LABEL_HOSTS_AUTO_SETTINGS_TAB, buildHostsAutoSettingsContent()),
            buildSettingsTab("Appearance", buildAppearanceSettingsContent()),
            buildSettingsTab("Advanced", buildAdvancedSettingsContent())
        );
        if (devModeEnabled) {
            settingsTabPane.getTabs().add(buildSettingsTab(DEV_MODE_SETTINGS_TAB, buildDeveloperSettingsContent()));
        }
        settingsTabPane.setPrefWidth(820);
        settingsTabPane.setPrefHeight(580);
        dialog.getDialogPane().setContent(settingsTabPane);

        dialog.setResultConverter(buttonType -> {
            if (buttonType != saveButtonType) {
                return null;
            }

            String activeWebServer = nginxModeRadio.isSelected()
                ? DesktopApiConfig.WEB_SERVER_PROFILE_NGINX
                : DesktopApiConfig.WEB_SERVER_PROFILE_APACHE;

            return new DesktopServiceSelectionSettings(
                activeWebServer,
                apacheCheckBox.isSelected(),
                nginxCheckBox.isSelected(),
                mysqlCheckBox.isSelected(),
                phpCheckBox.isSelected(),
                mailpitCheckBox.isSelected()
            ).normalized();
        });

        return dialog.showAndWait();
    }

    private Parent buildSettingsSection(String titleText, Parent content) {
        VBox section = new VBox(10);
        section.getStyleClass().add("jhoster-settings-section");
        Label title = new Label(titleText);
        title.getStyleClass().add(STYLE_SECTION_TITLE);
        section.getChildren().addAll(title, content);
        return section;
    }

    private Tab buildSettingsTab(String titleText, Parent content) {
        Tab tab = new Tab(titleText);
        tab.setContent(buildSettingsTabContent(content));
        return tab;
    }

    private Parent buildSettingsTabContent(Parent content) {
        VBox shell = new VBox(14);
        shell.getStyleClass().add("jhoster-settings-tab-content");
        shell.getChildren().add(content);

        ScrollPane scrollPane = new ScrollPane(shell);
        scrollPane.setFitToWidth(true);
        scrollPane.setPrefWidth(800);
        scrollPane.setPrefHeight(520);
        scrollPane.getStyleClass().add("jhoster-settings-scroll");
        return scrollPane;
    }

    private Parent buildAppearanceSettingsContent() {
        VBox box = new VBox(12);
        box.getStyleClass().add(STYLE_DEV_CARD);

        Label title = new Label("Appearance");
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        Label text = new Label("JHoster uses a clean light control panel theme by default. Dark theme and compact density can be added later without changing the left sidebar layout.");
        text.getStyleClass().add(STYLE_CARD_TEXT);
        text.setWrapText(true);

        box.getChildren().addAll(
            title,
            text,
            new Separator(),
            buildInfoRow("Theme", "Light"),
            buildInfoRow("Layout", "Left Sidebar"),
            buildInfoRow("Settings Navigation", "Tabs"),
            buildInfoRow("Startup Window", "Maximized")
        );
        return box;
    }

    private Parent buildAdvancedSettingsContent() {
        VBox box = new VBox(12);
        box.getStyleClass().add(STYLE_DEV_CARD);

        Label title = new Label("Advanced");
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        Label text = new Label("Advanced runtime paths and endpoint details are grouped here so the main left menu stays clean.");
        text.getStyleClass().add(STYLE_CARD_TEXT);
        text.setWrapText(true);

        box.getChildren().addAll(
            title,
            text,
            new Separator(),
            buildInfoRow("Agent Base URL", DesktopApiConfig.AGENT_BASE_URL),
            buildInfoRow("Quick App Plan", DesktopApiConfig.resolveUrl(DesktopApiConfig.QUICK_APP_PLAN_ROUTE)),
            buildInfoRow("Hosts Inspect", DesktopApiConfig.resolveUrl(DesktopApiConfig.HOSTS_AUTO_INSPECT_ROUTE)),
            buildInfoRow("License", DesktopApiConfig.resolveUrl(DesktopApiConfig.LICENSE_ROUTE))
        );
        return box;
    }

    private Parent buildHostsAutoSettingsContent() {
        VBox box = new VBox(12);
        box.getStyleClass().add(STYLE_DEV_CARD);
        box.getStyleClass().add(STYLE_HOSTS_AUTO_GRID);

        Label title = new Label(LABEL_HOSTS_AUTO_CARD);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        Label text = new Label(LABEL_HOSTS_AUTO_SUBTITLE);
        text.getStyleClass().add(STYLE_CARD_TEXT);
        text.setWrapText(true);

        FlowPane strip = new FlowPane();
        strip.getStyleClass().add(STYLE_SUMMARY_STRIP);
        strip.setHgap(10);
        strip.setVgap(10);
        strip.getChildren().addAll(
            buildSummaryPill(LABEL_HOSTS_AUTO_STATUS, settingsHostsAutoHealthValue),
            buildSummaryPill(LABEL_HOSTS_AUTO_MANAGED, settingsHostsAutoManagedValue),
            buildSummaryPill(LABEL_HOSTS_AUTO_ISSUES, settingsHostsAutoIssuesValue)
        );

        settingsHostsAutoInspectButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        settingsHostsAutoRepairPlanButton.getStyleClass().add(STYLE_SECONDARY_BUTTON);
        settingsHostsAutoRepairButton.getStyleClass().add(STYLE_PRIMARY_BUTTON);

        FlowPane actions = new FlowPane();
        actions.getStyleClass().add(STYLE_ACTION_GRID);
        actions.setHgap(10);
        actions.setVgap(10);
        actions.getChildren().addAll(settingsHostsAutoInspectButton, settingsHostsAutoRepairPlanButton, settingsHostsAutoRepairButton);

        box.getChildren().addAll(
            title,
            text,
            strip,
            new Separator(),
            buildInfoRowWithValue(LABEL_HOSTS_AUTO_MESSAGE, settingsHostsAutoMessageValue),
            buildInfoRowWithValue(LABEL_HOSTS_AUTO_TARGET, settingsHostsAutoTargetValue),
            buildInfoRowWithValue(LABEL_HOSTS_AUTO_MODE, settingsHostsAutoModeValue),
            buildInfoRow("Inspect Endpoint", DesktopApiConfig.resolveUrl(DesktopApiConfig.HOSTS_AUTO_INSPECT_ROUTE)),
            actions
        );
        return box;
    }

    private Parent buildLicenseSettingsContent() {
        VBox box = new VBox(12);
        box.getStyleClass().add(STYLE_DEV_CARD);

        Label title = new Label(LICENSE_SETTINGS_TITLE);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        Label text = new Label(LICENSE_SETTINGS_TEXT);
        text.getStyleClass().add(STYLE_CARD_TEXT);
        text.setWrapText(true);

        box.getChildren().addAll(
            title,
            text,
            new Separator(),
            buildInfoRow("Current Plan", licenseBadgeLabel.getText()),
            buildInfoRow("Site Usage", licenseUsageLabel.getText()),
            buildInfoRow("Upgrade Hint", licenseHintLabel.getText()),
            buildInfoRow("License Endpoint", DesktopApiConfig.resolveUrl(DesktopApiConfig.LICENSE_ROUTE)),
            new Separator(),
            buildLicenseFeatureRegistry()
        );
        return box;
    }

    private Parent buildLicenseFeatureRegistry() {
        VBox registry = new VBox(8);
        registry.getStyleClass().add(STYLE_LICENSE_FEATURE_GRID);

        Label title = new Label(LICENSE_FEATURES_TITLE);
        title.getStyleClass().add(STYLE_CARD_TITLE);

        registry.getChildren().addAll(
            title,
            buildLicenseFeatureRow(LICENSE_FEATURE_SITE_LIMIT, LICENSE_FEATURE_SITE_LIMIT_TEXT, licenseSiteLimitStatusLabel),
            buildLicenseFeatureRow(LICENSE_FEATURE_ADVANCED_SSL, LICENSE_FEATURE_ADVANCED_SSL_TEXT, licenseAdvancedSslStatusLabel),
            buildLicenseFeatureRow(LICENSE_FEATURE_AUTOMATED_BACKUP, LICENSE_FEATURE_AUTOMATED_BACKUP_TEXT, licenseAutomatedBackupStatusLabel),
            buildLicenseFeatureRow(LICENSE_FEATURE_ADVANCED_DNS, LICENSE_FEATURE_ADVANCED_DNS_TEXT, licenseAdvancedDnsStatusLabel),
            buildLicenseFeatureRow(LICENSE_FEATURE_AI_OLLAMA, LICENSE_FEATURE_AI_OLLAMA_TEXT, licenseAiOllamaStatusLabel)
        );
        return registry;
    }

    private Parent buildLicenseFeatureRow(String nameText, String descriptionText, Label statusLabel) {
        HBox row = new HBox(12);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_LICENSE_FEATURE_ROW);

        VBox textBox = new VBox(2);
        Label name = new Label(nameText);
        name.getStyleClass().add(STYLE_LICENSE_FEATURE_NAME);
        Label description = new Label(descriptionText);
        description.getStyleClass().add(STYLE_CARD_TEXT);
        description.setWrapText(true);
        textBox.getChildren().addAll(name, description);

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        applyLicenseFeatureStatusStyle(statusLabel);
        row.getChildren().addAll(textBox, spacer, statusLabel);
        return row;
    }

    private void applyLicenseFeatureStatusStyle(Label statusLabel) {
        statusLabel.getStyleClass().removeAll(STYLE_LICENSE_FEATURE_STATUS, STYLE_LICENSE_FEATURE_STATUS_LOCKED);
        statusLabel.getStyleClass().add(STYLE_LICENSE_FEATURE_STATUS);
        if (LICENSE_FEATURE_STATUS_PRO_LOCKED.equals(statusLabel.getText())) {
            statusLabel.getStyleClass().add(STYLE_LICENSE_FEATURE_STATUS_LOCKED);
        }
    }

    public void updateHostsAutoSummary(HostsAutoSummary summary) {
        HostsAutoSummary safeSummary = summary == null ? HostsAutoSummary.empty() : summary;
        hostsAutoHealthValue.setText(safeSummary.getHealthLabel());
        hostsAutoManagedValue.setText(safeSummary.getCountLabel());
        hostsAutoIssuesValue.setText(safeSummary.getIssueLabel());
        hostsAutoMessageValue.setText(safeSummary.getMessage());
        hostsAutoTargetValue.setText(safeSummary.getTargetFile());
        hostsAutoModeValue.setText(safeSummary.getApplyMode());
        quickHostsAutoHealthValue.setText(safeSummary.getHealthLabel());
        topbarHostsValue.setText(safeSummary.getHealthLabel());
        settingsHostsAutoHealthValue.setText(safeSummary.getHealthLabel());
        settingsHostsAutoManagedValue.setText(safeSummary.getCountLabel());
        settingsHostsAutoIssuesValue.setText(safeSummary.getIssueLabel());
        settingsHostsAutoMessageValue.setText(safeSummary.getMessage());
        settingsHostsAutoTargetValue.setText(safeSummary.getTargetFile());
        settingsHostsAutoModeValue.setText(safeSummary.getApplyMode());
        siteWizardHostsStatusPreviewValue.setText(safeSummary.getHealthLabel());
        siteWizardHostsIssuesPreviewValue.setText(safeSummary.getIssueLabel());
        applyHostsAutoStatusStyle(hostsAutoHealthValue);
        applyHostsAutoStatusStyle(quickHostsAutoHealthValue);
        applyHostsAutoStatusStyle(topbarHostsValue);
        applyHostsAutoStatusStyle(settingsHostsAutoHealthValue);
        applyHostsAutoStatusStyle(siteWizardHostsStatusPreviewValue);
    }

    private void applyHostsAutoStatusStyle(Label statusLabel) {
        statusLabel.getStyleClass().removeAll(STYLE_HOSTS_AUTO_STATUS, STYLE_HOSTS_AUTO_STATUS_WARNING, STYLE_HOSTS_AUTO_STATUS_OK);
        statusLabel.getStyleClass().add(STYLE_HOSTS_AUTO_STATUS);
        if ("Healthy".equals(statusLabel.getText())) {
            statusLabel.getStyleClass().add(STYLE_HOSTS_AUTO_STATUS_OK);
            return;
        }
        if (!VALUE_HOSTS_AUTO_NOT_CHECKED.equals(statusLabel.getText())) {
            statusLabel.getStyleClass().add(STYLE_HOSTS_AUTO_STATUS_WARNING);
        }
    }

    public void updateLicensePlanSummary(LicensePlanSummary summary) {
        LicensePlanSummary safeSummary = summary == null ? LicensePlanSummary.empty() : summary;
        licenseBadgeLabel.setText(safeSummary.getPlanLabel());
        licenseUsageLabel.setText("Sites " + safeSummary.getUsageLabel());
        topbarPlanValue.setText(safeSummary.getPlanLabel());
        topbarSitesValue.setText("Sites " + safeSummary.getUsageLabel());
        licenseHintLabel.setText(safeSummary.getUpgradeHint());
        licenseSiteLimitStatusLabel.setText(safeSummary.getSiteLimitStatusLabel());
        licenseAdvancedSslStatusLabel.setText(safeSummary.getAdvancedSslStatusLabel());
        licenseAutomatedBackupStatusLabel.setText(safeSummary.getAutomatedBackupStatusLabel());
        licenseAdvancedDnsStatusLabel.setText(safeSummary.getAdvancedDnsStatusLabel());
        licenseAiOllamaStatusLabel.setText(safeSummary.getAiOllamaStatusLabel());
        applyLicenseFeatureStatusStyle(licenseSiteLimitStatusLabel);
        applyLicenseFeatureStatusStyle(licenseAdvancedSslStatusLabel);
        applyLicenseFeatureStatusStyle(licenseAutomatedBackupStatusLabel);
        applyLicenseFeatureStatusStyle(licenseAdvancedDnsStatusLabel);
        applyLicenseFeatureStatusStyle(licenseAiOllamaStatusLabel);

        licenseUsageLabel.getStyleClass().remove("jhoster-license-limit-warning");
        topbarSitesValue.getStyleClass().remove("jhoster-license-limit-warning");
        if (!safeSummary.canCreateProject()) {
            licenseUsageLabel.getStyleClass().add("jhoster-license-limit-warning");
            topbarSitesValue.getStyleClass().add("jhoster-license-limit-warning");
        }
    }

    private Parent buildDeveloperSettingsContent() {
        VBox box = new VBox(12);
        box.getStyleClass().add(STYLE_DEV_CARD);

        Label title = new Label(DEV_MODE_BANNER_TITLE);
        title.getStyleClass().add(STYLE_SECTION_TITLE);

        Label text = new Label(DEV_MODE_SETTINGS_TEXT);
        text.getStyleClass().add(STYLE_CARD_TEXT);
        text.setWrapText(true);

        box.getChildren().addAll(
            title,
            text,
            new Separator(),
            buildInfoRow("Agent Base URL", DesktopApiConfig.AGENT_BASE_URL),
            buildInfoRow("Web Server Profiles", DesktopApiConfig.resolveUrl(DesktopApiConfig.WEB_SERVER_PROFILES_ROUTE)),
            buildInfoRow("Runtime Versions", DesktopApiConfig.resolveUrl(DesktopApiConfig.RUNTIME_VERSIONS_ROUTE)),
            buildInfoRow("Startup Gate", "Shift, --dev, -Djhoster.dev=true, JHOSTER_DEV_MODE=1"),
            buildInfoRow("Normal Mode", "Developer Tools hidden")
        );
        return box;
    }

    private Parent buildServiceSelectionRow(CheckBox checkBox, String port, String sslPort, String note) {
        HBox row = new HBox(12);
        row.setAlignment(Pos.CENTER_LEFT);
        row.getStyleClass().add(STYLE_SETTINGS_ROW);

        checkBox.setMinWidth(210);
        TextField portField = new TextField(port);
        portField.getStyleClass().add(STYLE_SETTINGS_PORT);
        portField.setPrefWidth(78);
        TextField sslPortField = new TextField(sslPort);
        sslPortField.getStyleClass().add(STYLE_SETTINGS_PORT);
        sslPortField.setPrefWidth(78);
        Label noteLabel = new Label(note);
        noteLabel.getStyleClass().add(STYLE_CARD_TEXT);

        row.getChildren().addAll(checkBox, new Label("Port"), portField, new Label("SSL"), sslPortField, noteLabel);
        return row;
    }

    private Parent buildServicePortInfoRow(String serviceName, String port, String sslPort, String note) {
        HBox row = new HBox(12);
        row.setAlignment(Pos.CENTER_LEFT);
        Label nameLabel = new Label(serviceName);
        nameLabel.setMinWidth(90);
        Label portLabel = new Label("Port: " + port);
        portLabel.setMinWidth(90);
        Label sslLabel = new Label("SSL: " + sslPort);
        sslLabel.setMinWidth(80);
        Label noteLabel = new Label(note);
        noteLabel.getStyleClass().add(STYLE_CARD_TEXT);
        row.getChildren().addAll(nameLabel, portLabel, sslLabel, noteLabel);
        return row;
    }


    public void appendPackageDownloadSummary(PackageDownloadSummary summary) {
        if (summary == null) {
            return;
        }
        packageResultArea.appendText("\n[" + summary.getTitle() + "] " + summary.getDescription() + "\n" + summary.getBody() + "\n");
        updateSelectedPackageStatusFromSummary(summary);
        appendLog(summary.getTitle() + " -> " + summary.getDescription());
    }

    public String getPackageCodeInput() {
        return packageCodeField.getText() == null ? "" : packageCodeField.getText().trim();
    }

    public void applyServiceSelectionSettings(DesktopServiceSelectionSettings settings) {
        DesktopServiceSelectionSettings safeSettings = settings == null ? DesktopServiceSelectionSettings.defaults() : settings.normalized();
        syncActiveWebServerDisplay(safeSettings.getActiveWebServer());

        applyServiceEnabledState(DesktopApiConfig.SERVICE_CODE_APACHE, safeSettings.isServiceEnabled(DesktopApiConfig.SERVICE_CODE_APACHE));
        applyServiceEnabledState(DesktopApiConfig.SERVICE_CODE_NGINX, safeSettings.isServiceEnabled(DesktopApiConfig.SERVICE_CODE_NGINX));
        applyServiceEnabledState(DesktopApiConfig.SERVICE_CODE_MYSQL, safeSettings.isServiceEnabled(DesktopApiConfig.SERVICE_CODE_MYSQL));
        applyServiceEnabledState(DesktopApiConfig.SERVICE_CODE_PHP, safeSettings.isServiceEnabled(DesktopApiConfig.SERVICE_CODE_PHP));
        applyServiceEnabledState(DesktopApiConfig.SERVICE_CODE_MAILPIT, safeSettings.isServiceEnabled(DesktopApiConfig.SERVICE_CODE_MAILPIT));
    }

    private String webServerDisplayName(String webServerCode) {
        if (DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(webServerCode)) {
            return VALUE_NGINX_DISPLAY;
        }
        return VALUE_APACHE_DISPLAY;
    }

    private String activeWebServerServiceCode() {
        return DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(activeWebServerCode)
            ? DesktopApiConfig.SERVICE_CODE_NGINX
            : DesktopApiConfig.SERVICE_CODE_APACHE;
    }

    private void syncActiveWebServerDisplay(String webServerCode) {
        activeWebServerCode = webServerCode;
        String activeDisplayName = webServerDisplayName(activeWebServerCode);
        activeWebServerValue.setText(activeDisplayName);
        simpleWebServerNameValue.setText(activeDisplayName);
        topbarEngineValue.setText(activeDisplayName);
        simpleWebServerStatusValue.setText(
            DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(activeWebServerCode)
                ? compactNginxStatusValue.getText()
                : compactApacheStatusValue.getText()
        );
        applyStatusStyle(simpleWebServerStatusValue, simpleWebServerStatusValue.getText());
    }

    private void applyServiceEnabledState(String serviceCode, boolean enabled) {
        if (DesktopApiConfig.SERVICE_CODE_APACHE.equals(serviceCode)) {
            setStartRestartState(compactApacheStartButton, compactApacheRestartButton, apacheStartButton, apacheRestartButton, enabled);
            if (!enabled) {
                updateServiceLabels(serviceApacheStatusValue, compactApacheStatusValue, "disabled");
            }
            return;
        }

        if (DesktopApiConfig.SERVICE_CODE_NGINX.equals(serviceCode)) {
            setStartRestartState(compactNginxStartButton, compactNginxRestartButton, nginxStartButton, nginxRestartButton, enabled);
            if (!enabled) {
                updateServiceLabels(serviceNginxStatusValue, compactNginxStatusValue, "disabled");
            }
            return;
        }

        if (DesktopApiConfig.SERVICE_CODE_MYSQL.equals(serviceCode)) {
            setStartRestartState(compactMysqlStartButton, compactMysqlRestartButton, mysqlStartButton, mysqlRestartButton, enabled);
            if (!enabled) {
                updateServiceLabels(serviceMysqlStatusValue, compactMysqlStatusValue, "disabled");
            }
            return;
        }

        if (DesktopApiConfig.SERVICE_CODE_PHP.equals(serviceCode)) {
            setStartRestartState(compactPhpStartButton, compactPhpRestartButton, phpStartButton, phpRestartButton, enabled);
            if (!enabled) {
                updateServiceLabels(servicePhpStatusValue, compactPhpStatusValue, "disabled");
            }
            return;
        }

        if (DesktopApiConfig.SERVICE_CODE_MAILPIT.equals(serviceCode)) {
            setStartRestartState(compactMailpitStartButton, compactMailpitRestartButton, mailpitStartButton, mailpitRestartButton, enabled);
            if (!enabled) {
                updateServiceLabels(serviceMailpitStatusValue, compactMailpitStatusValue, "disabled");
            }
        }
    }

    private void setStartRestartState(Button compactStart, Button compactRestart, Button fullStart, Button fullRestart, boolean enabled) {
        compactStart.setDisable(!enabled);
        compactRestart.setDisable(!enabled);
        fullStart.setDisable(!enabled);
        fullRestart.setDisable(!enabled);
    }

    private void setButtonAction(Button button, EventHandler<ActionEvent> handler) {
        button.setOnAction(handler);
    }

    public void setOnNavDashboard(EventHandler<ActionEvent> handler) {
        setButtonAction(navDashboardButton, handler);
    }

    public void setOnNavNewSite(EventHandler<ActionEvent> handler) {
        setButtonAction(navNewSiteButton, handler);
    }

    public void setOnNavServices(EventHandler<ActionEvent> handler) {
        setButtonAction(navServicesButton, handler);
    }

    public void setOnNavProjects(EventHandler<ActionEvent> handler) {
        setButtonAction(navProjectsButton, handler);
    }

    public void setOnNavVirtualHosts(EventHandler<ActionEvent> handler) {
        setButtonAction(navVirtualHostsButton, handler);
    }

    public void setOnNavApps(EventHandler<ActionEvent> handler) {
        setButtonAction(navAppsButton, handler);
    }

    public void setOnNavVersions(EventHandler<ActionEvent> handler) {
        setButtonAction(navVersionsButton, handler);
    }

    public void setOnNavWorkflow(EventHandler<ActionEvent> handler) {
        setButtonAction(navWorkflowButton, handler);
    }

    public void setOnNavTools(EventHandler<ActionEvent> handler) {
        setButtonAction(navToolsButton, handler);
    }

    public void setOnNavDeveloper(EventHandler<ActionEvent> handler) {
        setButtonAction(navDeveloperButton, handler);
    }

    public void setOnNavLogs(EventHandler<ActionEvent> handler) {
        setButtonAction(navLogsButton, handler);
    }

    public void setOnNavSettings(EventHandler<ActionEvent> handler) {
        setButtonAction(navSettingsButton, handler);
    }

    public void setOnOverviewTab(EventHandler<ActionEvent> handler) {
        setButtonAction(overviewTabButton, handler);
    }

    public void setOnRuntimeVersionsTab(EventHandler<ActionEvent> handler) {
        setButtonAction(runtimeVersionsTabButton, handler);
    }

    public void setOnQuickAppTab(EventHandler<ActionEvent> handler) {
        setButtonAction(quickAppTabButton, handler);
    }

    public void setOnWorkflowTab(EventHandler<ActionEvent> handler) {
        setButtonAction(workflowTabButton, handler);
    }

    public void setOnDiagnosticsTab(EventHandler<ActionEvent> handler) {
        setButtonAction(diagnosticsTabButton, handler);
    }

    public void setOnManageServices(EventHandler<ActionEvent> handler) {
        setButtonAction(manageServicesButton, handler);
    }

    public void setOnViewAllLogs(EventHandler<ActionEvent> handler) {
        setButtonAction(viewAllLogsButton, handler);
    }

    public void setOnClearCurrentLog(EventHandler<ActionEvent> handler) {
        setButtonAction(clearCurrentLogButton, handler);
    }

    public void setOnOpenCurrentLog(EventHandler<ActionEvent> handler) {
        setButtonAction(openCurrentLogButton, handler);
    }

    public void clearSelectedLogTab() {
        selectedApplicationLogArea().clear();
    }

    private TextArea selectedApplicationLogArea() {
        return switch (getSelectedSimpleLogTabTitle()) {
            case "Agent" -> agentLogArea;
            case "Apache" -> apacheLogArea;
            case "Nginx" -> nginxLogArea;
            case "MySQL" -> mysqlLogArea;
            case "PHP" -> phpLogArea;
            case "Mailpit" -> mailpitLogArea;
            case "System" -> systemLogArea;
            default -> logArea;
        };
    }

    private String getSelectedSimpleLogTabTitle() {
        Tab selected = applicationLogsTabPane.getSelectionModel().getSelectedItem();
        if (selected == null || selected.getText() == null || selected.getText().isBlank()) {
            return "Desktop";
        }
        return selected.getText();
    }

    public String getSelectedSimpleLogFolder() {
        return switch (getSelectedSimpleLogTabTitle()) {
            case "Agent" -> "logs/agent";
            case "Apache" -> "logs/apache";
            case "Nginx" -> "logs/nginx";
            case "MySQL" -> "logs/mysql";
            case "PHP" -> "logs/php";
            case "Mailpit" -> "logs/mailpit";
            case "System" -> "logs";
            default -> "logs/desktop";
        };
    }

    public void appendCurrentLogNotice(String message) {
        selectedApplicationLogArea().appendText(message + "\n");
    }

    public void setOnPackageCatalog(EventHandler<ActionEvent> handler) {
        setButtonAction(packageCatalogButton, handler);
    }

    public void setOnPackagePlan(EventHandler<ActionEvent> handler) {
        setButtonAction(packagePlanButton, handler);
    }

    public void setOnPackageDownload(EventHandler<ActionEvent> handler) {
        setButtonAction(packageDownloadButton, handler);
    }

    public void setOnPackageInstall(EventHandler<ActionEvent> handler) {
        setButtonAction(packageInstallButton, handler);
    }

    public void setOnOpenPackageCenter(EventHandler<ActionEvent> handler) {
        setButtonAction(packageCenterOpenButton, handler);
    }

    public void setOnSystemSettings(EventHandler<ActionEvent> handler) {
        setButtonAction(systemSettingsButton, handler);
    }

    public void setOnQuickStartAll(EventHandler<ActionEvent> handler) {
        setButtonAction(quickStartAllButton, handler);
    }

    public void setOnQuickStopAll(EventHandler<ActionEvent> handler) {
        setButtonAction(quickStopAllButton, handler);
    }

    public void setOnQuickWeb(EventHandler<ActionEvent> handler) {
        setButtonAction(quickWebButton, handler);
    }

    public void setOnQuickDatabase(EventHandler<ActionEvent> handler) {
        setButtonAction(quickDatabaseButton, handler);
    }

    public void setOnQuickMailpit(EventHandler<ActionEvent> handler) {
        setButtonAction(quickMailpitButton, handler);
    }

    public void setOnQuickTerminal(EventHandler<ActionEvent> handler) {
        setButtonAction(quickTerminalButton, handler);
    }

    public void setOnQuickRoot(EventHandler<ActionEvent> handler) {
        setButtonAction(quickRootButton, handler);
    }

    public void setOnQuickProjects(EventHandler<ActionEvent> handler) {
        setButtonAction(quickProjectsButton, handler);
    }

    public void setOnQuickLogs(EventHandler<ActionEvent> handler) {
        setButtonAction(quickLogsButton, handler);
    }

    public void setOnQuickBin(EventHandler<ActionEvent> handler) {
        setButtonAction(quickBinButton, handler);
    }

    public void setOnQuickCmder(EventHandler<ActionEvent> handler) {
        setButtonAction(quickCmderButton, handler);
    }

    public void setOnQuickGitBash(EventHandler<ActionEvent> handler) {
        setButtonAction(quickGitBashButton, handler);
    }

    public void setOnQuickNotepad(EventHandler<ActionEvent> handler) {
        setButtonAction(quickNotepadButton, handler);
    }

    public void setOnQuickNgrok(EventHandler<ActionEvent> handler) {
        setButtonAction(quickNgrokButton, handler);
    }

    public void setOnQuickComposer(EventHandler<ActionEvent> handler) {
        setButtonAction(quickComposerButton, handler);
    }

    public void setOnQuickYarn(EventHandler<ActionEvent> handler) {
        setButtonAction(quickYarnButton, handler);
    }

    public void setOnSelectApacheWebServer(EventHandler<ActionEvent> handler) {
        selectApacheWebServerHandler = handler;
        setButtonAction(selectApacheWebServerButton, handler);
    }

    public void setOnSelectNginxWebServer(EventHandler<ActionEvent> handler) {
        selectNginxWebServerHandler = handler;
        setButtonAction(selectNginxWebServerButton, handler);
    }


    public void setOnSimpleWebServerStart(EventHandler<ActionEvent> handler) {
        setButtonAction(simpleWebServerStartButton, handler);
    }

    public void setOnSimpleWebServerStop(EventHandler<ActionEvent> handler) {
        setButtonAction(simpleWebServerStopButton, handler);
    }

    public void setOnSimpleWebServerRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(simpleWebServerRestartButton, handler);
    }

    public void setOnSimpleWebServerSwitch(EventHandler<ActionEvent> handler) {
        simpleWebServerSwitchButton.setOnAction(event -> showEngineMenu(event, handler));
    }

    private void showEngineMenu(ActionEvent event, EventHandler<ActionEvent> fallbackHandler) {
        ContextMenu menu = new ContextMenu();
        MenuItem apacheItem = new MenuItem("Use Apache");
        MenuItem nginxItem = new MenuItem("Use Nginx");
        apacheItem.setDisable(DesktopApiConfig.WEB_SERVER_PROFILE_APACHE.equals(activeWebServerCode));
        nginxItem.setDisable(DesktopApiConfig.WEB_SERVER_PROFILE_NGINX.equals(activeWebServerCode));
        apacheItem.setOnAction(menuEvent -> {
            if (selectApacheWebServerHandler != null) {
                selectApacheWebServerHandler.handle(new ActionEvent(simpleWebServerSwitchButton, simpleWebServerSwitchButton));
            }
        });
        nginxItem.setOnAction(menuEvent -> {
            if (selectNginxWebServerHandler != null) {
                selectNginxWebServerHandler.handle(new ActionEvent(simpleWebServerSwitchButton, simpleWebServerSwitchButton));
            }
        });
        menu.getItems().addAll(apacheItem, nginxItem);
        if (selectApacheWebServerHandler == null || selectNginxWebServerHandler == null) {
            fallbackHandler.handle(event);
            return;
        }
        menu.show(simpleWebServerSwitchButton, javafx.geometry.Side.BOTTOM, 0, 6);
    }

    public void setOnStartAgent(EventHandler<ActionEvent> handler) {
        startAgentButton.setOnAction(handler);
    }

    public void setOnStopAgent(EventHandler<ActionEvent> handler) {
        stopAgentButton.setOnAction(handler);
    }

    public void setOnRestartAgent(EventHandler<ActionEvent> handler) {
        restartAgentButton.setOnAction(handler);
    }

    public void setOnOpenPanel(EventHandler<ActionEvent> handler) {
        openPanelButton.setOnAction(handler);
    }

    public void setOnOpenComponents(EventHandler<ActionEvent> handler) {
        openComponentsButton.setOnAction(handler);
    }

    public void setOnOpenHistory(EventHandler<ActionEvent> handler) {
        openHistoryButton.setOnAction(handler);
    }

    public void setOnOpenCache(EventHandler<ActionEvent> handler) {
        openCacheButton.setOnAction(handler);
    }

    public void setOnOpenApps(EventHandler<ActionEvent> handler) {
        openAppsButton.setOnAction(handler);
    }

    public void setOnOpenProcess(EventHandler<ActionEvent> handler) {
        openProcessButton.setOnAction(handler);
    }

    public void setOnOpenLocalPackages(EventHandler<ActionEvent> handler) {
        openLocalPackagesButton.setOnAction(handler);
    }

    public void setOnOpenRuntimeVersions(EventHandler<ActionEvent> handler) {
        openRuntimeVersionsButton.setOnAction(handler);
    }

    public void setOnOpenProjects(EventHandler<ActionEvent> handler) {
        openProjectsButton.setOnAction(handler);
    }

    public void setOnOpenVirtualHosts(EventHandler<ActionEvent> handler) {
        openVirtualHostsButton.setOnAction(handler);
    }

    public void setOnOpenNginxReload(EventHandler<ActionEvent> handler) {
        openNginxReloadButton.setOnAction(handler);
    }

    public void setOnOpenNginxExecutable(EventHandler<ActionEvent> handler) {
        openNginxExecutableButton.setOnAction(handler);
    }

    public void setOnOpenNginxRealValidate(EventHandler<ActionEvent> handler) {
        openNginxRealValidateButton.setOnAction(handler);
    }

    public void setOnOpenNginxRealReload(EventHandler<ActionEvent> handler) {
        openNginxRealReloadButton.setOnAction(handler);
    }

    public void setOnOpenNginxPreflight(EventHandler<ActionEvent> handler) {
        openNginxPreflightButton.setOnAction(handler);
    }

    public void setOnOpenHostsPublish(EventHandler<ActionEvent> handler) {
        openHostsPublishButton.setOnAction(handler);
    }

    public void setOnOpenHostsApply(EventHandler<ActionEvent> handler) {
        openHostsApplyButton.setOnAction(handler);
    }

    public void setOnOpenWebServerProfiles(EventHandler<ActionEvent> handler) {
        openWebServerProfilesButton.setOnAction(handler);
    }

    public void setOnOpenApacheVhosts(EventHandler<ActionEvent> handler) {
        openApacheVhostsButton.setOnAction(handler);
    }

    public void setOnOpenApachePublish(EventHandler<ActionEvent> handler) {
        openApachePublishButton.setOnAction(handler);
    }

    public void setOnOpenApacheValidate(EventHandler<ActionEvent> handler) {
        openApacheValidateButton.setOnAction(handler);
    }

    public void setOnOpenApacheExecutable(EventHandler<ActionEvent> handler) {
        openApacheExecutableButton.setOnAction(handler);
    }

    public void setOnOpenApacheRealValidate(EventHandler<ActionEvent> handler) {
        openApacheRealValidateButton.setOnAction(handler);
    }

    public void setOnOpenApacheRealReload(EventHandler<ActionEvent> handler) {
        openApacheRealReloadButton.setOnAction(handler);
    }

    public void setOnOpenServiceAdapters(EventHandler<ActionEvent> handler) {
        openServiceAdaptersButton.setOnAction(handler);
    }

    public void setOnServiceList(EventHandler<ActionEvent> handler) {
        setButtonAction(serviceListButton, handler);
        setButtonAction(compactServiceRefreshButton, handler);
    }

    public void setOnApacheStatus(EventHandler<ActionEvent> handler) {
        apacheStatusButton.setOnAction(handler);
    }

    public void setOnApachePreflight(EventHandler<ActionEvent> handler) {
        apachePreflightButton.setOnAction(handler);
    }

    public void setOnApacheStart(EventHandler<ActionEvent> handler) {
        setButtonAction(apacheStartButton, handler);
        setButtonAction(compactApacheStartButton, handler);
    }

    public void setOnApacheStop(EventHandler<ActionEvent> handler) {
        setButtonAction(apacheStopButton, handler);
        setButtonAction(compactApacheStopButton, handler);
    }

    public void setOnApacheRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(apacheRestartButton, handler);
        setButtonAction(compactApacheRestartButton, handler);
    }

    public void setOnNginxStatus(EventHandler<ActionEvent> handler) {
        nginxStatusButton.setOnAction(handler);
    }

    public void setOnNginxPreflight(EventHandler<ActionEvent> handler) {
        nginxPreflightButton.setOnAction(handler);
    }

    public void setOnNginxStart(EventHandler<ActionEvent> handler) {
        setButtonAction(nginxStartButton, handler);
        setButtonAction(compactNginxStartButton, handler);
    }

    public void setOnNginxStop(EventHandler<ActionEvent> handler) {
        setButtonAction(nginxStopButton, handler);
        setButtonAction(compactNginxStopButton, handler);
    }

    public void setOnNginxRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(nginxRestartButton, handler);
        setButtonAction(compactNginxRestartButton, handler);
    }

    public void setOnMysqlStatus(EventHandler<ActionEvent> handler) {
        mysqlStatusButton.setOnAction(handler);
    }

    public void setOnMysqlPreflight(EventHandler<ActionEvent> handler) {
        mysqlPreflightButton.setOnAction(handler);
    }

    public void setOnMysqlStart(EventHandler<ActionEvent> handler) {
        setButtonAction(mysqlStartButton, handler);
        setButtonAction(compactMysqlStartButton, handler);
    }

    public void setOnMysqlStop(EventHandler<ActionEvent> handler) {
        setButtonAction(mysqlStopButton, handler);
        setButtonAction(compactMysqlStopButton, handler);
    }

    public void setOnMysqlRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(mysqlRestartButton, handler);
        setButtonAction(compactMysqlRestartButton, handler);
    }

    public void setOnPhpStatus(EventHandler<ActionEvent> handler) {
        phpStatusButton.setOnAction(handler);
    }

    public void setOnPhpPreflight(EventHandler<ActionEvent> handler) {
        phpPreflightButton.setOnAction(handler);
    }

    public void setOnPhpStart(EventHandler<ActionEvent> handler) {
        setButtonAction(phpStartButton, handler);
        setButtonAction(compactPhpStartButton, handler);
    }

    public void setOnPhpStop(EventHandler<ActionEvent> handler) {
        setButtonAction(phpStopButton, handler);
        setButtonAction(compactPhpStopButton, handler);
    }

    public void setOnPhpRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(phpRestartButton, handler);
        setButtonAction(compactPhpRestartButton, handler);
    }

    public void setOnMailpitStatus(EventHandler<ActionEvent> handler) {
        mailpitStatusButton.setOnAction(handler);
    }

    public void setOnMailpitPreflight(EventHandler<ActionEvent> handler) {
        mailpitPreflightButton.setOnAction(handler);
    }

    public void setOnMailpitStart(EventHandler<ActionEvent> handler) {
        setButtonAction(mailpitStartButton, handler);
        setButtonAction(compactMailpitStartButton, handler);
    }

    public void setOnMailpitStop(EventHandler<ActionEvent> handler) {
        setButtonAction(mailpitStopButton, handler);
        setButtonAction(compactMailpitStopButton, handler);
    }

    public void setOnMailpitRestart(EventHandler<ActionEvent> handler) {
        setButtonAction(mailpitRestartButton, handler);
        setButtonAction(compactMailpitRestartButton, handler);
    }

    public void setOnRuntimeList(EventHandler<ActionEvent> handler) {
        runtimeListButton.setOnAction(handler);
    }

    public void setOnRuntimeScanBin(EventHandler<ActionEvent> handler) {
        runtimeScanBinButton.setOnAction(handler);
    }

    public void setOnRuntimeApacheActive(EventHandler<ActionEvent> handler) {
        runtimeApacheActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeApacheActivate(EventHandler<ActionEvent> handler) {
        runtimeApacheActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeApacheActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeApacheActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeNginxActive(EventHandler<ActionEvent> handler) {
        runtimeNginxActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeNginxActivate(EventHandler<ActionEvent> handler) {
        runtimeNginxActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeNginxActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeNginxActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeMysqlActive(EventHandler<ActionEvent> handler) {
        runtimeMysqlActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeMysqlActivate(EventHandler<ActionEvent> handler) {
        runtimeMysqlActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeMysqlActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeMysqlActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimePhpActive(EventHandler<ActionEvent> handler) {
        runtimePhpActiveButton.setOnAction(handler);
    }

    public void setOnRuntimePhpActivate(EventHandler<ActionEvent> handler) {
        runtimePhpActivateButton.setOnAction(handler);
    }

    public void setOnRuntimePhpActivatePortable(EventHandler<ActionEvent> handler) {
        runtimePhpActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeNodeActive(EventHandler<ActionEvent> handler) {
        runtimeNodeActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeNodeActivate(EventHandler<ActionEvent> handler) {
        runtimeNodeActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeNodeActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeNodeActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimePythonActive(EventHandler<ActionEvent> handler) {
        runtimePythonActiveButton.setOnAction(handler);
    }

    public void setOnRuntimePythonActivate(EventHandler<ActionEvent> handler) {
        runtimePythonActivateButton.setOnAction(handler);
    }

    public void setOnRuntimePythonActivatePortable(EventHandler<ActionEvent> handler) {
        runtimePythonActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeMemcachedActive(EventHandler<ActionEvent> handler) {
        runtimeMemcachedActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeMemcachedActivate(EventHandler<ActionEvent> handler) {
        runtimeMemcachedActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeMemcachedActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeMemcachedActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeRedisActive(EventHandler<ActionEvent> handler) {
        runtimeRedisActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeRedisActivate(EventHandler<ActionEvent> handler) {
        runtimeRedisActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeRedisActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeRedisActivatePortableButton.setOnAction(handler);
    }

    public void setOnRuntimeMailpitActive(EventHandler<ActionEvent> handler) {
        runtimeMailpitActiveButton.setOnAction(handler);
    }

    public void setOnRuntimeMailpitActivate(EventHandler<ActionEvent> handler) {
        runtimeMailpitActivateButton.setOnAction(handler);
    }

    public void setOnRuntimeMailpitActivatePortable(EventHandler<ActionEvent> handler) {
        runtimeMailpitActivatePortableButton.setOnAction(handler);
    }

    public void setOnHostsAutoInspect(EventHandler<ActionEvent> handler) {
        setButtonAction(quickHostsAutoInspectButton, handler);
        setButtonAction(settingsHostsAutoInspectButton, handler);
    }

    public void setOnHostsAutoRepairPlan(EventHandler<ActionEvent> handler) {
        setButtonAction(settingsHostsAutoRepairPlanButton, handler);
    }

    public void setOnHostsAutoRepair(EventHandler<ActionEvent> handler) {
        setButtonAction(settingsHostsAutoRepairButton, handler);
    }

    public void setOnQuickAppTemplates(EventHandler<ActionEvent> handler) {
        quickAppTemplatesButton.setOnAction(handler);
    }

    public void setOnQuickAppPlan(EventHandler<ActionEvent> handler) {
        quickAppPlanButton.setOnAction(handler);
    }

    public void setOnQuickAppCreate(EventHandler<ActionEvent> handler) {
        quickAppCreateButton.setOnAction(handler);
    }

    public void setOnWorkflowProfile(EventHandler<ActionEvent> handler) {
        workflowProfileButton.setOnAction(handler);
    }

    public void setOnWorkflowPlan(EventHandler<ActionEvent> handler) {
        workflowPlanButton.setOnAction(handler);
    }

    public void setOnWorkflowDryRun(EventHandler<ActionEvent> handler) {
        workflowDryRunButton.setOnAction(handler);
    }

    public void setOnWorkflowRuns(EventHandler<ActionEvent> handler) {
        workflowRunsButton.setOnAction(handler);
    }

    public void setOnWorkflowLocks(EventHandler<ActionEvent> handler) {
        workflowLocksButton.setOnAction(handler);
    }

    public void setOnCheckStatus(EventHandler<ActionEvent> handler) {
        checkStatusButton.setOnAction(handler);
    }

    public void updateServiceSummary(ServiceManagerSummary summary) {
        if (summary == null) {
            return;
        }

        if (!summary.hasServiceCode() || !summary.hasStatus()) {
            return;
        }

        String value = summary.isSuccess() ? summary.getStatus() : "error";
        switch (summary.getServiceCode()) {
            case DesktopApiConfig.SERVICE_CODE_APACHE -> updateServiceLabels(serviceApacheStatusValue, compactApacheStatusValue, value);
            case DesktopApiConfig.SERVICE_CODE_NGINX -> updateServiceLabels(serviceNginxStatusValue, compactNginxStatusValue, value);
            case DesktopApiConfig.SERVICE_CODE_MYSQL -> updateServiceLabels(serviceMysqlStatusValue, compactMysqlStatusValue, value);
            case DesktopApiConfig.SERVICE_CODE_PHP -> updateServiceLabels(servicePhpStatusValue, compactPhpStatusValue, value);
            case DesktopApiConfig.SERVICE_CODE_MAILPIT -> updateServiceLabels(serviceMailpitStatusValue, compactMailpitStatusValue, value);
            default -> {
            }
        }

        if (summary.getServiceCode().equals(activeWebServerServiceCode())) {
            simpleWebServerStatusValue.setText(value);
            applyStatusStyle(simpleWebServerStatusValue, value);
        }

        appendServiceLogEntry(summary.getServiceCode(), value);
    }

    private void appendServiceLogEntry(String serviceCode, String value) {
        String line = serviceCode + " -> " + value + "\n";
        switch (serviceCode) {
            case DesktopApiConfig.SERVICE_CODE_APACHE -> apacheLogArea.appendText(line);
            case DesktopApiConfig.SERVICE_CODE_NGINX -> nginxLogArea.appendText(line);
            case DesktopApiConfig.SERVICE_CODE_PHP -> phpLogArea.appendText(line);
            case DesktopApiConfig.SERVICE_CODE_MYSQL -> mysqlLogArea.appendText(line);
            case DesktopApiConfig.SERVICE_CODE_MAILPIT -> mailpitLogArea.appendText(line);
            default -> systemLogArea.appendText(line);
        }
    }

    private void updateServiceLabels(Label summaryLabel, Label compactLabel, String value) {
        summaryLabel.setText(value);
        compactLabel.setText(value);
        applyStatusStyle(summaryLabel, value);
        applyStatusStyle(compactLabel, value);
    }

    private void applyStatusStyle(Label label, String value) {
        label.getStyleClass().removeAll("jhoster-status-running", "jhoster-status-disabled", "jhoster-status-error", "jhoster-status-stopped");
        String normalized = value == null ? "" : value.toLowerCase();
        if (normalized.contains("running") || normalized.contains("active") || normalized.contains("ok")) {
            label.getStyleClass().add("jhoster-status-running");
            return;
        }
        if (normalized.contains("disabled")) {
            label.getStyleClass().add("jhoster-status-disabled");
            return;
        }
        if (normalized.contains("error") || normalized.contains("fail")) {
            label.getStyleClass().add("jhoster-status-error");
            return;
        }
        label.getStyleClass().add("jhoster-status-stopped");
    }

    public void updateRuntimeSummary(RuntimeManagerSummary summary) {
        if (summary == null) {
            return;
        }

        if (summary.hasCount()) {
            runtimeCountValue.setText(String.valueOf(summary.getCount()));
        }

        if (!summary.hasFamily()) {
            return;
        }

        String value = summary.isSuccess() ? summary.toDisplayValue() : "error";
        switch (summary.getFamily()) {
            case DesktopApiConfig.RUNTIME_FAMILY_PHP -> runtimePhpActiveValue.setText(value);
            case DesktopApiConfig.RUNTIME_FAMILY_NODE -> runtimeNodeActiveValue.setText(value);
            case DesktopApiConfig.RUNTIME_FAMILY_PYTHON -> runtimePythonActiveValue.setText(value);
            default -> {
            }
        }
    }

    public void updateQuickAppSummary(QuickAppSummary summary) {
        if (summary == null) {
            return;
        }

        if (summary.hasCount()) {
            quickAppTemplateCountValue.setText(String.valueOf(summary.getCount()));
        }

        updateLabelIfPresent(quickAppLastProjectValue, summary.hasProjectCode(), summary.getProjectCode());
        updateLabelIfPresent(quickAppLastTemplateValue, summary.hasTemplateCode(), summary.getTemplateCode());
        updateLabelIfPresent(quickAppLastStatusValue, summary.hasStatus(), summary.getStatus());
        updateLabelIfPresent(quickAppStackSummaryValue, summary.hasStackLabel(), summary.getStackLabel());
        updateLabelIfPresent(quickAppProvisioningSummaryValue, summary.hasProvisioningStatus(), summary.getProvisioningStatus());
        updateLabelIfPresent(quickAppDatabaseSummaryValue, summary.hasDatabaseLabel(), summary.getDatabaseLabel());
    }

    public void updateWorkflowSummary(WorkflowDesktopSummary summary) {
        if (summary == null) {
            return;
        }

        updateLabelIfPresent(summaryProfileValue, summary.hasWebServer(), summary.getWebServer());
        if (summary.hasWebServer()) {
            syncActiveWebServerDisplay(summary.getWebServer());
        }
        updateLabelIfPresent(summaryStatusValue, summary.hasStatus(), summary.getStatus());
        updateLabelIfPresent(summaryStepCountValue, summary.hasStepCount(), String.valueOf(summary.getStepCount()));
        updateLabelIfPresent(summaryRunIdValue, summary.hasRunId(), shortenRunId(summary.getRunId()));

        if (SUMMARY_RUNS_TITLE.equals(summary.getTitle()) && summary.hasRecordCount()) {
            summaryRunCountValue.setText(String.valueOf(summary.getRecordCount()));
        }

        if (SUMMARY_LOCKS_TITLE.equals(summary.getTitle()) && summary.hasRecordCount()) {
            summaryLockCountValue.setText(String.valueOf(summary.getRecordCount()));
        }
    }

    private void updateLabelIfPresent(Label label, boolean shouldUpdate, String value) {
        if (shouldUpdate) {
            label.setText(value);
        }
    }

    private String shortenRunId(String runId) {
        if (runId == null || runId.length() <= RUN_ID_MAX_VISIBLE_LENGTH) {
            return runId == null ? SUMMARY_VALUE_EMPTY : runId;
        }

        return runId.substring(0, RUN_ID_MAX_VISIBLE_LENGTH) + "...";
    }

    public void appendLog(String message) {
        String line = message + "\n";
        logArea.appendText(line);
        if (message != null && message.toLowerCase().contains("agent")) {
            agentLogArea.appendText(line);
        }
    }
}
