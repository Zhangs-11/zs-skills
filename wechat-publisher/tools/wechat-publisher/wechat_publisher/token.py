import json
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
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(
            json.dumps(
                {
                    "app_id": self.settings.wechat_app_id,
                    "access_token": token,
                    "expires_at": time.time() + expires_in,
                },
                indent=2,
            )
        )

    def invalidate(self) -> None:
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
