# 📄 Dosya Yolu: E:\JHoster\app\agent\tools\http_download_tool.py
# 📌 Amac: HTTP/HTTPS paketlerini cache klasorune guvenli indirir
# 📌 Modul - Python
# Version: 1.0.0
# Aciklama: URL scheme, dosya boyutu ve atomic temp dosya kontrolleri yapan download adaptor tool katmani
# Bagimli Oldugu Katman: Tool

from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import shutil
import time


class HttpDownloadTool:
    def download(self, source_url: str, target_path: Path, max_bytes: int) -> dict[str, Any]:
        normalized_url = str(source_url or "").strip()
        self._validate_url(normalized_url)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = target_path.with_suffix(target_path.suffix + ".part")
        if temp_path.exists():
            temp_path.unlink()

        request = Request(normalized_url, headers={"User-Agent": "JHoster-Package-Downloader/1.0"})
        total_bytes = 0
        started_at = time.time()

        with urlopen(request, timeout=60) as response:
            with temp_path.open("wb") as output_file:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    total_bytes += len(chunk)
                    if total_bytes > max_bytes:
                        temp_path.unlink(missing_ok=True)
                        raise ValueError("download_size_limit_exceeded")
                    output_file.write(chunk)

        if target_path.exists():
            target_path.unlink()
        shutil.move(str(temp_path), str(target_path))

        return {
            "source_url": normalized_url,
            "target": str(target_path).replace("/", "\\"),
            "bytes": total_bytes,
            "duration_seconds": round(time.time() - started_at, 3),
        }

    def _validate_url(self, source_url: str) -> None:
        parsed_url = urlparse(source_url)
        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("unsupported_download_url_scheme")
        if not parsed_url.netloc:
            raise ValueError("download_url_host_missing")
