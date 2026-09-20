# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-mode.py
# 📌 Amac: Apache/Nginx aktif web server mode secimi ve ortak www kuralini test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Gecici storage ile Apache seciliyken Nginx blok, Nginx seciliyken Apache blok ve mode switch davranisini dogrular
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil

from repositories.app_registry_repository import AppRegistryRepository
from repositories.process_state_repository import ProcessStateRepository
from repositories.web_server_profile_registry_repository import WebServerProfileRegistryRepository
from services.process_service import ProcessService
from services.web_server_profile_service import WebServerProfileService
from tools.process_guard_tool import ProcessGuardTool
from tools.safe_path_tool import SafePathTool
from tools.service_adapters.adapter_registry import ServiceAdapterRegistryTool
from tools.web_server_port_guard_tool import WebServerPortGuardTool
from tools.web_server_profile_tool import WebServerProfileTool


ROOT_PATH = Path(__file__).resolve().parents[2]
SOURCE_STORAGE_PATH = ROOT_PATH / "data" / "jhoster"


def copy_storage(target_path: Path) -> None:
    target_path.mkdir(parents=True, exist_ok=True)
    for file_name in ["app_registry.json", "process_state.json", "web_server_profile_registry.json"]:
        shutil.copy2(SOURCE_STORAGE_PATH / file_name, target_path / file_name)


def build_process_service(storage_path: Path) -> ProcessService:
    profile_repository = WebServerProfileRegistryRepository(storage_path)
    return ProcessService(
        app_registry_repository=AppRegistryRepository(storage_path, ROOT_PATH),
        process_state_repository=ProcessStateRepository(storage_path),
        process_guard_tool=ProcessGuardTool(SafePathTool(ROOT_PATH)),
        service_adapter_registry_tool=ServiceAdapterRegistryTool(),
        web_server_port_guard_tool=WebServerPortGuardTool(),
        web_server_profile_registry_repository=profile_repository,
    )


def build_profile_service(storage_path: Path) -> WebServerProfileService:
    return WebServerProfileService(
        web_server_profile_registry_repository=WebServerProfileRegistryRepository(storage_path),
        web_server_profile_tool=WebServerProfileTool(ROOT_PATH),
    )


def reset_profile(storage_path: Path, server_code: str) -> None:
    server_name = "Nginx" if server_code == "nginx" else "Apache HTTP Server"
    adapter_stage = "nginx_adapter_ready" if server_code == "nginx" else "apache_adapter_ready"
    payload = {
        "profile_records": [
            {
                "server_code": server_code,
                "server_name": server_name,
                "profile_status": "ready",
                "adapter_stage": adapter_stage,
                "default": server_code == "apache",
                "status": "selected",
                "selected_from": "test-web-server-mode",
                "selected_at": "2026-05-13T00:00:00+00:00",
                "shared_document_root": "www",
            }
        ]
    }
    with (storage_path / "web_server_profile_registry.json").open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def main() -> None:
    with TemporaryDirectory() as temp_dir:
        storage_path = Path(temp_dir)
        copy_storage(storage_path)
        reset_profile(storage_path, "apache")

        process_service = build_process_service(storage_path)
        profile_service = build_profile_service(storage_path)

        assert profile_service.get_current_profile()["current"]["server_code"] == "apache"
        assert process_service.start_process("nginx", dry_run=False)["success"] is False
        assert process_service.start_process("apache", dry_run=False)["success"] is True

        assert profile_service.select_profile("nginx", dry_run=False)["selection"]["server_code"] == "nginx"
        assert process_service.start_process("apache", dry_run=False)["success"] is False
        assert process_service.start_process("nginx", dry_run=False)["success"] is True

        assert profile_service.select_profile("apache", dry_run=False)["selection"]["server_code"] == "apache"
        assert process_service.start_process("apache", dry_run=False)["success"] is True
        assert process_service.process_state_repository.get_status("nginx") == "stopped"
        assert process_service.process_state_repository.get_status("apache") == "running"

    print("web server mode settings test passed")


if __name__ == "__main__":
    main()
