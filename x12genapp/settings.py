from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    X12 Gen App settings.
    Each setting field defines an environment variable, with a meaningful default.
    Settings are overridden using environment variables.
    Example: is_passthrough_enabled is set using IS_PASSTHROUGH_ENABLED
    """
    # passthrough returns a 271 response where the member has insurance coverage
    # this bypasses the genapp customer lookup
    is_passthrough_enabled: bool = False

    # genapp url settings
    genapp_host: str = 'http://localhost:9990'
    genapp_base_url: str = '/Genapp'

    # genapp services/endpoints
    genapp_customer_lookup: str = '/Customer/Inq'

    #
    genapp_customer_min_id: int = 1
    genapp_customer_max_id: int = 5
