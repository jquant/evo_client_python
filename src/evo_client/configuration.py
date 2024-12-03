from typing import Optional
from pydantic import BaseModel

class Configuration(BaseModel):
    """
    Configuration for the API client
    """
    host: str = "https://evo-integracao-api.w12app.com.br"
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    api_key_prefix: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 60  # seconds 