from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    url: str = None


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", ".env.template"), case_sensitive=False,
                                      env_nested_delimiter="__", env_prefix="APP_CONFIG__")
    db: DatabaseConfig = DatabaseConfig()


settings: Settings = Settings()
