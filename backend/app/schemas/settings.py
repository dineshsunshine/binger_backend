"""
Settings schemas.
"""
from typing import Any
from pydantic import BaseModel


class AppSettings(BaseModel):
    """
    Schema for user application settings.
    This accepts any structure from the frontend as the AppSettings type is defined there.
    """
    
    class Config:
        extra = "allow"  # Allow any fields from frontend AppSettings type

