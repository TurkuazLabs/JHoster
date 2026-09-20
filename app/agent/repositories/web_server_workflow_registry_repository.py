# 📄 Dosya Yolu: E:\JHoster\app\agent\repositories\web_server_workflow_registry_repository.py
# 📌 Amac: JHoster unified web server workflow kayitlarini JSON dosyasinda saklar
# 📌 Modul - FileType
# Version: 1.1.0
# Aciklama: Workflow gecmisi, proje bazli kayitlar ve run_id bazli kayit sorgulama islemlerini yapar
# Bagimli Oldugu Katman: Repo

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from config.constants import WEB_SERVER_WORKFLOW_REGISTRY_FILE_NAME


class WebServerWorkflowRegistryRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self.registry_file_path = storage_path / WEB_SERVER_WORKFLOW_REGISTRY_FILE_NAME

    def list_records(self) -> list[dict[str, Any]]:
        registry_data = self._read_registry()
        workflow_records = registry_data.get("workflow_records", [])

        if not isinstance(workflow_records, list):
            return []

        return sorted(
            [item for item in workflow_records if isinstance(item, dict)],
            key=lambda item: str(item.get("finished_at", item.get("stored_at", ""))),
            reverse=True,
        )

    def list_project_records(self, project_code: str) -> list[dict[str, Any]]:
        normalized_code = str(project_code).strip().lower()

        return [
            workflow_record
            for workflow_record in self.list_records()
            if str(workflow_record.get("project_code", "")).strip().lower() == normalized_code
        ]

    def list_status_records(self, status: str) -> list[dict[str, Any]]:
        normalized_status = str(status).strip().lower()

        return [
            workflow_record
            for workflow_record in self.list_records()
            if str(workflow_record.get("status", "")).strip().lower() == normalized_status
        ]

    def get_latest_workflow(self, project_code: str) -> dict[str, Any] | None:
        project_records = self.list_project_records(project_code)

        if not project_records:
            return None

        return project_records[0]

    def get_workflow_by_run_id(self, run_id: str) -> dict[str, Any] | None:
        normalized_run_id = str(run_id).strip().lower()

        for workflow_record in self.list_records():
            if str(workflow_record.get("run_id", "")).strip().lower() == normalized_run_id:
                return workflow_record

        return None

    def append_record(self, workflow_data: dict[str, Any]) -> dict[str, Any]:
        registry_data = self._read_registry()
        workflow_records = registry_data.get("workflow_records", [])

        if not isinstance(workflow_records, list):
            workflow_records = []

        now_value = datetime.now(timezone.utc).isoformat()
        stored_item = {
            **workflow_data,
            "stored_at": now_value,
        }

        workflow_records.append(stored_item)
        registry_data["workflow_records"] = workflow_records
        self._write_registry(registry_data)

        return stored_item

    def _read_registry(self) -> dict[str, Any]:
        if not self.registry_file_path.exists():
            return {"workflow_records": []}

        with self.registry_file_path.open("r", encoding="utf-8") as registry_file:
            loaded_data = json.load(registry_file)

        if not isinstance(loaded_data, dict):
            return {"workflow_records": []}

        return loaded_data

    def _write_registry(self, registry_data: dict[str, Any]) -> None:
        self.storage_path.mkdir(parents=True, exist_ok=True)

        with self.registry_file_path.open("w", encoding="utf-8") as registry_file:
            json.dump(registry_data, registry_file, indent=2, ensure_ascii=False)
