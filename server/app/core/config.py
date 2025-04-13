from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DGIS_API_KEY: str = "c2259912-6dc2-4517-bc47-670c9e8fd570"
    OVERPASS_TIMEOUT: int = 10  # Таймаут для Overpass API в секундах

    class Config:
        env_file = ".env"


settings = Settings()
