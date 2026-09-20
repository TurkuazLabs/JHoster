# 📄 Dosya Yolu: E:/JHoster/app/agent/test-api-surface-audit.py
# 📌 Amac: Agent API route listesi, routes.txt ve DesktopApiConfig endpoint sabitlerini denetler
# 📌 Modul - Python
# Version: 3.76.0
# Aciklama: FastAPI route yuzeyini, desktop endpoint sabitlerini ve kritik smoke endpointlerini kontrol eder
# Bagimli Oldugu Katman: Tool

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from fastapi.testclient import TestClient

from main import app


AGENT_PATH = Path(__file__).resolve().parent
ROOT_PATH = AGENT_PATH.parents[1]
ROUTES_FILE_PATH = AGENT_PATH / "routes.txt"
DESKTOP_API_CONFIG_PATH = (
    ROOT_PATH
    / "app"
    / "desktop"
    / "src"
    / "main"
    / "java"
    / "com"
    / "jhoster"
    / "desktop"
    / "config"
    / "DesktopApiConfig.java"
)

SMOKE_CHECKS = [
    ("GET", "/"),
    ("GET", "/api/v1/health"),
    ("GET", "/api/v1/components"),
    ("GET", "/api/v1/apps"),
    ("GET", "/api/v1/cache"),
    ("GET", "/api/v1/local-packages"),
    ("GET", "/api/v1/package-downloads"),
    ("GET", "/api/v1/runtime-versions"),
    ("GET", "/api/v1/runtime-versions/active"),
    ("GET", "/api/v1/runtime-versions/portable-summary"),
    ("GET", "/api/v1/license"),
    ("GET", "/api/v1/projects"),
    ("GET", "/api/v1/quick-apps"),
    ("GET", "/api/v1/quick-apps/templates"),
    (
        "GET",
        "/api/v1/quick-apps/demo-quick-app/plan?web_server=apache&include_mysql=true&include_php=true&include_mailpit=false",
    ),
    (
        "POST",
        "/api/v1/quick-apps/demo-quick-app/create?dry_run=true&web_server=nginx&include_mysql=true&include_php=true&include_mailpit=true",
    ),
    ("GET", "/api/v1/virtual-hosts"),
    ("GET", "/api/v1/nginx-publish"),
    ("GET", "/api/v1/nginx-validate"),
    ("GET", "/api/v1/nginx-reload"),
    ("GET", "/api/v1/nginx-executable"),
    ("GET", "/api/v1/nginx-real-validate"),
    ("GET", "/api/v1/nginx-real-reload"),
    ("GET", "/api/v1/nginx-execution-preflight"),
    ("GET", "/api/v1/apache-vhosts"),
    ("GET", "/api/v1/apache-publish"),
    ("GET", "/api/v1/apache-validate"),
    ("GET", "/api/v1/apache-executable"),
    ("GET", "/api/v1/apache-real-validate"),
    ("GET", "/api/v1/apache-real-reload"),
    ("GET", "/api/v1/hosts-publish"),
    ("GET", "/api/v1/hosts-apply"),
    ("GET", "/api/v1/hosts-auto"),
    ("GET", "/api/v1/hosts-auto/inspect?real_write=false"),
    ("GET", "/api/v1/hosts-auto/repair-plan?real_write=false"),
    ("POST", "/api/v1/hosts-auto/repair?real_write=false&dry_run=true"),
    ("GET", "/api/v1/web-server-profiles"),
    ("GET", "/api/v1/web-server-profiles/current"),
    ("GET", "/api/v1/web-server-workflow"),
    ("GET", "/api/v1/web-server-workflow/runs"),
    ("GET", "/api/v1/web-server-workflow/locks"),
    ("GET", "/api/v1/service-adapters"),
    ("GET", "/api/v1/process"),
    ("GET", "/api/v1/folder-layout"),
    ("GET", "/api/v1/install/history"),
]


def get_actual_routes() -> list[str]:
    routes: list[str] = []
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if path is None or methods is None:
            continue
        for method in sorted(methods):
            if method == "HEAD":
                continue
            routes.append(f"{method} {path}")
    return sorted(routes)


def get_declared_routes() -> list[str]:
    declared: list[str] = []
    for line in ROUTES_FILE_PATH.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        if not cleaned.startswith(("GET ", "POST ", "PUT ", "DELETE ", "PATCH ")):
            continue
        declared.append(re.sub(r"\s+", " ", cleaned))
    return sorted(declared)


def normalize_dynamic_route(path: str) -> str:
    return re.sub(r"\{[^/]+\}", "[^/]+", re.escape(path).replace("\\{", "{").replace("\\}", "}"))


def path_matches_route(candidate_path: str, route_path: str) -> bool:
    pattern = "^" + re.sub(r"\{[^/]+\}", r"[^/]+", re.escape(route_path).replace("\\{", "{").replace("\\}", "}")) + "$"
    return re.match(pattern, candidate_path) is not None


def resolve_desktop_string_constants() -> dict[str, str]:
    content = DESKTOP_API_CONFIG_PATH.read_text(encoding="utf-8")
    constants: dict[str, str] = {}
    pattern = re.compile(r"public static final String\s+(\w+)\s*=\s*([^;]+);")
    for name, expression in pattern.findall(content):
        expression = expression.strip()
        if expression.startswith('"') and expression.endswith('"'):
            constants[name] = expression.strip('"')

    for name, expression in pattern.findall(content):
        expression = expression.strip()
        if name in constants:
            continue
        resolved = expression
        for const_name in sorted(constants, key=len, reverse=True):
            resolved = resolved.replace(const_name, repr(constants[const_name]))
        try:
            value = eval(resolved, {"__builtins__": {}}, {})
        except Exception:
            continue
        if isinstance(value, str):
            constants[name] = value
    return constants


def assert_routes_file_matches_app() -> None:
    actual = get_actual_routes()
    declared = get_declared_routes()
    missing = sorted(set(actual) - set(declared))
    extra = sorted(set(declared) - set(actual))
    duplicates = sorted(item for item in set(declared) if declared.count(item) > 1)

    assert not missing, f"routes.txt missing actual routes: {missing}"
    assert not extra, f"routes.txt has unknown routes: {extra}"
    assert not duplicates, f"routes.txt has duplicate routes: {duplicates}"


def assert_desktop_routes_match_app() -> None:
    constants = resolve_desktop_string_constants()
    route_constants = {
        name: value
        for name, value in constants.items()
        if name.endswith("_ROUTE") and value.startswith("/")
    }
    app_paths = [item.split(" ", 1)[1] for item in get_actual_routes()]

    missing: list[str] = []
    for name, value in route_constants.items():
        path = value.split("?", 1)[0]
        if not any(path_matches_route(path, app_path) for app_path in app_paths):
            missing.append(f"{name}={value}")

    assert not missing, f"DesktopApiConfig route constants not found in FastAPI app: {missing}"


def assert_smoke_checks() -> None:
    client = TestClient(app)
    failures: list[str] = []
    for method, route in SMOKE_CHECKS:
        response = client.get(route) if method == "GET" else client.post(route)
        if response.status_code >= 400:
            failures.append(f"{method} {route} -> {response.status_code}: {response.text[:160]}")
    assert not failures, "API smoke failures: " + " | ".join(failures)


def main() -> None:
    assert_routes_file_matches_app()
    assert_desktop_routes_match_app()
    assert_smoke_checks()
    print("api surface audit passed")


if __name__ == "__main__":
    main()
