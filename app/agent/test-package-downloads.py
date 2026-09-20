# 📄 Dosya Yolu: E:\JHoster\app\agent\test-package-downloads.py
# 📌 Amac: Package downloader katmanlarinin temel plan ve dry-run kontrollerini yapar
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: Registry, plan ve service dry-run davranisini dogrulayan test scripti
# Bagimli Oldugu Katman: Tool

from config.settings import AppSettings
from repositories.app_registry_repository import AppRegistryRepository
from repositories.execution_log_repository import ExecutionLogRepository
from repositories.package_download_repository import PackageDownloadRepository
from services.package_download_service import PackageDownloadService
from tools.archive_extract_tool import ArchiveExtractTool
from tools.checksum_tool import ChecksumTool
from tools.http_download_tool import HttpDownloadTool
from tools.package_download_installer_tool import PackageDownloadInstallerTool
from tools.safe_path_tool import SafePathTool


settings = AppSettings.load()
service = PackageDownloadService(
    package_download_repository=PackageDownloadRepository(settings.storage_path),
    package_download_installer_tool=PackageDownloadInstallerTool(
        safe_path_tool=SafePathTool(settings.root_path),
        http_download_tool=HttpDownloadTool(),
        checksum_tool=ChecksumTool(),
        archive_extract_tool=ArchiveExtractTool(),
    ),
    execution_log_repository=ExecutionLogRepository(settings.storage_path),
    app_registry_repository=AppRegistryRepository(settings.storage_path, settings.root_path),
    allow_external_downloads=settings.allow_external_downloads,
)

catalog = service.list_packages()
assert catalog["success"] is True
assert catalog["count"] >= 3
plan = service.get_plan("nginx-windows-stable")
assert plan["success"] is True
assert plan["download_plan"]["ready_to_download"] is True
result = service.download_package("nginx-windows-stable", dry_run=True)
assert result["success"] is True
print("package_download_tests_ok")
