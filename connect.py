from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    IP: Optional[str] = None
    API_KEY: Optional[str] = None
    LOCATION: Optional[str] = None

    class Config:
        env_file = ".env"
