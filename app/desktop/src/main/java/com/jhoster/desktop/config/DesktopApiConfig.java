// # 📄 Dosya Yolu: E:\JHoster\app\desktop\src\main\java\com\jhoster\desktop\config\DesktopApiConfig.java
// # 📌 Amac: Desktop API route ve varsayilan workflow/service/runtime manager ve quick app, quick action ve compact dashboard degerlerini merkezi olarak tutar
// # 📌 Modul - Java
// # Version: 3.76.0
// # Aciklama: JavaFX tarafinda agent URL, quick app plan route, license route, hosts auto UI route, feature registry, package downloader, aktif web server mode, fullscreen layout ve New Site stack secimi ayarlarini merkezi tutar
// # Bagimli Oldugu Katman: Config

package com.jhoster.desktop.config;

public final class DesktopApiConfig {
    public static final String AGENT_BASE_URL = "http://127.0.0.1:8751";

    public static final String ROOT_ROUTE = "/";
    public static final String HEALTH_ROUTE = "/api/v1/health";
    public static final String COMPONENTS_ROUTE = "/api/v1/components";
    public static final String INSTALL_HISTORY_ROUTE = "/api/v1/install/history";
    public static final String CACHE_ROUTE = "/api/v1/cache";
    public static final String APPS_ROUTE = "/api/v1/apps";
    public static final String PROCESS_ROUTE = "/api/v1/process";
    public static final String SERVICE_ADAPTERS_ROUTE = "/api/v1/service-adapters";
    public static final String LOCAL_PACKAGES_ROUTE = "/api/v1/local-packages";
    public static final String PACKAGE_DOWNLOADS_ROUTE = "/api/v1/package-downloads";
    public static final String RUNTIME_VERSIONS_ROUTE = "/api/v1/runtime-versions";
    public static final String PROJECTS_ROUTE = "/api/v1/projects";
    public static final String QUICK_APPS_ROUTE = "/api/v1/quick-apps";
    public static final String LICENSE_ROUTE = "/api/v1/license";
    public static final String VIRTUAL_HOSTS_ROUTE = "/api/v1/virtual-hosts";
    public static final String NGINX_RELOAD_ROUTE = "/api/v1/nginx-reload";
    public static final String NGINX_EXECUTABLE_ROUTE = "/api/v1/nginx-executable";
    public static final String NGINX_REAL_VALIDATE_ROUTE = "/api/v1/nginx-real-validate";
    public static final String NGINX_REAL_RELOAD_ROUTE = "/api/v1/nginx-real-reload";
    public static final String NGINX_PREFLIGHT_ROUTE = "/api/v1/nginx-execution-preflight";
    public static final String HOSTS_PUBLISH_ROUTE = "/api/v1/hosts-publish";
    public static final String HOSTS_APPLY_ROUTE = "/api/v1/hosts-apply";
    public static final String HOSTS_AUTO_ROUTE = "/api/v1/hosts-auto";
    public static final String HOSTS_AUTO_INSPECT_ROUTE = "/api/v1/hosts-auto/inspect";
    public static final String HOSTS_AUTO_REPAIR_PLAN_ROUTE = "/api/v1/hosts-auto/repair-plan";
    public static final String HOSTS_AUTO_REPAIR_ROUTE = "/api/v1/hosts-auto/repair";
    public static final String HOSTS_AUTO_REAL_WRITE_QUERY = "?real_write=true";
    public static final String HOSTS_AUTO_REPAIR_REAL_QUERY = "?real_write=true&dry_run=false";
    public static final String HOSTS_AUTO_REPAIR_PLAN_REAL_QUERY = "?real_write=true";
    public static final String WEB_SERVER_PROFILES_ROUTE = "/api/v1/web-server-profiles";
    public static final String WEB_SERVER_CURRENT_PROFILE_ROUTE = "/api/v1/web-server-profiles/current";
    public static final String WEB_SERVER_PROFILE_APACHE = "apache";
    public static final String WEB_SERVER_PROFILE_NGINX = "nginx";
    public static final String WEB_SERVER_PROFILE_APACHE_SELECT_ROUTE = "/api/v1/web-server-profiles/apache/select";
    public static final String WEB_SERVER_PROFILE_NGINX_SELECT_ROUTE = "/api/v1/web-server-profiles/nginx/select";
    public static final String WEB_SERVER_PROFILE_SELECT_DRY_RUN_FALSE_QUERY = "?dry_run=false";
    public static final String WEB_SERVER_SHARED_DOCUMENT_ROOT = "www";
    public static final String WEB_SERVER_WORKFLOW_ROUTE = "/api/v1/web-server-workflow";
    public static final String WEB_SERVER_WORKFLOW_RUNS_ROUTE = "/api/v1/web-server-workflow/runs";
    public static final String WEB_SERVER_WORKFLOW_LOCKS_ROUTE = "/api/v1/web-server-workflow/locks";
    public static final String APACHE_VHOSTS_ROUTE = "/api/v1/apache-vhosts";
    public static final String APACHE_PUBLISH_ROUTE = "/api/v1/apache-publish";
    public static final String APACHE_VALIDATE_ROUTE = "/api/v1/apache-validate";
    public static final String APACHE_EXECUTABLE_ROUTE = "/api/v1/apache-executable";
    public static final String APACHE_REAL_VALIDATE_ROUTE = "/api/v1/apache-real-validate";
    public static final String APACHE_REAL_RELOAD_ROUTE = "/api/v1/apache-real-reload";
    public static final String FOLDER_LAYOUT_ROUTE = "/api/v1/folder-layout";

    public static final String DEFAULT_WORKFLOW_PROJECT_CODE = "demo-site";
    public static final String DEFAULT_WORKFLOW_DOMAIN = "demo-site.test";
    public static final String DEFAULT_WORKFLOW_TARGET_DIR = "";
    public static final int DEFAULT_WORKFLOW_PORT = 80;
    public static final boolean DEFAULT_WORKFLOW_RELOAD = true;
    public static final boolean DEFAULT_WORKFLOW_ROLLBACK_ON_FAILURE = true;
    public static final boolean SAFE_REAL_EXECUTION = false;
    public static final boolean SAFE_DRY_RUN = true;
    public static final String SERVICE_CODE_APACHE = "apache";
    public static final String SERVICE_CODE_NGINX = "nginx";
    public static final String SERVICE_CODE_MYSQL = "mysql";
    public static final String SERVICE_CODE_PHP = "php";
    public static final String SERVICE_CODE_MAILPIT = "mailpit";
    public static final String SERVICE_CODE_REDIS = "redis";
    public static final String SERVICE_CODE_MEMCACHED = "memcached";
    public static final String SERVICE_CODE_SENDMAIL = "sendmail";
    public static final boolean SERVICE_MANAGER_STATE_DRY_RUN = false;
    public static final boolean SERVICE_MANAGER_REAL_EXECUTION = false;
    public static final String RUNTIME_FAMILY_APACHE = "apache";
    public static final String RUNTIME_FAMILY_NGINX = "nginx";
    public static final String RUNTIME_FAMILY_MYSQL = "mysql";
    public static final String RUNTIME_FAMILY_PHP = "php";
    public static final String RUNTIME_FAMILY_NODE = "node";
    public static final String RUNTIME_FAMILY_PYTHON = "python";
    public static final String RUNTIME_FAMILY_MEMCACHED = "memcached";
    public static final String RUNTIME_FAMILY_REDIS = "redis";
    public static final String RUNTIME_FAMILY_MAILPIT = "mailpit";
    public static final String DEFAULT_APACHE_RUNTIME_CODE = "apache";
    public static final String DEFAULT_NGINX_RUNTIME_CODE = "nginx";
    public static final String DEFAULT_MYSQL_RUNTIME_CODE = "mysql";
    public static final String DEFAULT_PHP_RUNTIME_CODE = "php";
    public static final String DEFAULT_NODE_RUNTIME_CODE = "node";
    public static final String DEFAULT_PYTHON_RUNTIME_CODE = "python";
    public static final String DEFAULT_MEMCACHED_RUNTIME_CODE = "memcached";
    public static final String DEFAULT_REDIS_RUNTIME_CODE = "redis";
    public static final String DEFAULT_MAILPIT_RUNTIME_CODE = "mailpit";
    public static final String DEFAULT_PACKAGE_DOWNLOAD_CODE = "nginx-windows-stable";
    public static final String DEFAULT_APACHE_RUNTIME_FOLDER = "httpd-2.4.66-260223-Win64-VS18";
    public static final String DEFAULT_NGINX_RUNTIME_FOLDER = "nginx-1.28.2";
    public static final String DEFAULT_MYSQL_RUNTIME_FOLDER = "mysql-8.0.30-winx64";
    public static final String DEFAULT_PHP_RUNTIME_FOLDER = "php-8.3.30-Win32-vs16-x64";
    public static final String DEFAULT_NODE_RUNTIME_FOLDER = "node-v22";
    public static final String DEFAULT_PYTHON_RUNTIME_FOLDER = "python-3.13";
    public static final String DEFAULT_MEMCACHED_RUNTIME_FOLDER = "memcached-1.6.8-win64-mingw";
    public static final String DEFAULT_REDIS_RUNTIME_FOLDER = "redis-7.2.4";
    public static final String DEFAULT_MAILPIT_RUNTIME_FOLDER = "mailpit-1.22.3";
    public static final boolean RUNTIME_MANAGER_ACTIVATE_DRY_RUN = false;
    public static final String DEFAULT_QUICK_APP_PROJECT_CODE = "demo-quick-app";
    public static final String DEFAULT_QUICK_APP_PROJECT_NAME = "Demo Quick App";
    public static final String DEFAULT_QUICK_APP_TEMPLATE_CODE = "php-empty";
    public static final String DEFAULT_QUICK_APP_DOMAIN = "demo-quick-app.test";
    public static final int DEFAULT_QUICK_APP_PORT = 80;
    public static final String DEFAULT_QUICK_APP_WEB_SERVER = WEB_SERVER_PROFILE_APACHE;
    public static final boolean DEFAULT_QUICK_APP_INCLUDE_MYSQL = true;
    public static final boolean DEFAULT_QUICK_APP_INCLUDE_PHP = true;
    public static final boolean DEFAULT_QUICK_APP_INCLUDE_MAILPIT = false;
    public static final boolean QUICK_APP_CREATE_DRY_RUN = false;
    public static final String QUICK_APP_PLAN_ROUTE = QUICK_APPS_ROUTE + "/" + DEFAULT_QUICK_APP_PROJECT_CODE + "/plan";

    public static final String QUICK_ACTION_WEB_URL = "http://localhost";
    public static final String QUICK_ACTION_MAILPIT_URL = "http://localhost:8025";
    public static final String QUICK_ACTION_ROOT_FOLDER = "";
    public static final String QUICK_ACTION_PROJECTS_FOLDER = "www";
    public static final String QUICK_ACTION_LOGS_FOLDER = "logs";
    public static final String QUICK_ACTION_SETTINGS_FOLDER = "etc/jhoster";
    public static final String QUICK_ACTION_TERMINAL_EXECUTABLE = "powershell.exe";
    public static final String QUICK_ACTION_TERMINAL_NO_EXIT_ARG = "-NoExit";
    public static final String QUICK_ACTION_TERMINAL_COMMAND_ARG = "-Command";
    public static final String QUICK_ACTION_TERMINAL_SET_LOCATION_COMMAND = "Set-Location -LiteralPath";
    public static final String QUICK_ACTION_HEIDISQL_RELATIVE_PATH_PRIMARY = "bin/heidisql/heidisql.exe";
    public static final String QUICK_ACTION_HEIDISQL_RELATIVE_PATH_TOOLS = "app/tools/heidisql/heidisql.exe";
    public static final String QUICK_ACTION_HEIDISQL_RELATIVE_PATH_APPS = "app/resources/heidisql/heidisql.exe";
    public static final String QUICK_ACTION_HEIDISQL_RELATIVE_PATH_USR = "data/user/bin/heidisql/heidisql.exe";
    public static final String QUICK_ACTION_CMDER_RELATIVE_PATH_PRIMARY = "bin/cmder/Cmder.exe";
    public static final String QUICK_ACTION_CMDER_RELATIVE_PATH_ALT = "bin/cmder/cmder.exe";
    public static final String QUICK_ACTION_GIT_BASH_RELATIVE_PATH_PRIMARY = "bin/git/git-bash.exe";
    public static final String QUICK_ACTION_GIT_BASH_RELATIVE_PATH_ALT = "bin/git/bin/bash.exe";
    public static final String QUICK_ACTION_NOTEPAD_RELATIVE_PATH_PRIMARY = "bin/notepad++/notepad++.exe";
    public static final String QUICK_ACTION_NOTEPAD_RELATIVE_PATH_ALT = "bin/notepadpp/notepad++.exe";
    public static final String QUICK_ACTION_NGROK_RELATIVE_PATH_PRIMARY = "bin/ngrok/ngrok.exe";
    public static final String QUICK_ACTION_COMPOSER_RELATIVE_PATH_PRIMARY = "bin/composer/composer.bat";
    public static final String QUICK_ACTION_YARN_RELATIVE_PATH_PRIMARY = "bin/yarn/yarn.cmd";
    public static final String QUICK_ACTION_BIN_FOLDER = "bin";
    public static final String QUICK_ACTION_APP_DIRECTORY_NAME = "app";
    public static final String QUICK_ACTION_DESKTOP_DIRECTORY_NAME = "desktop";
    public static final String QUICK_ACTION_AGENT_DIRECTORY_NAME = "agent";
    public static final String QUICK_ACTION_FOUND_MESSAGE = "opened";
    public static final String QUICK_ACTION_MISSING_MESSAGE = "missing";

    private DesktopApiConfig() {
    }

    public static String resolveUrl(String route) {
        return AGENT_BASE_URL + route;
    }
}
