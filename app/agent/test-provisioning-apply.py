# 📄 Dosya Yolu: E:\JHoster\app\agent\test-provisioning-apply.py
# 📌 Amac: v3.78.0 provisioning apply guard ve dry-run API akisini smoke test eder
# 📌 Modul - Python
# Version: 3.78.0
# Aciklama: Plan, dry-run, approval guard ve MySQL password guard davranislarini dogrular
# Bagimli Oldugu Katman: Service

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_apply_plan_without_mysql() -> None:
    response = client.get(
        "/api/v1/provisioning-apply/v378-plan/plan",
        params={
            "template_code": "php-empty",
            "project_name": "v378 Plan",
            "domain": "v378-plan.test",
            "port": 80,
            "web_server": "apache",
            "include_mysql": False,
            "include_php": True,
            "include_mailpit": False,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["status"] == "planned"
    assert payload["approved_required"] is True
    assert payload["quick_app_plan"]["success"] is True


def test_apply_post_defaults_to_dry_run() -> None:
    response = client.post(
        "/api/v1/provisioning-apply/v378-dry/apply",
        json={
            "project_name": "v378 Dry",
            "template_code": "php-empty",
            "domain": "v378-dry.test",
            "web_server": "nginx",
            "include_mysql": False,
            "include_php": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["status"] == "planned"


def test_real_apply_requires_approval() -> None:
    response = client.post(
        "/api/v1/provisioning-apply/v378-reject/apply",
        json={
            "project_name": "v378 Reject",
            "template_code": "php-empty",
            "domain": "v378-reject.test",
            "web_server": "apache",
            "include_mysql": False,
            "include_php": True,
            "dry_run": False,
            "approved": False,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["status"] == "rejected"
    assert payload["error"] == "provisioning_apply_approval_required"


def test_mysql_plan_reports_real_apply_blocker_when_execution_is_disabled() -> None:
    response = client.get(
        "/api/v1/provisioning-apply/v378-mysql-plan/plan",
        params={
            "template_code": "php-empty",
            "project_name": "v378 MySQL Plan",
            "domain": "v378-mysql-plan.test",
            "web_server": "apache",
            "include_mysql": True,
            "include_php": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "mysql_shell_execution_disabled" in payload["blockers"]
    assert payload["ready_for_apply"] is False


def test_mysql_real_apply_requires_password_before_mutation() -> None:
    response = client.post(
        "/api/v1/provisioning-apply/v378-mysql-guard/apply",
        json={
            "project_name": "v378 MySQL Guard",
            "template_code": "php-empty",
            "domain": "v378-mysql-guard.test",
            "web_server": "apache",
            "include_mysql": True,
            "include_php": True,
            "dry_run": False,
            "approved": True,
            "mysql_admin_password": "",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is False
    assert payload["status"] == "rejected"
    assert payload["error"] == "mysql_admin_password_required"


if __name__ == "__main__":
    test_apply_plan_without_mysql()
    test_apply_post_defaults_to_dry_run()
    test_real_apply_requires_approval()
    test_mysql_plan_reports_real_apply_blocker_when_execution_is_disabled()
    test_mysql_real_apply_requires_password_before_mutation()
    print("v3.78.0 provisioning apply smoke tests passed")
