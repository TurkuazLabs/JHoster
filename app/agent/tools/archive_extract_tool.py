# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\archive_extract_tool.py
# 📌 Amac: ZIP arsivlerini path traversal riskine karsi guvenli sekilde acar
# 📌 Modul - FileType
# Version: 1.0.0
# Aciklama: Zip-slip, symlink ve boyut limit kontrolleri yapan archive extract tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from zipfile import ZipFile, ZipInfo, BadZipFile
import stat

from config.constants import ZIP_FILE_EXTENSION


class ArchiveExtractTool:
    def extract_zip(self, archive_path: Path, target_path: Path, max_bytes: int) -> dict[str, int | str]:
        if archive_path.suffix.lower() != ZIP_FILE_EXTENSION:
            raise ValueError("unsupported_archive_type")

        if not archive_path.exists() or not archive_path.is_file():
            raise FileNotFoundError("archive_file_not_found")

        target_path.mkdir(parents=True, exist_ok=True)
        resolved_target = target_path.resolve()

        try:
            with ZipFile(archive_path, "r") as archive_file:
                self._validate_members(archive_file.infolist(), resolved_target, max_bytes)
                archive_file.extractall(resolved_target)
                return {
                    "archive": str(archive_path).replace("/", "\\"),
                    "target": str(resolved_target).replace("/", "\\"),
                    "files": len([member for member in archive_file.infolist() if not member.is_dir()]),
                    "bytes": sum(member.file_size for member in archive_file.infolist()),
                }
        except BadZipFile as error:
            raise ValueError("invalid_zip_archive") from error

    def _validate_members(self, members: list[ZipInfo], target_path: Path, max_bytes: int) -> None:
        total_bytes = 0

        for member in members:
            self._validate_member(member, target_path)
            total_bytes += int(member.file_size)

            if total_bytes > max_bytes:
                raise ValueError("archive_size_limit_exceeded")

    def _validate_member(self, member: ZipInfo, target_path: Path) -> None:
        if member.filename.startswith(("/", "\\")):
            raise ValueError("absolute_archive_path_blocked")

        if ".." in Path(member.filename).parts:
            raise ValueError("archive_path_traversal_blocked")

        member_target = (target_path / member.filename).resolve()

        try:
            member_target.relative_to(target_path)
        except ValueError as error:
            raise ValueError("archive_member_outside_target") from error

        external_mode = member.external_attr >> 16
        if stat.S_ISLNK(external_mode):
            raise ValueError("archive_symlink_blocked")
