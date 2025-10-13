"""
Authentication schemas.
"""
from pydantic import BaseModel


class GoogleAuthRequest(BaseModel):
    """Request schema for Google OAuth authentication."""
    code: str


class TokenResponse(BaseModel):
    """Response schema for authentication token."""
    token: str
    user: dict

