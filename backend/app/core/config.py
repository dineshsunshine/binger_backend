"""
Application configuration using environment variables.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Binger API"
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    
    # Database
    IS_PRODUCTION: bool = False
    DATABASE_URL: Optional[str] = None
    
    # Authentication
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int = 24  # 24 hours
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days
    
    # CORS
    CORS_ORIGINS: str = "*"  # Comma-separated origins or "*" for all
    
    # ngrok (local development)
    NGROK_AUTH_TOKEN: Optional[str] = None
    NGROK_DOMAIN: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        """Get database URL based on environment."""
        if self.IS_PRODUCTION and self.DATABASE_URL:
            return self.DATABASE_URL
        return "sqlite:///./database.db"


settings = Settings()

