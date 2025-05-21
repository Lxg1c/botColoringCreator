from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    BOT_TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int


# Создаем объект настроек
settings = Settings()