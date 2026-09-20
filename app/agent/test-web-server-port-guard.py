# 📄 Dosya Yolu: E:\JHoster\app\agent\test-web-server-port-guard.py
# 📌 Amac: Apache ve Nginx 80/443 port guard kuralini test eder
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Nginx calisirken Apache start isteginin ortak public port nedeniyle bloklandigini dogrular
# Bagimli Oldugu Katman: Tool

from tools.web_server_port_guard_tool import WebServerPortGuardTool


def test_apache_nginx_shared_public_ports_are_blocked() -> None:
    tool = WebServerPortGuardTool()
    result = tool.validate_start(
        "apache",
        {"code": "apache", "ports": {"http": 80, "https": 443}},
        [
            {"code": "apache", "ports": {"http": 80, "https": 443}},
            {"code": "nginx", "ports": {"http": 80, "https": 443}},
        ],
        [{"code": "nginx", "status": "running"}],
    )

    assert result["allowed"] is False
    assert result["running_service"] == "nginx"
    assert result["shared_ports"] == [80, 443]


def test_apache_nginx_distinct_public_ports_are_allowed() -> None:
    tool = WebServerPortGuardTool()
    result = tool.validate_start(
        "apache",
        {"code": "apache", "ports": {"http": 8080}},
        [
            {"code": "apache", "ports": {"http": 8080}},
            {"code": "nginx", "ports": {"http": 80, "https": 443}},
        ],
        [{"code": "nginx", "status": "running"}],
    )

    assert result["allowed"] is True
