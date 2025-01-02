from pydantic_settings import BaseSettings, SettingsConfigDict

__SETTINGS = None


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    ENABLE_LOGGING_EXCEPTION: bool = False

    # Prometheus
    ENABLE_METRICS: bool
    PROMETHEUS_MULTIPROC_DIR: str = "./prometheus"

    # Gunicorn
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    MAX_REQUESTS: int = 500
    GUNICORN_TIMEOUT: int = 5
    WORKERS: int = 2
    KEEPALIVE: int = 2

    # Requests
    REQUESTS_RETRY_MAX: int = 5
    REQUESTS_TIMEOUT: int = 20
    REQUESTS_ALLOW_REDIRECTS: bool = True
    REQUESTS_STREAM: bool = True
    REQUESTS_VERIFY: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_settings() -> Settings:
    global __SETTINGS

    if __SETTINGS is None:
        __SETTINGS = Settings()

    return __SETTINGS
