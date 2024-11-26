from pydantic_settings import BaseSettings, SettingsConfigDict

__SETTINGS = None


class Settings(BaseSettings):
    APP_NAME: str = "My App"
    LOG_LEVEL: str = "INFO"
    ENABLE_METRICS: bool

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    MAX_REQUESTS: int = 500

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    global __SETTINGS

    if __SETTINGS is None:
        __SETTINGS = Settings()

    return __SETTINGS
