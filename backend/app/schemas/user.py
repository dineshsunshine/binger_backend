"""
User schemas.
"""
from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response schema for user information."""
    id: str
    name: str
    email: str
    picture: str | None
    
    class Config:
        from_attributes = True

