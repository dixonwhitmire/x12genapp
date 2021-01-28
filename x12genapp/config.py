from functools import lru_cache

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    """
    X12 Gen App settings.
    Each setting field defines an environment variable, with a meaningful default.
    Settings are overridden using environment variables.
    Example: is_passthrough_enabled is set using IS_PASSTHROUGH_ENABLED
    """
    uvicorn_app: str = 'x12genapp.main:app'
    uvicorn_host: str = '0.0.0.0'
    uvicorn_port: int = 8000
    uvicorn_reload: bool = True

    api_version: str = 'v2'

    # passthrough bypasses the genapp customer lookup and returns a 271 response indicating coverage
    is_passthrough_enabled: bool = True

    # genapp url/endpoint settings
    genapp_base_url: str = 'http://localhost:9990/Genapp'
    genapp_customer_lookup: str = '/Customer/Inq'

    # record range for caching
    genapp_customer_min_id: int = 1
    genapp_customer_max_id: int = 5

    class Config:
        case_sensitive = False


@lru_cache()
def get_app_settings() -> AppSettings:
    """Returns the app settings instance"""
    return AppSettings()