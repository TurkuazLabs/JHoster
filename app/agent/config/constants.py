# 📄 Dosya Yolu: E:\JHoster\app\agent\config\constants.py
# 📌 Amac: JHoster agent sabit degerlerini merkezi olarak tanimlar
# 📌 Modul - FileType
# Version: 3.80.0
# Aciklama: Route, dosya adi, sade root layout, manifest, executor, cache, package downloader, app registry, process, web server mode, port guard, portable version, quick app, web server workflow ve layout sabitleri
# Bagimli Oldugu Katman: Config

CONFIG_FILE_NAME = "agent.yml"
STATE_FILE_NAME = "agent_state.json"
INSTALL_HISTORY_FILE_NAME = "install_history.json"
APP_REGISTRY_FILE_NAME = "app_registry.json"
PROCESS_STATE_FILE_NAME = "process_state.json"
RUNTIME_VERSION_STATE_FILE_NAME = "runtime_versions.json"
PACKAGE_DOWNLOAD_REGISTRY_FILE_NAME = "package_download_registry.json"
STACK_PROVISIONING_CONFIG_FILE_NAME = "stack_provisioning.yml"
PROVISIONING_APPLY_REGISTRY_FILE_NAME = "provisioning_apply_registry.json"
PROJECT_REGISTRY_FILE_NAME = "project_registry.json"
LICENSE_STATE_FILE_NAME = "license_state.json"
VIRTUAL_HOST_REGISTRY_FILE_NAME = "virtual_host_registry.json"
NGINX_PUBLISH_REGISTRY_FILE_NAME = "nginx_publish_registry.json"
NGINX_VALIDATE_REGISTRY_FILE_NAME = "nginx_validate_registry.json"
NGINX_RELOAD_REGISTRY_FILE_NAME = "nginx_reload_registry.json"
NGINX_EXECUTABLE_REGISTRY_FILE_NAME = "nginx_executable_registry.json"
NGINX_REAL_VALIDATE_REGISTRY_FILE_NAME = "nginx_real_validate_registry.json"
NGINX_REAL_RELOAD_REGISTRY_FILE_NAME = "nginx_real_reload_registry.json"
NGINX_EXECUTION_PREFLIGHT_REGISTRY_FILE_NAME = "nginx_execution_preflight_registry.json"
HOSTS_PUBLISH_REGISTRY_FILE_NAME = "hosts_publish_registry.json"
HOSTS_APPLY_REGISTRY_FILE_NAME = "hosts_apply_registry.json"
HOSTS_AUTO_REGISTRY_FILE_NAME = "hosts_auto_registry.json"
WEB_SERVER_PROFILE_REGISTRY_FILE_NAME = "web_server_profile_registry.json"
APACHE_VHOST_REGISTRY_FILE_NAME = "apache_vhost_registry.json"
APACHE_PUBLISH_REGISTRY_FILE_NAME = "apache_publish_registry.json"
APACHE_VALIDATE_REGISTRY_FILE_NAME = "apache_validate_registry.json"
APACHE_EXECUTABLE_REGISTRY_FILE_NAME = "apache_executable_registry.json"
APACHE_REAL_VALIDATE_REGISTRY_FILE_NAME = "apache_real_validate_registry.json"
APACHE_REAL_RELOAD_REGISTRY_FILE_NAME = "apache_real_reload_registry.json"
WEB_SERVER_WORKFLOW_REGISTRY_FILE_NAME = "web_server_workflow_registry.json"
WEB_SERVER_WORKFLOW_LOCK_REGISTRY_FILE_NAME = "web_server_workflow_lock_registry.json"
QUICK_APP_REGISTRY_FILE_NAME = "quick_app_registry.json"
MANIFEST_FILE_NAME = "manifest.yml"
MODULES_DIRECTORY_NAME = "modules"
CACHE_DIRECTORY_NAME = "cache"
APP_DIRECTORY_NAME = "app"
BIN_DIRECTORY_NAME = "bin"
DATA_DIRECTORY_NAME = "data"
ETC_DIRECTORY_NAME = "etc"
LOGS_DIRECTORY_NAME = "logs"
TMP_DIRECTORY_NAME = "tmp"
WWW_DIRECTORY_NAME = "www"
JHOSTER_DATA_DIRECTORY_NAME = "jhoster"
SIMPLIFIED_ROOT_DIRECTORIES = [
    APP_DIRECTORY_NAME,
    BIN_DIRECTORY_NAME,
    DATA_DIRECTORY_NAME,
    ETC_DIRECTORY_NAME,
    LOGS_DIRECTORY_NAME,
    TMP_DIRECTORY_NAME,
    WWW_DIRECTORY_NAME,
    "backup",
    CACHE_DIRECTORY_NAME,
]
LEGACY_TOP_LEVEL_DIRECTORIES = [
    "apps",
    "config",
    "databases",
    "language",
    "modules",
    "packages",
    "www",
    "readme",
    "runtimes",
    "scripts",
    "services",
    "snapshot",
    "ssl",
    "templates",
    "themes",
    "tools",
    "updater",
    "usr",
]
APPS_DIRECTORY_NAME = "apps"
USER_PROJECTS_DIRECTORY_NAME = "www"
PROJECT_PUBLIC_DIRECTORY_NAME = "public"
PROJECT_CONFIG_FILE_NAME = ".jhoster.yml"
PROJECT_INDEX_FILE_NAME = "index.html"
SNAPSHOT_DIRECTORY_NAME = "snapshot"
VIRTUAL_HOSTS_DIRECTORY_NAME = "vhosts"
NGINX_VHOST_DIRECTORY_NAME = "nginx"
APACHE_VHOST_DIRECTORY_NAME = "apache"
APACHE_PUBLISHED_DIRECTORY_NAME = "apache-published"
NGINX_PUBLISHED_DIRECTORY_NAME = "nginx-published"
HOSTS_DIRECTORY_NAME = "hosts"
HOSTS_PUBLISHED_DIRECTORY_NAME = "hosts-published"
HOSTS_PUBLISHED_FILE_NAME = "hosts.jhoster"
HOSTS_APPLIED_DIRECTORY_NAME = "hosts-applied"
HOSTS_APPLIED_FILE_NAME = "hosts.jhoster"
HOSTS_AUTO_SNAPSHOT_DIRECTORY_NAME = "hosts-auto"
HOSTS_AUTO_SNAPSHOT_FILE_NAME = "hosts.jhoster"
APPLY_DIRECTORY_NAME = "apply"
PUBLISH_DIRECTORY_NAME = "publish"
BACKUP_DIRECTORY_NAME = "backup"
NGINX_VHOST_EXTENSION = ".conf"
MAIN_APP_IMPORT_PATH = "main:app"

ROOT_ROUTE_PATH = "/"
FAVICON_ROUTE_PATH = "/favicon.ico"
ROOT_ROUTE_TAG = "root"

API_VERSION_PREFIX = "/api/v1"
HEALTH_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/health"
HEALTH_ROUTE_TAG = "health"
COMPONENT_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/components"
COMPONENT_ROUTE_TAG = "components"
INSTALLER_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/components"
INSTALLER_ROUTE_TAG = "installer"
INSTALL_HISTORY_ROUTE_PATH = f"{API_VERSION_PREFIX}/install/history"
CACHE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/cache"
CACHE_ROUTE_TAG = "cache"
APPS_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apps"
APPS_ROUTE_TAG = "apps"
PROCESS_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/process"
PROCESS_ROUTE_TAG = "process"
SERVICE_ADAPTER_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/service-adapters"
SERVICE_ADAPTER_ROUTE_TAG = "service-adapters"
LOCAL_PACKAGE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/local-packages"
LOCAL_PACKAGE_ROUTE_TAG = "local-packages"
PACKAGE_DOWNLOAD_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/package-downloads"
PACKAGE_DOWNLOAD_ROUTE_TAG = "package-downloads"
RUNTIME_VERSION_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/runtime-versions"
RUNTIME_VERSION_ROUTE_TAG = "runtime-versions"
PROJECT_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/projects"
PROJECT_ROUTE_TAG = "projects"
LICENSE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/license"
LICENSE_ROUTE_TAG = "license"
QUICK_APP_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/quick-apps"
PROVISIONING_APPLY_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/provisioning-apply"
PROVISIONING_APPLY_ROUTE_TAG = "provisioning-apply"
QUICK_APP_ROUTE_TAG = "quick-apps"
FOLDER_LAYOUT_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/folder-layout"
FOLDER_LAYOUT_ROUTE_TAG = "folder-layout"
VIRTUAL_HOST_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/virtual-hosts"
VIRTUAL_HOST_ROUTE_TAG = "virtual-hosts"
NGINX_PUBLISH_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-publish"
NGINX_PUBLISH_ROUTE_TAG = "nginx-publish"
NGINX_VALIDATE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-validate"
NGINX_VALIDATE_ROUTE_TAG = "nginx-validate"
NGINX_RELOAD_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-reload"
NGINX_RELOAD_ROUTE_TAG = "nginx-reload"
NGINX_EXECUTABLE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-executable"
NGINX_EXECUTABLE_ROUTE_TAG = "nginx-executable"
NGINX_REAL_VALIDATE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-real-validate"
NGINX_REAL_VALIDATE_ROUTE_TAG = "nginx-real-validate"
NGINX_REAL_RELOAD_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-real-reload"
NGINX_REAL_RELOAD_ROUTE_TAG = "nginx-real-reload"
NGINX_EXECUTION_PREFLIGHT_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/nginx-execution-preflight"
NGINX_EXECUTION_PREFLIGHT_ROUTE_TAG = "nginx-execution-preflight"
HOSTS_PUBLISH_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/hosts-publish"
HOSTS_PUBLISH_ROUTE_TAG = "hosts-publish"
HOSTS_APPLY_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/hosts-apply"
HOSTS_APPLY_ROUTE_TAG = "hosts-apply"
HOSTS_AUTO_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/hosts-auto"
HOSTS_AUTO_ROUTE_TAG = "hosts-auto"
WEB_SERVER_PROFILE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/web-server-profiles"
WEB_SERVER_PROFILE_ROUTE_TAG = "web-server-profiles"
APACHE_VHOST_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-vhosts"
APACHE_VHOST_ROUTE_TAG = "apache-vhosts"
APACHE_PUBLISH_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-publish"
APACHE_PUBLISH_ROUTE_TAG = "apache-publish"
APACHE_VALIDATE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-validate"
APACHE_VALIDATE_ROUTE_TAG = "apache-validate"
APACHE_EXECUTABLE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-executable"
APACHE_EXECUTABLE_ROUTE_TAG = "apache-executable"
APACHE_REAL_VALIDATE_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-real-validate"
APACHE_REAL_VALIDATE_ROUTE_TAG = "apache-real-validate"
APACHE_REAL_RELOAD_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/apache-real-reload"
APACHE_REAL_RELOAD_ROUTE_TAG = "apache-real-reload"
WEB_SERVER_WORKFLOW_ROUTE_PREFIX = f"{API_VERSION_PREFIX}/web-server-workflow"
WEB_SERVER_WORKFLOW_ROUTE_TAG = "web-server-workflow"
DOCS_ROUTE_PATH = "/docs"

PACKAGE_SECTION_KEY = "package"
ACTIONS_SECTION_KEY = "actions"
REQUIREMENTS_SECTION_KEY = "requirements"
INSTALLER_SECTION_KEY = "installer"

PACKAGE_CODE_KEY = "code"
PACKAGE_NAME_KEY = "name"
PACKAGE_VERSION_KEY = "version"
PACKAGE_CATEGORY_KEY = "category"
PACKAGE_DESCRIPTION_KEY = "description"
PACKAGE_EDITION_KEY = "edition"

ACTION_TYPE_KEY = "type"
ACTION_NAME_KEY = "name"
ACTION_SOURCE_KEY = "source"
ACTION_TARGET_KEY = "target"
ACTION_CONTENT_KEY = "content"
ACTION_COMMAND_KEY = "command"
ACTION_ALGORITHM_KEY = "algorithm"
ACTION_CHECKSUM_KEY = "checksum"
ACTION_MAX_BYTES_KEY = "max_bytes"
INSTALLER_MODE_KEY = "mode"
INSTALLER_PACKAGE_SOURCE_KEY = "package_source"
INSTALLER_PACKAGE_TARGET_KEY = "package_target"
INSTALLER_PACKAGE_CHECKSUM_KEY = "package_checksum"
INSTALLER_PACKAGE_ALGORITHM_KEY = "package_algorithm"
INSTALLER_PACKAGE_MAX_BYTES_KEY = "package_max_bytes"

ACTION_TYPE_CHECK = "check"
ACTION_TYPE_DOWNLOAD = "download"
ACTION_TYPE_EXTRACT = "extract"
ACTION_TYPE_WRITE_FILE = "write_file"
ACTION_TYPE_ENSURE_DIRECTORY = "ensure_directory"
ACTION_TYPE_VERIFY_CHECKSUM = "verify_checksum"

ACTION_STATUS_PLANNED = "planned"
ACTION_STATUS_OK = "ok"
ACTION_STATUS_BLOCKED = "blocked"
ACTION_STATUS_FAILED = "failed"
ACTION_STATUS_SKIPPED = "skipped"

CHECKSUM_ALGORITHM_SHA256 = "sha256"
ZIP_FILE_EXTENSION = ".zip"

INSTALLER_MODE_PLAN_ONLY = "plan_only"
INSTALLER_MODE_SAFE_ARCHIVE = "safe_archive"
INSTALLER_MODE_LOCAL_PACKAGE = "local_package"

DEFAULT_AGENT_STATE = {
    "state": "ready"
}

DEFAULT_PACKAGE_EDITION = "community"
UNKNOWN_PACKAGE_VALUE = "unknown"

APP_STATUS_INSTALLED = "installed"
APP_STATUS_UNKNOWN = "unknown"

PROCESS_STATUS_RUNNING = "running"
PROCESS_STATUS_STOPPED = "stopped"
PROCESS_STATUS_UNKNOWN = "unknown"
PROCESS_OPERATION_START = "start"
PROCESS_OPERATION_STOP = "stop"
PROCESS_OPERATION_STATUS = "status"
PROCESS_OPERATION_RESTART = "restart"
PROCESS_OPERATION_PREFLIGHT = "preflight"
PROCESS_OPERATION_INSPECT = "inspect"
PROCESS_OPERATION_REAL_PROFILE = "real_profile"
PROCESS_OPERATION_REAL_PROFILE_PLAN = "real_profile_plan"
PROCESS_OPERATION_REAL_PROFILE_APPLY = "real_profile_apply"
PROCESS_MODE_SIMULATED = "simulated"
PROCESS_MODE_REAL = "real"
PROCESS_MESSAGE_DRY_RUN = "dry run only"
PROCESS_MESSAGE_APP_NOT_FOUND = "app_not_found"
PROCESS_MESSAGE_ALREADY_RUNNING = "process already running"
PROCESS_MESSAGE_ALREADY_STOPPED = "process already stopped"
PROCESS_MESSAGE_STARTED = "process marked as running"
PROCESS_MESSAGE_STOPPED = "process marked as stopped"
PROCESS_MESSAGE_RESTARTED = "process restarted"
PROCESS_MESSAGE_STATUS_READY = "process status ready"
PROCESS_MESSAGE_PREFLIGHT_READY = "process preflight ready"
PROCESS_MESSAGE_INSPECTION_READY = "process inspection ready"
PROCESS_MESSAGE_REAL_PROFILE_READY = "real process profile ready"
PROCESS_MESSAGE_REAL_PROFILE_PLANNED = "real process profile plan ready"
PROCESS_MESSAGE_REAL_PROFILE_UPDATED = "real process profile updated"
PROCESS_MESSAGE_REAL_PROFILE_DRY_RUN = "real process profile dry run only"
PROCESS_MESSAGE_REAL_PROFILE_INVALID_PATH = "real process profile invalid path"
PROCESS_MESSAGE_ADAPTER_BLOCKED = "service adapter blocked operation"
PROCESS_MESSAGE_WEB_SERVER_PORT_CONFLICT = "web server port conflict"
SERVICE_CODE_APACHE = "apache"
SERVICE_CODE_NGINX = "nginx"
WEB_SERVER_FRONTEND_CODES = [SERVICE_CODE_APACHE, SERVICE_CODE_NGINX]
WEB_SERVER_PUBLIC_PORTS = [80, 443]
WEB_SERVER_PORTS_KEY = "ports"
WEB_SERVER_HTTP_PORT_KEY = "http"
WEB_SERVER_HTTPS_PORT_KEY = "https"
WEB_SERVER_PORT_GUARD_ALLOWED_KEY = "allowed"
WEB_SERVER_PORT_GUARD_MESSAGE_KEY = "message"
WEB_SERVER_PORT_GUARD_REQUESTED_SERVICE_KEY = "requested_service"
WEB_SERVER_PORT_GUARD_RUNNING_SERVICE_KEY = "running_service"
WEB_SERVER_PORT_GUARD_REQUESTED_PORTS_KEY = "requested_ports"
WEB_SERVER_PORT_GUARD_RUNNING_PORTS_KEY = "running_ports"
WEB_SERVER_PORT_GUARD_SHARED_PORTS_KEY = "shared_ports"
WEB_SERVER_PORT_GUARD_PUBLIC_PORTS_KEY = "public_ports"
WEB_SERVER_PORT_GUARD_POLICY_KEY = "policy"
WEB_SERVER_PORT_GUARD_POLICY_VALUE = "apache_nginx_public_port_exclusive"
WEB_SERVER_PORT_GUARD_OK_MESSAGE = "web server port guard passed"
PROCESS_MESSAGE_WEB_SERVER_PROFILE_MISMATCH = "web server profile mismatch"
PROCESS_MESSAGE_WEB_SERVER_SWITCH_STOP_FAILED = "web server switch stop failed"
WEB_SERVER_PROFILE_RECORDS_KEY = "profile_records"
WEB_SERVER_PROFILE_LEGACY_SELECTED_KEY = "selected_profiles"
WEB_SERVER_PROFILE_SELECTED_FROM_PROCESS = "process_service"
WEB_SERVER_SHARED_DOCUMENT_ROOT_KEY = "shared_document_root"
WEB_SERVER_SHARED_DOCUMENT_ROOT_VALUE = "www"
WEB_SERVER_ACTIVE_PROFILE_KEY = "active_web_server"
SERVICE_ADAPTER_RUNTIME_KEY = "runtime_adapter"
RUNTIME_FAMILY_KEY = "runtime_family"
SERVICE_ADAPTER_MODE_SIMULATED = "simulated"
SERVICE_ADAPTER_MODE_BLOCKED = "blocked"
SERVICE_ADAPTER_MODE_PHP = "php"
SERVICE_ADAPTER_MODE_NGINX = "nginx"
SERVICE_ADAPTER_MODE_APACHE = "apache"
SERVICE_ADAPTER_MODE_MYSQL = "mysql"
SERVICE_ADAPTER_MODE_NODE = "node"
SERVICE_ADAPTER_CAPABILITY_DRY_RUN = "dry_run"
SERVICE_ADAPTER_CAPABILITY_SIMULATED_STATE = "simulated_state"
SERVICE_ADAPTER_CAPABILITY_REAL_PROCESS = "real_process"
SERVICE_ADAPTER_MESSAGE_DRY_RUN = "adapter dry run only"
SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_DISABLED = "real process start is disabled in this version"
SERVICE_ADAPTER_MESSAGE_REAL_EXECUTION_REQUIRED = "real execution requires allow_real_execution"
SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_CONFIG_DISABLED = "real process config is disabled"
SERVICE_ADAPTER_MESSAGE_REAL_EXECUTABLE_MISSING = "real executable is missing"
SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_EXECUTED = "real process command executed"
SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_UNSUPPORTED_OS = "real process execution is supported only on Windows"
SERVICE_ADAPTER_MESSAGE_REAL_STOP_COMMAND_MISSING = "real stop command is missing"
SERVICE_ADAPTER_MESSAGE_REAL_PROCESS_VERIFICATION_FAILED = "real process verification failed"
PATH_SEPARATOR_WINDOWS = "\\"

LOCAL_PACKAGE_STATUS_PLANNED = "planned"
LOCAL_PACKAGE_STATUS_INSTALLED = "installed"
LOCAL_PACKAGE_MESSAGE_DRY_RUN = "local package dry run only"
LOCAL_PACKAGE_MESSAGE_INSTALLED = "local package installed"
LOCAL_PACKAGE_ERROR_NOT_FOUND = "local_package_not_found"
LOCAL_PACKAGE_ERROR_UNSUPPORTED_MODE = "local_package_mode_required"
LOCAL_PACKAGE_ERROR_SOURCE_MISSING = "local_package_source_missing"
LOCAL_PACKAGE_ERROR_TARGET_MISSING = "local_package_target_missing"
LOCAL_PACKAGE_ERROR_CHECKSUM_MISSING = "local_package_checksum_missing"
LOCAL_PACKAGE_ERROR_CHECKSUM_MISMATCH = "checksum_mismatch"
DEFAULT_LOCAL_PACKAGE_MAX_BYTES = 104857600

RUNTIME_VERSION_STATUS_ACTIVE = "active"
RUNTIME_VERSION_STATUS_INACTIVE = "inactive"
RUNTIME_VERSION_MESSAGE_DRY_RUN = "runtime version dry run only"
RUNTIME_VERSION_MESSAGE_ACTIVATED = "runtime version activated"
RUNTIME_VERSION_ERROR_APP_NOT_FOUND = "runtime_app_not_found"
RUNTIME_VERSION_ERROR_FAMILY_NOT_FOUND = "runtime_family_not_found"

RUNTIME_VERSION_PORTABLE_SCAN_SOURCE = "portable-bin-scan"
RUNTIME_VERSION_MESSAGE_PORTABLE_SCAN_READY = "portable runtime scan ready"
RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATED = "portable runtime version activated"
RUNTIME_VERSION_MESSAGE_PORTABLE_ACTIVATE_DRY_RUN = "portable runtime activation dry run only"
RUNTIME_VERSION_ERROR_PORTABLE_FAMILY_NOT_FOUND = "portable_runtime_family_not_found"
RUNTIME_VERSION_ERROR_PORTABLE_FOLDER_NOT_FOUND = "portable_runtime_folder_not_found"

PROJECT_STATUS_PLANNED = "planned"
PROJECT_STATUS_ACTIVE = "active"
PROJECT_STATUS_CREATED = "created"
PROJECT_DEFAULT_RUNTIME_FAMILY = "demo-local-package"
PROJECT_MESSAGE_DRY_RUN = "project dry run only"
PROJECT_MESSAGE_CREATED = "project created"
PROJECT_ERROR_INVALID_CODE = "project_invalid_code"
PROJECT_ERROR_ALREADY_EXISTS = "project_already_exists"
PROJECT_ERROR_NOT_FOUND = "project_not_found"
PROJECT_ERROR_ACTIVE_RUNTIME_NOT_FOUND = "project_active_runtime_not_found"
PROJECT_ERROR_PATH_BLOCKED = "project_path_blocked"
PROJECT_ERROR_COMMUNITY_SITE_LIMIT = "project_community_site_limit"

LICENSE_PLAN_COMMUNITY = "community"
LICENSE_PLAN_PRO = "pro"
LICENSE_DEFAULT_PLAN = LICENSE_PLAN_COMMUNITY
LICENSE_COMMUNITY_MAX_ACTIVE_PROJECTS = 5
LICENSE_PRO_UNLIMITED_LIMIT = -1
LICENSE_MESSAGE_CREATE_ALLOWED = "project create allowed"
LICENSE_MESSAGE_COMMUNITY_SITE_LIMIT = "Community surumde en fazla 5 aktif site kullanabilirsiniz. Daha fazla site icin Pro surume gecebilirsiniz."
LICENSE_LABEL_COMMUNITY = "Community"
LICENSE_LABEL_PRO = "Pro"
LICENSE_USAGE_UNLIMITED_LABEL = "Unlimited"
LICENSE_UPGRADE_HINT = "Pro surum sinirsiz aktif site, gelismis SSL, yedekleme, DNS ve AI modul kapilarini acar."
LICENSE_FEATURE_SITE_LIMIT = "site_limit"
LICENSE_FEATURE_UNLIMITED_SITES = "unlimited_sites"
LICENSE_FEATURE_ADVANCED_SSL = "advanced_ssl"
LICENSE_FEATURE_AUTOMATED_BACKUP = "automated_backup"
LICENSE_FEATURE_ADVANCED_DNS = "advanced_dns"
LICENSE_FEATURE_AI_OLLAMA = "ai_ollama"
LICENSE_FEATURE_GROUP_CORE = "Core"
LICENSE_FEATURE_GROUP_PRO_MODULE = "Pro Module"
LICENSE_FEATURE_STATUS_INCLUDED = "Included"
LICENSE_FEATURE_STATUS_PRO_LOCKED = "Pro Locked"
LICENSE_FEATURES = [
    {
        "code": LICENSE_FEATURE_SITE_LIMIT,
        "label": "5 Active Sites",
        "description": "Community surum 5 aktif siteye kadar ucretsiz kullanim saglar.",
        "group": LICENSE_FEATURE_GROUP_CORE,
        "required_plan": LICENSE_PLAN_COMMUNITY,
    },
    {
        "code": LICENSE_FEATURE_ADVANCED_SSL,
        "label": "Advanced SSL",
        "description": "Gelismis local SSL ve sertifika yonetimi Pro modulu olarak acilir.",
        "group": LICENSE_FEATURE_GROUP_PRO_MODULE,
        "required_plan": LICENSE_PLAN_PRO,
    },
    {
        "code": LICENSE_FEATURE_AUTOMATED_BACKUP,
        "label": "Automated Backup",
        "description": "Site ve config yedek otomasyonu Pro modulu olarak acilir.",
        "group": LICENSE_FEATURE_GROUP_PRO_MODULE,
        "required_plan": LICENSE_PLAN_PRO,
    },
    {
        "code": LICENSE_FEATURE_ADVANCED_DNS,
        "label": "Advanced DNS",
        "description": "Gelismis local DNS, domain alias ve host yonetimi Pro modulu olarak acilir.",
        "group": LICENSE_FEATURE_GROUP_PRO_MODULE,
        "required_plan": LICENSE_PLAN_PRO,
    },
    {
        "code": LICENSE_FEATURE_AI_OLLAMA,
        "label": "AI / Ollama",
        "description": "Local AI ve Ollama entegrasyon kapilari Pro modulu olarak acilir.",
        "group": LICENSE_FEATURE_GROUP_PRO_MODULE,
        "required_plan": LICENSE_PLAN_PRO,
    },
]

QUICK_APP_STATUS_PLANNED = "planned"
QUICK_APP_STATUS_CREATED = "created"
QUICK_APP_MESSAGE_DRY_RUN = "quick app dry run only"
QUICK_APP_MESSAGE_CREATED = "quick app scaffold created"
QUICK_APP_ERROR_INVALID_PROJECT_CODE = "quick_app_invalid_project_code"
QUICK_APP_ERROR_TEMPLATE_NOT_FOUND = "quick_app_template_not_found"
QUICK_APP_ERROR_ALREADY_EXISTS = "quick_app_project_already_exists"
QUICK_APP_ERROR_ACTIVE_RUNTIME_NOT_FOUND = "quick_app_active_runtime_not_found"
QUICK_APP_ERROR_PATH_BLOCKED = "quick_app_path_blocked"
QUICK_APP_ERROR_COMMUNITY_SITE_LIMIT = "quick_app_community_site_limit"
QUICK_APP_TEMPLATE_PHP_EMPTY = "php-empty"
QUICK_APP_TEMPLATE_LARAVEL = "laravel"
QUICK_APP_TEMPLATE_WORDPRESS = "wordpress"
QUICK_APP_TEMPLATE_OPENCART3 = "opencart-3"
QUICK_APP_TEMPLATE_NODE_VITE = "node-vite"

FOLDER_LAYOUT_STATUS_PLANNED = "planned"
FOLDER_LAYOUT_STATUS_APPLIED = "applied"
FOLDER_LAYOUT_MESSAGE_READY = "folder layout ready"
FOLDER_LAYOUT_MESSAGE_PLAN_READY = "folder layout plan ready"
FOLDER_LAYOUT_MESSAGE_DRY_RUN = "folder layout dry run only"
FOLDER_LAYOUT_MESSAGE_APPLIED = "folder layout standard directories ensured"


VIRTUAL_HOST_STATUS_PLANNED = "planned"
VIRTUAL_HOST_STATUS_GENERATED = "generated"
VIRTUAL_HOST_DEFAULT_PORT = 80
VIRTUAL_HOST_DEFAULT_SERVER_SUFFIX = "localhost"
VIRTUAL_HOST_MESSAGE_DRY_RUN = "virtual host dry run only"
VIRTUAL_HOST_MESSAGE_GENERATED = "virtual host config generated"
VIRTUAL_HOST_ERROR_PROJECT_NOT_FOUND = "virtual_host_project_not_found"
VIRTUAL_HOST_ERROR_INVALID_DOMAIN = "virtual_host_invalid_domain"
VIRTUAL_HOST_ERROR_PATH_BLOCKED = "virtual_host_path_blocked"


NGINX_PUBLISH_STATUS_PLANNED = "planned"
NGINX_PUBLISH_STATUS_PUBLISHED = "published"
NGINX_PUBLISH_STATUS_REJECTED = "rejected"
NGINX_PUBLISH_MESSAGE_DRY_RUN = "nginx publish dry run only"
NGINX_PUBLISH_MESSAGE_PUBLISHED = "nginx config published"
NGINX_PUBLISH_MESSAGE_REJECTED = "nginx publish plan is not safe"
NGINX_PUBLISH_ERROR_VHOST_NOT_FOUND = "nginx_publish_virtual_host_not_found"
NGINX_PUBLISH_ERROR_SOURCE_NOT_FOUND = "nginx_publish_source_not_found"
NGINX_PUBLISH_ERROR_PATH_BLOCKED = "nginx_publish_path_blocked"
NGINX_PUBLISH_HASH_ALGORITHM = "sha256"


NGINX_VALIDATE_STATUS_PLANNED = "planned"
NGINX_VALIDATE_STATUS_VALID = "valid"
NGINX_VALIDATE_STATUS_INVALID = "invalid"
NGINX_VALIDATE_STATUS_REJECTED = "rejected"
NGINX_VALIDATE_MESSAGE_DRY_RUN = "nginx validate dry run only"
NGINX_VALIDATE_MESSAGE_VALID = "nginx config validation passed"
NGINX_VALIDATE_MESSAGE_INVALID = "nginx config validation failed"
NGINX_VALIDATE_MESSAGE_REJECTED = "nginx validate plan is not safe"
NGINX_VALIDATE_ERROR_PUBLISH_NOT_FOUND = "nginx_validate_publish_not_found"
NGINX_VALIDATE_ERROR_TARGET_NOT_FOUND = "nginx_validate_target_not_found"
NGINX_VALIDATE_ERROR_PATH_BLOCKED = "nginx_validate_path_blocked"
NGINX_VALIDATE_REQUIRED_DIRECTIVES = ["server", "listen", "server_name", "root", "location"]


NGINX_RELOAD_STATUS_PLANNED = "planned"
NGINX_RELOAD_STATUS_RELOADED = "reloaded"
NGINX_RELOAD_STATUS_REJECTED = "rejected"
NGINX_RELOAD_MODE_SIMULATED = "simulated_safe_reload"
NGINX_RELOAD_MESSAGE_DRY_RUN = "nginx reload dry run only"
NGINX_RELOAD_MESSAGE_RELOADED = "nginx reload simulated"
NGINX_RELOAD_MESSAGE_REJECTED = "nginx reload plan is not safe"
NGINX_RELOAD_ERROR_VALIDATION_NOT_FOUND = "nginx_reload_validation_not_found"
NGINX_RELOAD_ERROR_VALIDATION_NOT_VALID = "nginx_reload_validation_not_valid"
NGINX_RELOAD_ERROR_TARGET_NOT_FOUND = "nginx_reload_target_not_found"
NGINX_RELOAD_ERROR_PATH_BLOCKED = "nginx_reload_path_blocked"
NGINX_RELOAD_COMMAND_LABEL = "nginx -s reload"


NGINX_EXECUTABLE_STATUS_PLANNED = "planned"
NGINX_EXECUTABLE_STATUS_DETECTED = "detected"
NGINX_EXECUTABLE_STATUS_NOT_FOUND = "not_found"
NGINX_EXECUTABLE_STATUS_REJECTED = "rejected"
NGINX_EXECUTABLE_MESSAGE_DRY_RUN = "nginx executable detection dry run only"
NGINX_EXECUTABLE_MESSAGE_DETECTED = "nginx executable detected"
NGINX_EXECUTABLE_MESSAGE_NOT_FOUND = "nginx executable not found"
NGINX_EXECUTABLE_MESSAGE_REJECTED = "nginx executable detection rejected"
NGINX_EXECUTABLE_ENV_PATH = "JHOSTER_NGINX_EXE"
NGINX_EXECUTABLE_FILE_NAME_WINDOWS = "nginx.exe"
NGINX_EXECUTABLE_VERSION_COMMAND_LABEL = "nginx -v"
NGINX_EXECUTABLE_VALIDATE_COMMAND_LABEL = "nginx -t"
NGINX_EXECUTABLE_MODE_SAFE_SCAN = "safe_path_scan"
NGINX_EXECUTABLE_SOURCE_ENV = "environment"
NGINX_EXECUTABLE_SOURCE_PROJECT = "project_snapshot"
NGINX_EXECUTABLE_SOURCE_STANDARD = "standard_windows_path"
NGINX_EXECUTABLE_STANDARD_WINDOWS_PATHS = [
    r"C:\nginx\nginx.exe",
    r"C:\tools\nginx\nginx.exe",
    r"C:\Program Files\nginx\nginx.exe",
]
NGINX_EXECUTABLE_ERROR_NOT_FOUND = "nginx_executable_not_found"
NGINX_EXECUTABLE_ERROR_PATH_BLOCKED = "nginx_executable_path_blocked"


NGINX_REAL_VALIDATE_STATUS_PLANNED = "planned"
NGINX_REAL_VALIDATE_STATUS_VALID = "valid"
NGINX_REAL_VALIDATE_STATUS_INVALID = "invalid"
NGINX_REAL_VALIDATE_STATUS_SKIPPED = "execution_skipped"
NGINX_REAL_VALIDATE_STATUS_REJECTED = "rejected"
NGINX_REAL_VALIDATE_MESSAGE_DRY_RUN = "nginx real validate dry run only"
NGINX_REAL_VALIDATE_MESSAGE_VALID = "nginx real validation passed"
NGINX_REAL_VALIDATE_MESSAGE_INVALID = "nginx real validation failed"
NGINX_REAL_VALIDATE_MESSAGE_SKIPPED = "nginx real execution skipped"
NGINX_REAL_VALIDATE_MESSAGE_REJECTED = "nginx real validate plan is not safe"
NGINX_REAL_VALIDATE_MODE_REAL_ADAPTER = "real_nginx_t_adapter"
NGINX_REAL_VALIDATE_ENV_MAIN_CONFIG = "JHOSTER_NGINX_MAIN_CONF"
NGINX_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME = "nginx.conf"
NGINX_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS = 15
NGINX_REAL_VALIDATE_ERROR_PUBLISH_NOT_FOUND = "nginx_real_validate_publish_not_found"
NGINX_REAL_VALIDATE_ERROR_EXECUTABLE_NOT_FOUND = "nginx_real_validate_executable_not_found"
NGINX_REAL_VALIDATE_ERROR_TARGET_NOT_FOUND = "nginx_real_validate_target_not_found"
NGINX_REAL_VALIDATE_ERROR_MAIN_CONFIG_NOT_FOUND = "nginx_real_validate_main_config_not_found"
NGINX_REAL_VALIDATE_ERROR_PATH_BLOCKED = "nginx_real_validate_path_blocked"


NGINX_REAL_RELOAD_STATUS_PLANNED = "planned"
NGINX_REAL_RELOAD_STATUS_RELOADED = "reloaded"
NGINX_REAL_RELOAD_STATUS_SKIPPED = "execution_skipped"
NGINX_REAL_RELOAD_STATUS_REJECTED = "rejected"
NGINX_REAL_RELOAD_MESSAGE_DRY_RUN = "nginx real reload dry run only"
NGINX_REAL_RELOAD_MESSAGE_RELOADED = "nginx real reload completed"
NGINX_REAL_RELOAD_MESSAGE_SKIPPED = "nginx real reload execution skipped"
NGINX_REAL_RELOAD_MESSAGE_REJECTED = "nginx real reload plan is not safe"
NGINX_REAL_RELOAD_MODE_REAL_ADAPTER = "real_nginx_reload_adapter"
NGINX_REAL_RELOAD_COMMAND_LABEL = "nginx -s reload -c <main nginx.conf>"
NGINX_REAL_RELOAD_ENV_MAIN_CONFIG = "JHOSTER_NGINX_MAIN_CONF"
NGINX_REAL_RELOAD_MAIN_CONFIG_FILE_NAME = "nginx.conf"
NGINX_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS = 15
NGINX_REAL_RELOAD_ERROR_PUBLISH_NOT_FOUND = "nginx_real_reload_publish_not_found"
NGINX_REAL_RELOAD_ERROR_VALIDATION_NOT_FOUND = "nginx_real_reload_validation_not_found"
NGINX_REAL_RELOAD_ERROR_VALIDATION_NOT_VALID = "nginx_real_reload_validation_not_valid"
NGINX_REAL_RELOAD_ERROR_EXECUTABLE_NOT_FOUND = "nginx_real_reload_executable_not_found"
NGINX_REAL_RELOAD_ERROR_TARGET_NOT_FOUND = "nginx_real_reload_target_not_found"
NGINX_REAL_RELOAD_ERROR_PATH_BLOCKED = "nginx_real_reload_path_blocked"

NGINX_EXECUTION_PREFLIGHT_STATUS_PLANNED = "planned"
NGINX_EXECUTION_PREFLIGHT_STATUS_READY = "ready"
NGINX_EXECUTION_PREFLIGHT_STATUS_BLOCKED = "blocked"
NGINX_EXECUTION_PREFLIGHT_MESSAGE_DRY_RUN = "nginx execution preflight dry run only"
NGINX_EXECUTION_PREFLIGHT_MESSAGE_READY = "nginx real execution preflight passed"
NGINX_EXECUTION_PREFLIGHT_MESSAGE_BLOCKED = "nginx real execution preflight blocked"
NGINX_EXECUTION_PREFLIGHT_MODE = "real_execution_preflight"
NGINX_EXECUTION_PREFLIGHT_ENV_MAIN_CONFIG = "JHOSTER_NGINX_MAIN_CONF"
NGINX_EXECUTION_PREFLIGHT_MAIN_CONFIG_FILE_NAME = "nginx.conf"
NGINX_EXECUTION_PREFLIGHT_ERROR_PUBLISH_NOT_FOUND = "nginx_execution_preflight_publish_not_found"
NGINX_EXECUTION_PREFLIGHT_ERROR_EXECUTABLE_NOT_FOUND = "nginx_execution_preflight_executable_not_found"
NGINX_EXECUTION_PREFLIGHT_ERROR_TARGET_NOT_FOUND = "nginx_execution_preflight_target_not_found"
NGINX_EXECUTION_PREFLIGHT_ERROR_PATH_BLOCKED = "nginx_execution_preflight_path_blocked"
NGINX_EXECUTION_PREFLIGHT_REQUIRED_DIRECTIVES = ["events", "http", "include"]
NGINX_EXECUTION_PREFLIGHT_BLOCKED_INCLUDE_TOKENS = ["..", "|", "&", "$", "%", "`"]


HOSTS_PUBLISH_STATUS_PLANNED = "planned"
HOSTS_PUBLISH_STATUS_PUBLISHED = "published"
HOSTS_PUBLISH_STATUS_REJECTED = "rejected"
HOSTS_PUBLISH_MESSAGE_DRY_RUN = "hosts publish dry run only"
HOSTS_PUBLISH_MESSAGE_PUBLISHED = "hosts entry published"
HOSTS_PUBLISH_MESSAGE_REJECTED = "hosts publish plan is not safe"
HOSTS_PUBLISH_ERROR_VHOST_NOT_FOUND = "hosts_publish_virtual_host_not_found"
HOSTS_PUBLISH_ERROR_PATH_BLOCKED = "hosts_publish_path_blocked"
HOSTS_PUBLISH_DEFAULT_IP = "127.0.0.1"
HOSTS_PUBLISH_LINE_MARKER_PREFIX = "# jhoster:"


HOSTS_APPLY_STATUS_PLANNED = "planned"
HOSTS_APPLY_STATUS_APPLIED = "applied"
HOSTS_APPLY_STATUS_ROLLBACK_PLANNED = "rollback_planned"
HOSTS_APPLY_STATUS_ROLLED_BACK = "rolled_back"
HOSTS_APPLY_STATUS_REJECTED = "rejected"
HOSTS_APPLY_MESSAGE_DRY_RUN = "hosts apply dry run only"
HOSTS_APPLY_MESSAGE_APPLIED = "hosts entry applied"
HOSTS_APPLY_MESSAGE_ROLLBACK_DRY_RUN = "hosts rollback dry run only"
HOSTS_APPLY_MESSAGE_ROLLED_BACK = "hosts entry rollback completed"
HOSTS_APPLY_MESSAGE_REJECTED = "hosts apply plan is not safe"
HOSTS_APPLY_ERROR_VHOST_NOT_FOUND = "hosts_apply_virtual_host_not_found"
HOSTS_APPLY_ERROR_RECORD_NOT_FOUND = "hosts_apply_record_not_found"
HOSTS_APPLY_ERROR_BACKUP_NOT_FOUND = "hosts_apply_backup_not_found"
HOSTS_APPLY_ERROR_ADMIN_REQUIRED = "hosts_apply_admin_required"
HOSTS_APPLY_ERROR_PATH_BLOCKED = "hosts_apply_path_blocked"
HOSTS_APPLY_MODE_SNAPSHOT = "snapshot_apply"
HOSTS_APPLY_MODE_REAL_WINDOWS = "real_windows_hosts_apply"
HOSTS_WINDOWS_SYSTEM_FILE = r"C:\Windows\System32\drivers\etc\hosts"


HOSTS_AUTO_STATUS_PLANNED = "planned"
HOSTS_AUTO_STATUS_SYNCED = "synced"
HOSTS_AUTO_STATUS_REJECTED = "rejected"
HOSTS_AUTO_STATUS_INSPECTED = "inspected"
HOSTS_AUTO_STATUS_REPAIR_NOT_REQUIRED = "repair_not_required"
HOSTS_AUTO_MESSAGE_DRY_RUN = "hosts auto sync dry run only"
HOSTS_AUTO_MESSAGE_SYNCED = "hosts auto sync completed"
HOSTS_AUTO_MESSAGE_REJECTED = "hosts auto sync plan is not safe"
HOSTS_AUTO_MESSAGE_INSPECTED = "hosts auto inspect completed"
HOSTS_AUTO_MESSAGE_REPAIR_NOT_REQUIRED = "hosts auto repair is not required"
HOSTS_AUTO_DEFAULT_IP = "127.0.0.1"
HOSTS_AUTO_MODE_SNAPSHOT = "snapshot_hosts_auto"
HOSTS_AUTO_MODE_REAL_WINDOWS = "real_windows_hosts_auto"
HOSTS_AUTO_BLOCK_BEGIN = "# BEGIN JHOSTER AUTO HOSTS"
HOSTS_AUTO_BLOCK_END = "# END JHOSTER AUTO HOSTS"
HOSTS_AUTO_COMMENT_PREFIX = "#jhoster:auto:"


WEB_SERVER_CODE_NGINX = "nginx"
WEB_SERVER_CODE_APACHE = "apache"
WEB_SERVER_PROFILE_STATUS_READY = "ready"
WEB_SERVER_PROFILE_STATUS_PLANNED = "planned"
WEB_SERVER_PROFILE_STATUS_SELECTED = "selected"
WEB_SERVER_PROFILE_STATUS_REJECTED = "rejected"
WEB_SERVER_PROFILE_MESSAGE_DRY_RUN = "web server profile dry run only"
WEB_SERVER_PROFILE_MESSAGE_SELECTED = "web server profile selected"
WEB_SERVER_PROFILE_MESSAGE_REJECTED = "web server profile selection rejected"
WEB_SERVER_PROFILE_ERROR_NOT_FOUND = "web_server_profile_not_found"
WEB_SERVER_PROFILE_ERROR_UNSUPPORTED = "web_server_profile_unsupported"
WEB_SERVER_PROFILE_ERROR_NOT_READY = "web_server_profile_not_ready"
WEB_SERVER_PROFILE_DEFAULT = WEB_SERVER_CODE_APACHE
WEB_SERVER_PROFILE_SUPPORTED_CODES = [WEB_SERVER_CODE_NGINX, WEB_SERVER_CODE_APACHE]
WEB_SERVER_PROFILE_APACHE_STAGE = "apache_adapter_ready"
WEB_SERVER_PROFILE_NGINX_STAGE = "nginx_adapter_ready"

WEB_SERVER_WORKFLOW_STATUS_PLANNED = "planned"
WEB_SERVER_WORKFLOW_STATUS_COMPLETED = "completed"
WEB_SERVER_WORKFLOW_STATUS_FAILED = "failed"
WEB_SERVER_WORKFLOW_STATUS_SKIPPED = "skipped"
WEB_SERVER_WORKFLOW_STATUS_ROLLED_BACK = "rolled_back"
WEB_SERVER_WORKFLOW_LOCK_STATUS_ACTIVE = "active"
WEB_SERVER_WORKFLOW_LOCK_STATUS_RELEASED = "released"
WEB_SERVER_WORKFLOW_MESSAGE_DRY_RUN = "web server workflow dry run only"
WEB_SERVER_WORKFLOW_MESSAGE_COMPLETED = "web server workflow completed"
WEB_SERVER_WORKFLOW_MESSAGE_FAILED = "web server workflow failed"
WEB_SERVER_WORKFLOW_MESSAGE_RELOAD_SKIPPED = "web server workflow reload skipped"
WEB_SERVER_WORKFLOW_MESSAGE_LOCK_ACQUIRED = "web server workflow lock acquired"
WEB_SERVER_WORKFLOW_MESSAGE_LOCK_RELEASED = "web server workflow lock released"
WEB_SERVER_WORKFLOW_MESSAGE_LOCKED = "web server workflow is already locked"
WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_DRY_RUN = "web server workflow rollback dry run only"
WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_COMPLETED = "web server workflow rollback completed"
WEB_SERVER_WORKFLOW_MESSAGE_ROLLBACK_SKIPPED = "web server workflow rollback skipped"
WEB_SERVER_WORKFLOW_ERROR_UNSUPPORTED_PROFILE = "web_server_workflow_unsupported_profile"
WEB_SERVER_WORKFLOW_ERROR_PROJECT_NOT_FOUND = "web_server_workflow_project_not_found"
WEB_SERVER_WORKFLOW_ERROR_NOT_FOUND = "web_server_workflow_not_found"
WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_SOURCE_NOT_FOUND = "web_server_workflow_rollback_source_not_found"
WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_TARGET_NOT_FOUND = "web_server_workflow_rollback_target_not_found"
WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_PATH_BLOCKED = "web_server_workflow_rollback_path_blocked"
WEB_SERVER_WORKFLOW_ERROR_ROLLBACK_STEP_NOT_FOUND = "web_server_workflow_rollback_step_not_found"
WEB_SERVER_WORKFLOW_ERROR_RUN_NOT_FOUND = "web_server_workflow_run_not_found"
WEB_SERVER_WORKFLOW_ERROR_LOCKED = "web_server_workflow_locked"
WEB_SERVER_WORKFLOW_ERROR_LOCK_NOT_FOUND = "web_server_workflow_lock_not_found"
WEB_SERVER_WORKFLOW_ERROR_LOCK_RUN_MISMATCH = "web_server_workflow_lock_run_mismatch"
WEB_SERVER_WORKFLOW_RUN_ID_PREFIX = "wsw"
WEB_SERVER_WORKFLOW_REASON_APACHE_REAL_EXECUTION_REQUIRED = "apache reload needs allow_real_execution=true"
WEB_SERVER_WORKFLOW_STEP_PROFILE = "profile"
WEB_SERVER_WORKFLOW_STEP_LOCK = "lock"
WEB_SERVER_WORKFLOW_STEP_GENERATE = "generate"
WEB_SERVER_WORKFLOW_STEP_PUBLISH = "publish"
WEB_SERVER_WORKFLOW_STEP_VALIDATE = "validate"
WEB_SERVER_WORKFLOW_STEP_REAL_VALIDATE = "real_validate"
WEB_SERVER_WORKFLOW_STEP_RELOAD = "reload"
WEB_SERVER_WORKFLOW_STEP_ROLLBACK = "rollback"
WEB_SERVER_WORKFLOW_STEP_DEFERRED_MESSAGE = "step requires workflow execution"
WEB_SERVER_WORKFLOW_SOURCE = "web_server_workflow_service"
APACHE_VHOST_STATUS_PLANNED = "planned"
APACHE_VHOST_STATUS_GENERATED = "generated"
APACHE_VHOST_MESSAGE_DRY_RUN = "apache virtual host dry run only"
APACHE_VHOST_MESSAGE_GENERATED = "apache virtual host config generated"
APACHE_VHOST_ERROR_PROJECT_NOT_FOUND = "apache_vhost_project_not_found"
APACHE_VHOST_ERROR_INVALID_DOMAIN = "apache_vhost_invalid_domain"
APACHE_VHOST_ERROR_PATH_BLOCKED = "apache_vhost_path_blocked"
APACHE_VHOST_DEFAULT_PORT = 80
APACHE_VHOST_DEFAULT_SERVER_SUFFIX = "localhost"
APACHE_VHOST_REQUIRED_DIRECTIVES = ["VirtualHost", "ServerName", "DocumentRoot", "Directory", "Require all granted"]


APACHE_PUBLISH_STATUS_PLANNED = "planned"
APACHE_PUBLISH_STATUS_PUBLISHED = "published"
APACHE_PUBLISH_STATUS_REJECTED = "rejected"
APACHE_PUBLISH_MESSAGE_DRY_RUN = "apache publish dry run only"
APACHE_PUBLISH_MESSAGE_PUBLISHED = "apache config published"
APACHE_PUBLISH_MESSAGE_REJECTED = "apache publish plan is not safe"
APACHE_PUBLISH_ERROR_VHOST_NOT_FOUND = "apache_publish_virtual_host_not_found"
APACHE_PUBLISH_ERROR_SOURCE_NOT_FOUND = "apache_publish_source_not_found"
APACHE_PUBLISH_ERROR_PATH_BLOCKED = "apache_publish_path_blocked"
APACHE_PUBLISH_HASH_ALGORITHM = "sha256"

APACHE_VALIDATE_STATUS_PLANNED = "planned"
APACHE_VALIDATE_STATUS_VALID = "valid"
APACHE_VALIDATE_STATUS_INVALID = "invalid"
APACHE_VALIDATE_STATUS_REJECTED = "rejected"
APACHE_VALIDATE_MESSAGE_DRY_RUN = "apache validate dry run only"
APACHE_VALIDATE_MESSAGE_VALID = "apache config validation passed"
APACHE_VALIDATE_MESSAGE_INVALID = "apache config validation failed"
APACHE_VALIDATE_MESSAGE_REJECTED = "apache validate plan is not safe"
APACHE_VALIDATE_ERROR_PUBLISH_NOT_FOUND = "apache_validate_publish_not_found"
APACHE_VALIDATE_ERROR_TARGET_NOT_FOUND = "apache_validate_target_not_found"
APACHE_VALIDATE_ERROR_PATH_BLOCKED = "apache_validate_path_blocked"
APACHE_VALIDATE_REQUIRED_DIRECTIVES = ["VirtualHost", "ServerName", "DocumentRoot", "Directory", "Require all granted"]

APACHE_EXECUTABLE_STATUS_PLANNED = "planned"
APACHE_EXECUTABLE_STATUS_DETECTED = "detected"
APACHE_EXECUTABLE_STATUS_NOT_FOUND = "not_found"
APACHE_EXECUTABLE_STATUS_REJECTED = "rejected"
APACHE_EXECUTABLE_MESSAGE_DRY_RUN = "apache executable detection dry run only"
APACHE_EXECUTABLE_MESSAGE_DETECTED = "apache executable detected"
APACHE_EXECUTABLE_MESSAGE_NOT_FOUND = "apache executable not found"
APACHE_EXECUTABLE_MESSAGE_REJECTED = "apache executable detection rejected"
APACHE_EXECUTABLE_ENV_PATH = "JHOSTER_APACHE_EXE"
APACHE_EXECUTABLE_FILE_NAME_WINDOWS = "httpd.exe"
APACHE_EXECUTABLE_VERSION_COMMAND_LABEL = "httpd -v"
APACHE_EXECUTABLE_VALIDATE_COMMAND_LABEL = "httpd -t"
APACHE_EXECUTABLE_MODE_SAFE_SCAN = "safe_path_scan"
APACHE_EXECUTABLE_SOURCE_ENV = "environment"
APACHE_EXECUTABLE_SOURCE_PROJECT = "project_snapshot"
APACHE_EXECUTABLE_SOURCE_STANDARD = "standard_windows_path"
APACHE_MAIN_CONFIG_FILE_NAME = "httpd.conf"
APACHE_VHOST_EXTENSION = ".conf"
APACHE_VALIDATE_COMMAND_LABEL = "httpd -t -f <main httpd.conf>"
APACHE_RELOAD_COMMAND_LABEL = "httpd -k restart -f <main httpd.conf>"
APACHE_EXECUTABLE_STANDARD_WINDOWS_PATHS = [
    r"C:\Apache24\bin\httpd.exe",
    r"C:\tools\apache\bin\httpd.exe",
    r"C:\Program Files\Apache Group\Apache2\bin\httpd.exe",
]
APACHE_EXECUTABLE_ERROR_NOT_FOUND = "apache_executable_not_found"
APACHE_EXECUTABLE_ERROR_PATH_BLOCKED = "apache_executable_path_blocked"

APACHE_REAL_VALIDATE_STATUS_PLANNED = "planned"
APACHE_REAL_VALIDATE_STATUS_VALID = "valid"
APACHE_REAL_VALIDATE_STATUS_INVALID = "invalid"
APACHE_REAL_VALIDATE_STATUS_REJECTED = "rejected"
APACHE_REAL_VALIDATE_STATUS_SKIPPED = "execution_skipped"
APACHE_REAL_VALIDATE_MESSAGE_DRY_RUN = "apache real validate dry run only"
APACHE_REAL_VALIDATE_MESSAGE_VALID = "apache real config validation passed"
APACHE_REAL_VALIDATE_MESSAGE_INVALID = "apache real config validation failed"
APACHE_REAL_VALIDATE_MESSAGE_REJECTED = "apache real validate plan is not safe"
APACHE_REAL_VALIDATE_MESSAGE_SKIPPED = "apache real execution skipped"
APACHE_REAL_VALIDATE_ERROR_PUBLISH_NOT_FOUND = "apache_real_validate_publish_not_found"
APACHE_REAL_VALIDATE_ERROR_EXECUTABLE_NOT_FOUND = "apache_real_validate_executable_not_found"
APACHE_REAL_VALIDATE_ERROR_TARGET_NOT_FOUND = "apache_real_validate_target_not_found"
APACHE_REAL_VALIDATE_ERROR_PATH_BLOCKED = "apache_real_validate_path_blocked"
APACHE_REAL_VALIDATE_ENV_MAIN_CONFIG = "JHOSTER_APACHE_MAIN_CONFIG"
APACHE_REAL_VALIDATE_MAIN_CONFIG_FILE_NAME = "httpd.conf"
APACHE_REAL_VALIDATE_MODE_REAL_ADAPTER = "real_httpd_t_adapter"
APACHE_REAL_VALIDATE_COMMAND_TIMEOUT_SECONDS = 8

APACHE_REAL_RELOAD_STATUS_PLANNED = "planned"
APACHE_REAL_RELOAD_STATUS_RELOADED = "reloaded"
APACHE_REAL_RELOAD_STATUS_SKIPPED = "execution_skipped"
APACHE_REAL_RELOAD_STATUS_REJECTED = "rejected"
APACHE_REAL_RELOAD_MESSAGE_DRY_RUN = "apache real reload dry run only"
APACHE_REAL_RELOAD_MESSAGE_RELOADED = "apache real reload completed"
APACHE_REAL_RELOAD_MESSAGE_SKIPPED = "apache real reload execution skipped"
APACHE_REAL_RELOAD_MESSAGE_REJECTED = "apache real reload plan is not safe"
APACHE_REAL_RELOAD_MODE_REAL_ADAPTER = "real_httpd_restart_adapter"
APACHE_REAL_RELOAD_COMMAND_LABEL = "httpd -k restart -f <main httpd.conf>"
APACHE_REAL_RELOAD_ENV_MAIN_CONFIG = "JHOSTER_APACHE_MAIN_CONFIG"
APACHE_REAL_RELOAD_MAIN_CONFIG_FILE_NAME = "httpd.conf"
APACHE_REAL_RELOAD_COMMAND_TIMEOUT_SECONDS = 15
APACHE_REAL_RELOAD_ERROR_PUBLISH_NOT_FOUND = "apache_real_reload_publish_not_found"
APACHE_REAL_RELOAD_ERROR_VALIDATION_NOT_FOUND = "apache_real_reload_validation_not_found"
APACHE_REAL_RELOAD_ERROR_VALIDATION_NOT_VALID = "apache_real_reload_validation_not_valid"
APACHE_REAL_RELOAD_ERROR_EXECUTABLE_NOT_FOUND = "apache_real_reload_executable_not_found"
APACHE_REAL_RELOAD_ERROR_TARGET_NOT_FOUND = "apache_real_reload_target_not_found"
APACHE_REAL_RELOAD_ERROR_PATH_BLOCKED = "apache_real_reload_path_blocked"




PACKAGE_DOWNLOAD_STATUS_AVAILABLE = "available"
PACKAGE_DOWNLOAD_STATUS_DOWNLOADED = "downloaded"
PACKAGE_DOWNLOAD_STATUS_INSTALLED = "installed"
PACKAGE_DOWNLOAD_STATUS_PLANNED = "planned"
PACKAGE_DOWNLOAD_MESSAGE_DRY_RUN = "package download dry run only"
PACKAGE_DOWNLOAD_MESSAGE_DOWNLOADED = "package downloaded"
PACKAGE_DOWNLOAD_MESSAGE_INSTALLED = "package installed"
PACKAGE_DOWNLOAD_ERROR_NOT_FOUND = "package_download_not_found"
PACKAGE_DOWNLOAD_ERROR_DISABLED = "package_download_disabled"
PACKAGE_DOWNLOAD_ERROR_URL_MISSING = "package_download_url_missing"
PACKAGE_DOWNLOAD_ERROR_EXTERNAL_DOWNLOADS_DISABLED = "external_downloads_disabled"
PACKAGE_DOWNLOAD_ERROR_CHECKSUM_MISMATCH = "package_download_checksum_mismatch"
PACKAGE_DOWNLOAD_ERROR_ARCHIVE_MISSING = "package_download_archive_missing"
DEFAULT_PACKAGE_DOWNLOAD_MAX_BYTES = 524288000
