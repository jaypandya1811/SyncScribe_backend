import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    COOKIE_NAME: str
    COOKIE_SECURE: bool
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings() # type: ignore