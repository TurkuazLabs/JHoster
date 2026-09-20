# 📄 Dosya Yolu: E:\JHoster\app\agent\main.py
# 📌 Amac: JHoster agent FastAPI uygulamasini baslatilabilir hale getirir
# 📌 Modul - FileType
# Version: 3.76.0
# Aciklama: Root, health, component, process, runtime, quick app, package downloader, license feature registry, web server workflow ve folder layout, hosts auto route kayitlarini baglar
# Bagimli Oldugu Katman: Controller

from fastapi import FastAPI

from config.settings import AppSettings
from controllers.apps_controller import router as apps_router
from controllers.apache_vhost_controller import router as apache_vhost_router
from controllers.apache_publish_controller import router as apache_publish_router
from controllers.apache_validate_controller import router as apache_validate_router
from controllers.apache_executable_controller import router as apache_executable_router
from controllers.apache_real_validate_controller import router as apache_real_validate_router
from controllers.apache_real_reload_controller import router as apache_real_reload_router
from controllers.cache_controller import router as cache_router
from controllers.component_controller import router as component_router
from controllers.health_controller import router as health_router
from controllers.folder_layout_controller import router as folder_layout_router
from controllers.installation_controller import history_router as install_history_router
from controllers.installation_controller import router as installation_router
from controllers.license_controller import router as license_router
from controllers.local_package_controller import router as local_package_router
from controllers.package_download_controller import router as package_download_router
from controllers.nginx_publish_controller import router as nginx_publish_router
from controllers.nginx_validate_controller import router as nginx_validate_router
from controllers.nginx_reload_controller import router as nginx_reload_router
from controllers.nginx_executable_controller import router as nginx_executable_router
from controllers.nginx_real_validate_controller import router as nginx_real_validate_router
from controllers.nginx_real_reload_controller import router as nginx_real_reload_router
from controllers.nginx_execution_preflight_controller import router as nginx_execution_preflight_router
from controllers.hosts_publish_controller import router as hosts_publish_router
from controllers.hosts_apply_controller import router as hosts_apply_router
from controllers.hosts_auto_controller import router as hosts_auto_router
from controllers.web_server_profile_controller import router as web_server_profile_router
from controllers.web_server_workflow_controller import router as web_server_workflow_router
from controllers.process_controller import router as process_router
from controllers.project_controller import router as project_router
from controllers.quick_app_controller import router as quick_app_router
from controllers.root_controller import router as root_router
from controllers.runtime_version_controller import router as runtime_version_router
from controllers.service_adapter_controller import router as service_adapter_router
from controllers.virtual_host_controller import router as virtual_host_router


settings = AppSettings.load()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(root_router)
app.include_router(health_router)
app.include_router(folder_layout_router)
app.include_router(component_router)
app.include_router(cache_router)
app.include_router(apps_router)
app.include_router(local_package_router)
app.include_router(package_download_router)
app.include_router(runtime_version_router)
app.include_router(license_router)
app.include_router(project_router)
app.include_router(quick_app_router)
app.include_router(virtual_host_router)
app.include_router(nginx_publish_router)
app.include_router(nginx_validate_router)
app.include_router(nginx_reload_router)
app.include_router(nginx_executable_router)
app.include_router(nginx_real_validate_router)
app.include_router(nginx_real_reload_router)
app.include_router(nginx_execution_preflight_router)
app.include_router(hosts_publish_router)
app.include_router(hosts_apply_router)
app.include_router(hosts_auto_router)
app.include_router(web_server_profile_router)
app.include_router(web_server_workflow_router)
app.include_router(apache_vhost_router)
app.include_router(apache_publish_router)
app.include_router(apache_validate_router)
app.include_router(apache_executable_router)
app.include_router(apache_real_validate_router)
app.include_router(apache_real_reload_router)
app.include_router(service_adapter_router)
app.include_router(process_router)
app.include_router(installation_router)
app.include_router(install_history_router)
