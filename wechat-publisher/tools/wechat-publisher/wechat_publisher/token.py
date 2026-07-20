import json
import os
import tempfile
import time
from pathlib import Path

from .config import Settings

CACHE_DIR = Path.home() / ".wechat-publisher"
CACHE_FILE = CACHE_DIR / "token_cache.json"
BUFFER = 300  # seconds: refresh 5 min early


class TokenManager:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_cached(self) -> str | None:
        if not CACHE_FILE.exists():
            return None
        try:
            data = json.loads(CACHE_FILE.read_text())
            if data.get("app_id") != self.settings.wechat_app_id:
                return None
            if time.time() + BUFFER < data.get("expires_at", 0):
                return data["access_token"]
        except (json.JSONDecodeError, KeyError, OSError):
            pass
        return None

    def save(self, token: str, expires_in: int) -> None:
        CACHE_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
        CACHE_DIR.chmod(0o700)
        payload = json.dumps(
            {
                "app_id": self.settings.wechat_app_id,
                "access_token": token,
                "expires_at": time.time() + expires_in,
            },
            indent=2,
        )
        temp_path: Path | None = None
        try:
            fd, raw_path = tempfile.mkstemp(
                dir=CACHE_DIR,
                prefix=".token_cache.",
                suffix=".tmp",
            )
            temp_path = Path(raw_path)
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            temp_path.replace(CACHE_FILE)
            CACHE_FILE.chmod(0o600)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)

    def invalidate(self) -> None:
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
