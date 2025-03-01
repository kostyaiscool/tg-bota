from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: str = None


class TelegramConfig(BaseModel):
    token: str = None
    webhook_url: str = None
    webhook_path: str = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.template"), case_sensitive=False,
                                      env_nested_delimiter="__", env_prefix="APP_CONFIG__", extra='allow')
    db: DatabaseConfig = DatabaseConfig()
    tg: TelegramConfig = TelegramConfig()


settings: Settings = Settings()
