from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OVERPASS_TIMEOUT: int = 10  # Таймаут для Overpass API в секундах

    class Config:
        env_file = ".env"


settings = Settings()
