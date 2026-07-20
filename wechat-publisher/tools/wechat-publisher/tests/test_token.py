import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from wechat_publisher.config import Settings
from wechat_publisher.token import TokenManager
import wechat_publisher.token as token_module


class TokenManagerSecurityTests(unittest.TestCase):
    def test_save_uses_private_permissions_and_valid_json(self) -> None:
        settings = Settings(
            wechat_app_id="wx-test",
            wechat_app_secret="secret",
        )
        manager = TokenManager(settings)

        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "wechat-cache"
            cache_file = cache_dir / "token_cache.json"
            with (
                patch.object(token_module, "CACHE_DIR", cache_dir),
                patch.object(token_module, "CACHE_FILE", cache_file),
            ):
                manager.save("token", 7200)

            self.assertEqual(cache_dir.stat().st_mode & 0o777, 0o700)
            self.assertEqual(cache_file.stat().st_mode & 0o777, 0o600)
            self.assertEqual(
                json.loads(cache_file.read_text(encoding="utf-8"))["access_token"],
                "token",
            )


if __name__ == "__main__":
    unittest.main()
