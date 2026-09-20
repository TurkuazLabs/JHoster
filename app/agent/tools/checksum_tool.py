# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\checksum_tool.py
# 📌 Amac: Dosya checksum degerlerini hesaplar ve dogrular
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: SHA256 tabanli guvenli dosya butunluk kontrol tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
import hashlib

from config.constants import CHECKSUM_ALGORITHM_SHA256


class ChecksumTool:
    def calculate(self, file_path: Path, algorithm: str) -> str:
        normalized_algorithm = algorithm.strip().lower()

        if normalized_algorithm != CHECKSUM_ALGORITHM_SHA256:
            raise ValueError("unsupported_checksum_algorithm")

        digest = hashlib.sha256()

        with file_path.open("rb") as source_file:
            for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()

    def verify(self, file_path: Path, expected_checksum: str, algorithm: str) -> dict[str, str | bool]:
        calculated_checksum = self.calculate(file_path, algorithm)
        normalized_expected = expected_checksum.strip().lower()

        return {
            "valid": calculated_checksum == normalized_expected,
            "algorithm": algorithm.strip().lower(),
            "expected": normalized_expected,
            "actual": calculated_checksum,
        }
