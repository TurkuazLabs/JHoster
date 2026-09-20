# 📄 Dosya Yolu: E:\JHoster\app\desktop\test-source-header-path-guard.py
# 📌 Amac: Aktif Java ve Python kaynak dosyalarinin header yol bilgisini gercek dosya yolu ile karsilastirir
# 📌 Modul - Python
# Version: 3.76.1
# Aciklama: Desktop Java ve Agent Python kaynaklarinda tam E:\JHoster dosya yolu header standardinin bozulmasini engeller
# Bagimli Oldugu Katman: Tool

from __future__ import annotations

import re
from pathlib import Path


ROOT_PATH = Path(__file__).resolve().parents[2]
SOURCE_GROUPS = (
    (ROOT_PATH / "app" / "desktop" / "src", {".java"}),
    (ROOT_PATH / "app" / "agent", {".py"}),
)
HEADER_PATTERN = re.compile(r"Dosya Yolu:\s*([^\r\n]+)")
EXPECTED_ROOT = "E:/JHoster/"


def normalize_path(value: str) -> str:
    return value.strip().strip("*/# ").replace("\\", "/")


def expected_header_path(file_path: Path) -> str:
    relative_path = file_path.relative_to(ROOT_PATH).as_posix()
    return EXPECTED_ROOT + relative_path


def audit_source_headers() -> list[str]:
    failures: list[str] = []

    for source_root, extensions in SOURCE_GROUPS:
        for file_path in sorted(source_root.rglob("*")):
            if not file_path.is_file() or file_path.suffix.lower() not in extensions:
                continue

            content = file_path.read_text(encoding="utf-8-sig")
            header_match = HEADER_PATTERN.search("\n".join(content.splitlines()[:10]))
            if header_match is None:
                failures.append(f"missing header: {file_path.relative_to(ROOT_PATH).as_posix()}")
                continue

            actual_header = normalize_path(header_match.group(1))
            expected_header = expected_header_path(file_path)
            if actual_header.lower() != expected_header.lower():
                failures.append(
                    "path mismatch: "
                    f"{file_path.relative_to(ROOT_PATH).as_posix()} -> "
                    f"{actual_header} != {expected_header}"
                )

    return failures


def main() -> None:
    failures = audit_source_headers()
    if failures:
        raise AssertionError("source header path audit failed:\n" + "\n".join(failures))
    print("source header path audit passed")


if __name__ == "__main__":
    main()
