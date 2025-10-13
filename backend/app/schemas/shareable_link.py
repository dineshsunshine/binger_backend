"""
Shareable Link Schemas
Pydantic models for shareable link validation
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ShareableLinkCreate(BaseModel):
    """Schema for creating a shareable link"""
    pass  # No input needed, generated automatically


class ShareableLinkResponse(BaseModel):
    """Schema for shareable link response"""
    id: str
    user_id: str
    token: str
    shareable_url: str  # Full URL for sharing
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ShareableLinkDelete(BaseModel):
    """Schema for confirming deletion"""
    message: str
    success: bool

