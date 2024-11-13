import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    BASE_URL: str = os.getenv("BASE_URL", "https://fletappfastapi-yakvenalex.amvera.io")  # значение по умолчанию

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env")


# Получаем параметры для загрузки переменных среды
settings = Settings()
