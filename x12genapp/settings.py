from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    X12 Gen App settings.
    Each setting field defines an environment variable, with a meaningful default.
    Settings are overriden using environment variables.
    Example: is_passthrough_enabled is set using IS_PASSTHROUGH_ENABLED
    """
    # passthrough returns a 271 response where the member has insurance coverage
    is_passthrough_enabled: bool = False

    # genapp url settings
    genapp_host: str = 'http://localhost:9990'
    genapp_base_url: str = '/Genapp'

    # genapp services/endpoints
    genapp_customer_lookup: str = '/Customer/Inq'
