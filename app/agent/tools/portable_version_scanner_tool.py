# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\portable_version_scanner_tool.py
# 📌 Amac: Portable bin klasorlerindeki versionlu runtime ve servis klasorlerini tespit eder
# 📌 Modul - FileType
# Version: 2.0.0
# Aciklama: Laragon benzeri bin/* altindaki versionlu klasorleri semantic siralama, alias ve executable profil bilgisiyle tarar
# Bagimli Oldugu Katman: Tool

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re


@dataclass(frozen=True)
class PortableFamilyDefinition:
    family: str
    display_name: str
    base_path: str
    folder_pattern: str
    executable_candidates: tuple[str, ...]
    runtime_adapter: str
    category: str
    aliases: tuple[str, ...] = ()
    process_name: str = ""
    working_dir: str = ""
    start_args: tuple[str, ...] = ()
    stop_args: tuple[str, ...] = ()
    status_args: tuple[str, ...] = ()


class PortableVersionScannerTool:
    VERSION_UNKNOWN = "unknown"
    SOURCE_KEY = "portable-bin-scan"
    PATH_SEPARATOR = "/"
    FAMILY_DEFINITIONS: tuple[PortableFamilyDefinition, ...] = (
        PortableFamilyDefinition(
            family="apache",
            display_name="Apache",
            base_path="bin/apache",
            folder_pattern=r"^(?:httpd|apache)-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("bin/httpd.exe", "Apache24/bin/httpd.exe", "httpd.exe", "apache.exe"),
            runtime_adapter="apache",
            category="web_server",
            aliases=("httpd",),
            process_name="httpd.exe",
            working_dir="",
            start_args=("-k", "start"),
            stop_args=("-k", "stop"),
            status_args=("-v",),
        ),
        PortableFamilyDefinition(
            family="nginx",
            display_name="Nginx",
            base_path="bin/nginx",
            folder_pattern=r"^nginx-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("nginx.exe",),
            runtime_adapter="nginx",
            category="web_server",
            process_name="nginx.exe",
            working_dir="",
            start_args=(),
            stop_args=("-s", "quit"),
            status_args=("-v",),
        ),
        PortableFamilyDefinition(
            family="php",
            display_name="PHP",
            base_path="bin/php",
            folder_pattern=r"^php-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("php-cgi.exe", "php.exe"),
            runtime_adapter="php",
            category="runtime",
            process_name="php-cgi.exe",
            working_dir="",
            start_args=("-b", "127.0.0.1:9000"),
            stop_args=(),
            status_args=("-v",),
        ),
        PortableFamilyDefinition(
            family="mysql",
            display_name="MySQL",
            base_path="bin/mysql",
            folder_pattern=r"^mysql-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("bin/mysqld.exe", "mysqld.exe"),
            runtime_adapter="mysql",
            category="database",
            aliases=("mysqld",),
            process_name="mysqld.exe",
            working_dir="",
            start_args=("--console",),
            stop_args=(),
            status_args=("--version",),
        ),
        PortableFamilyDefinition(
            family="mariadb",
            display_name="MariaDB",
            base_path="bin/mysql",
            folder_pattern=r"^mariadb-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("bin/mysqld.exe", "mysqld.exe"),
            runtime_adapter="mysql",
            category="database",
            aliases=("maria",),
            process_name="mysqld.exe",
            working_dir="",
            start_args=("--console",),
            stop_args=(),
            status_args=("--version",),
        ),
        PortableFamilyDefinition(
            family="node",
            display_name="Node.js",
            base_path="bin/nodejs",
            folder_pattern=r"^(?:nodejs?|node-v|v)(?:-)?(?P<version>[0-9]+(?:\.[0-9]+){0,2})",
            executable_candidates=("node.exe",),
            runtime_adapter="node",
            category="runtime",
            aliases=("nodejs",),
            process_name="node.exe",
            working_dir="",
            start_args=("--version",),
            stop_args=(),
            status_args=("--version",),
        ),
        PortableFamilyDefinition(
            family="python",
            display_name="Python",
            base_path="bin/python",
            folder_pattern=r"^python-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("python.exe",),
            runtime_adapter="python",
            category="runtime",
            aliases=("py",),
            process_name="python.exe",
            working_dir="",
            start_args=("--version",),
            stop_args=(),
            status_args=("--version",),
        ),
        PortableFamilyDefinition(
            family="memcached",
            display_name="Memcached",
            base_path="bin/memcached",
            folder_pattern=r"^memcached-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("memcached.exe",),
            runtime_adapter="memcached",
            category="cache",
            process_name="memcached.exe",
            working_dir="",
            start_args=("-p", "11211"),
            stop_args=(),
            status_args=("-h",),
        ),
        PortableFamilyDefinition(
            family="redis",
            display_name="Redis",
            base_path="bin/redis",
            folder_pattern=r"^redis-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("redis-server.exe", "bin/redis-server.exe"),
            runtime_adapter="redis",
            category="cache",
            process_name="redis-server.exe",
            working_dir="",
            start_args=("redis.windows.conf",),
            stop_args=(),
            status_args=("--version",),
        ),
        PortableFamilyDefinition(
            family="mailpit",
            display_name="Mailpit",
            base_path="bin/mailpit",
            folder_pattern=r"^mailpit-(?P<version>[0-9]+(?:\.[0-9]+){1,2})",
            executable_candidates=("mailpit.exe",),
            runtime_adapter="mailpit",
            category="mail",
            process_name="mailpit.exe",
            working_dir="",
            start_args=("--smtp", "127.0.0.1:1025", "--listen", "127.0.0.1:8025"),
            stop_args=(),
            status_args=("--version",),
        ),
    )

    def __init__(self, root_path: Path) -> None:
        self.root_path = root_path.resolve()

    def scan_all(self) -> dict[str, Any]:
        families = [self.scan_family(definition.family) for definition in self.FAMILY_DEFINITIONS]
        detected_count = sum(int(family.get("count", 0)) for family in families)

        return {
            "success": True,
            "source": self.SOURCE_KEY,
            "count": detected_count,
            "family_count": len(families),
            "families": families,
        }

    def scan_family(self, family: str) -> dict[str, Any]:
        definition = self.resolve_definition(family)
        if definition is None:
            return {
                "success": False,
                "source": self.SOURCE_KEY,
                "family": self.normalize_family(family),
                "error": "portable_family_not_found",
                "count": 0,
                "versions": [],
            }

        base_directory = self.root_path / definition.base_path
        versions = self._scan_definition(definition, base_directory)
        recommended = self._select_recommended_version(versions)

        return {
            "success": True,
            "source": self.SOURCE_KEY,
            "family": definition.family,
            "display_name": definition.display_name,
            "base_path": definition.base_path,
            "category": definition.category,
            "aliases": list(definition.aliases),
            "base_exists": base_directory.exists(),
            "count": len(versions),
            "recommended_folder_name": recommended.get("folder_name", "") if recommended else "",
            "recommended_version": recommended.get("version", "") if recommended else "",
            "versions": versions,
        }

    def list_family_definitions(self) -> dict[str, Any]:
        return {
            "success": True,
            "source": self.SOURCE_KEY,
            "count": len(self.FAMILY_DEFINITIONS),
            "families": [self._definition_payload(definition) for definition in self.FAMILY_DEFINITIONS],
        }

    def get_version_by_folder(self, family: str, folder_name: str) -> dict[str, Any] | None:
        definition = self.resolve_definition(family)
        if definition is None:
            return None

        normalized_folder_name = self._safe_folder_name(folder_name)
        if not normalized_folder_name:
            return None

        version_directory = self.root_path / definition.base_path / normalized_folder_name
        if not version_directory.exists() or not version_directory.is_dir():
            return None

        return self._build_version_payload(definition, version_directory)

    def get_latest_version(self, family: str) -> dict[str, Any] | None:
        scan_result = self.scan_family(family)
        versions = scan_result.get("versions", [])
        if not isinstance(versions, list) or not versions:
            return None

        for version in versions:
            if bool(version.get("executable_exists", False)):
                return version

        return versions[0]

    def resolve_definition(self, family: str) -> PortableFamilyDefinition | None:
        normalized_family = self.normalize_family(family)
        for definition in self.FAMILY_DEFINITIONS:
            aliases = {self.normalize_family(alias) for alias in definition.aliases}
            if definition.family == normalized_family or normalized_family in aliases:
                return definition
        return None

    def normalize_family(self, family: str) -> str:
        return str(family or "").strip().lower()

    def _scan_definition(self, definition: PortableFamilyDefinition, base_directory: Path) -> list[dict[str, Any]]:
        if not base_directory.exists() or not base_directory.is_dir():
            return []

        versions: list[dict[str, Any]] = []
        for version_directory in sorted(base_directory.iterdir(), key=lambda item: item.name.lower()):
            if not version_directory.is_dir():
                continue

            if not self._matches_definition(definition, version_directory.name):
                continue

            versions.append(self._build_version_payload(definition, version_directory))

        versions.sort(key=lambda item: item.get("version_sort_key", []), reverse=True)
        return versions

    def _build_version_payload(self, definition: PortableFamilyDefinition, version_directory: Path) -> dict[str, Any]:
        folder_name = version_directory.name
        version = self._extract_version(definition, folder_name)
        install_path = self._relative_path(version_directory)
        executable_result = self._resolve_executable(version_directory, definition.executable_candidates)
        metadata = self._extract_folder_metadata(folder_name)
        version_parts = self._version_parts(version)

        return {
            "family": definition.family,
            "display_name": definition.display_name,
            "code": self._build_component_code(definition.family, version, folder_name),
            "name": f"{definition.display_name} {version}",
            "version": version,
            "version_parts": version_parts,
            "version_sort_key": self._version_sort_key(version_parts),
            "folder_name": folder_name,
            "install_path": install_path,
            "category": definition.category,
            "runtime_adapter": definition.runtime_adapter,
            "source": self.SOURCE_KEY,
            "executable_exists": executable_result.get("exists"),
            "executable_path": executable_result.get("path"),
            "executable_candidates": [self._join_relative_path(install_path, candidate) for candidate in definition.executable_candidates],
            "process_profile": self._process_profile_payload(definition),
            "metadata": metadata,
            "display_label": self._build_display_label(definition.display_name, version, metadata),
        }

    def _resolve_executable(self, version_directory: Path, candidates: tuple[str, ...]) -> dict[str, Any]:
        first_candidate = ""
        for candidate in candidates:
            candidate_path = version_directory / candidate
            relative_candidate = self._relative_path(candidate_path)
            if not first_candidate:
                first_candidate = relative_candidate
            if candidate_path.exists() and candidate_path.is_file():
                return {"exists": True, "path": relative_candidate}

        return {"exists": False, "path": first_candidate}

    def _matches_definition(self, definition: PortableFamilyDefinition, folder_name: str) -> bool:
        return re.search(definition.folder_pattern, folder_name, flags=re.IGNORECASE) is not None

    def _extract_version(self, definition: PortableFamilyDefinition, folder_name: str) -> str:
        match = re.search(definition.folder_pattern, folder_name, flags=re.IGNORECASE)
        if match is None:
            return self.VERSION_UNKNOWN
        return str(match.group("version"))

    def _extract_folder_metadata(self, folder_name: str) -> dict[str, Any]:
        lower_value = folder_name.lower()
        architecture = self._first_match(lower_value, ("x64", "win64", "x86", "win32"))
        compiler_match = re.search(r"(?:vc|vs)[0-9]+", lower_value, flags=re.IGNORECASE)
        thread_safety = "nts" if "nts" in lower_value else "ts" if re.search(r"(?:^|-)ts(?:-|$)", lower_value) else ""
        platform = "windows" if "win" in lower_value else "portable"

        return {
            "platform": platform,
            "architecture": architecture,
            "compiler": compiler_match.group(0).upper() if compiler_match else "",
            "thread_safety": thread_safety.upper(),
            "raw_tokens": [token for token in re.split(r"[-_]+", folder_name) if token],
        }

    def _first_match(self, value: str, candidates: tuple[str, ...]) -> str:
        for candidate in candidates:
            if candidate in value:
                return candidate.upper()
        return ""

    def _version_parts(self, version: str) -> list[int]:
        if version == self.VERSION_UNKNOWN:
            return []
        return [int(part) for part in re.findall(r"[0-9]+", version)[:4]]

    def _version_sort_key(self, version_parts: list[int]) -> list[int]:
        padded = [*version_parts]
        while len(padded) < 4:
            padded.append(0)
        return padded[:4]

    def _build_component_code(self, family: str, version: str, folder_name: str) -> str:
        if version and version != self.VERSION_UNKNOWN:
            return f"{family}-{version}"
        return self._slugify(folder_name)

    def _build_display_label(self, display_name: str, version: str, metadata: dict[str, Any]) -> str:
        badges = [metadata.get("architecture", ""), metadata.get("compiler", ""), metadata.get("thread_safety", "")]
        suffix = " ".join([badge for badge in badges if badge])
        return f"{display_name} {version}" if not suffix else f"{display_name} {version} ({suffix})"

    def _process_profile_payload(self, definition: PortableFamilyDefinition) -> dict[str, Any]:
        return {
            "process_name": definition.process_name,
            "working_dir": definition.working_dir,
            "executable_candidates": list(definition.executable_candidates),
            "start_args": list(definition.start_args),
            "stop_args": list(definition.stop_args),
            "status_args": list(definition.status_args),
        }

    def _definition_payload(self, definition: PortableFamilyDefinition) -> dict[str, Any]:
        return {
            "family": definition.family,
            "display_name": definition.display_name,
            "base_path": definition.base_path,
            "category": definition.category,
            "aliases": list(definition.aliases),
            "folder_pattern": definition.folder_pattern,
            "process_profile": self._process_profile_payload(definition),
        }

    def _select_recommended_version(self, versions: list[dict[str, Any]]) -> dict[str, Any] | None:
        if not versions:
            return None
        for version in versions:
            if bool(version.get("executable_exists", False)):
                return version
        return versions[0]

    def _safe_folder_name(self, folder_name: str) -> str:
        normalized = str(folder_name or "").strip().replace("\\", self.PATH_SEPARATOR)
        if self.PATH_SEPARATOR in normalized or normalized in {"", ".", ".."}:
            return ""
        return normalized

    def _relative_path(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root_path).as_posix()
        except ValueError:
            return ""

    def _join_relative_path(self, install_path: str, candidate: str) -> str:
        return f"{install_path.rstrip(self.PATH_SEPARATOR)}{self.PATH_SEPARATOR}{candidate.replace('\\\\', self.PATH_SEPARATOR).replace('\\', self.PATH_SEPARATOR).lstrip(self.PATH_SEPARATOR)}"

    def _slugify(self, value: str) -> str:
        lowered = str(value or "").strip().lower()
        return re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
