# 📄 Dosya Yolu: E:\JHoster\app\agent\test-stack-provisioning.py
# 📌 Amac: v3.77.0 New Site provisioning plan entegrasyonunu smoke test eder
# 📌 Modul - Python
# Version: 3.77.0
# Aciklama: Quick App plan cevabinda runtime installer, web workflow ve database wizard planlarini dogrular
# Bagimli Oldugu Katman: Service

from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_apache_mysql_php_provisioning_plan() -> None:
    response = client.get(
        "/api/v1/quick-apps/v377-apache/plan",
        params={
            "template_code": "php-empty",
            "project_name": "v377 Apache",
            "domain": "v377-apache.test",
            "port": 80,
            "web_server": "apache",
            "include_mysql": True,
            "include_php": True,
            "include_mailpit": False,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["provisioning_plan"]["web_server"] == "apache"
    assert payload["provisioning_plan"]["database_wizard"]["enabled"] is True
    assert payload["provisioning_plan"]["database_wizard"]["database_name"] == "v377_apache"
    assert payload["provisioning_plan"]["runtime_installer"]["status"] == "active"
    assert payload["provisioning_plan"]["service_installers"]["mysql"]["package_code"] == "mysql-windows-x64"
    assert payload["database_label"] == "MySQL: v377_apache"


def test_nginx_without_mysql_provisioning_plan() -> None:
    response = client.get(
        "/api/v1/quick-apps/v377-nginx/plan",
        params={
            "template_code": "php-empty",
            "project_name": "v377 Nginx",
            "domain": "v377-nginx.test",
            "port": 80,
            "web_server": "nginx",
            "include_mysql": False,
            "include_php": True,
            "include_mailpit": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    plan = payload["provisioning_plan"]
    assert plan["web_server"] == "nginx"
    assert plan["web_server_profile"]["safe"] is True
    assert plan["database_wizard"]["enabled"] is False
    assert plan["service_installers"]["mailpit"]["package_code"] == "mailpit-windows-amd64"
    assert plan["web_server_workflow"]["server_code"] == "nginx"


if __name__ == "__main__":
    test_apache_mysql_php_provisioning_plan()
    test_nginx_without_mysql_provisioning_plan()
    print("v3.77.0 stack provisioning smoke tests passed")
