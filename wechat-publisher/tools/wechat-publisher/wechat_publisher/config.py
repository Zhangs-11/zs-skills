from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(Path.home() / ".wechat-publisher" / ".env"),
        env_file_encoding="utf-8",
    )

    wechat_app_id: str
    wechat_app_secret: str
    wechat_author: str = ""
    wechat_default_cover_media_id: str = ""
