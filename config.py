from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Конфигурация Pydantic
    model_config = SettingsConfigDict(
        env_file="./.env",  # Указываем, что переменные окружения загружаются из .env файла
        env_file_encoding="utf-8",  # Указываем кодировку файла
        case_sensitive=False,  # Не учитывать регистр
    )

    BOT_TOKEN: str


# Создаем объект настроек
settings = Settings()
# print(settings.BOT_TOKEN)