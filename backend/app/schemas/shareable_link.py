"""
Shareable Link Schemas
Pydantic models for shareable link validation
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ShareableLinkCreate(BaseModel):
    """Schema for creating a shareable link"""
    entity_types: List[str] = Field(
        default=["movies", "restaurants"],
        description="What to show: 'movies', 'restaurants', or both"
    )


class ShareableLinkUpdate(BaseModel):
    """Schema for updating what entities to show"""
    entity_types: List[str] = Field(
        ...,
        description="What to show: 'movies', 'restaurants', or both"
    )


class ShareableLinkResponse(BaseModel):
    """Schema for shareable link response"""
    id: str
    user_id: str
    token: str
    entity_types: List[str]  # What entities to show
    shareable_url: Optional[str] = None  # Full URL for sharing (set by endpoint)
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ShareableLinkDelete(BaseModel):
    """Schema for confirming deletion"""
    message: str
    success: bool

