"""
Watchlist schemas.
"""
from typing import Any
from pydantic import BaseModel


class MovieSchema(BaseModel):
    """
    Schema for Movie object.
    This accepts any structure from the frontend as the Movie type is defined there.
    """
    id: str
    title: str
    # Allow any additional fields from frontend Movie type
    
    class Config:
        extra = "allow"  # Allow additional fields


class WatchlistResponse(BaseModel):
    """Response schema for watchlist item."""
    id: str
    movie_id: str
    movie_data: dict
    added_at: str
    
    class Config:
        from_attributes = True


class WatchlistUpdateRequest(BaseModel):
    """Request schema for updating watchlist item."""
    watched: bool | None = None
    # Allow other movie fields to be updated
    
    class Config:
        extra = "allow"

