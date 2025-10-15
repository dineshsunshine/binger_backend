"""
Pydantic schemas for restaurant data and API requests/responses.
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


# Restaurant Data Structures
class Hours(BaseModel):
    """Operating hours for a restaurant."""
    monday: Optional[str] = None
    tuesday: Optional[str] = None
    wednesday: Optional[str] = None
    thursday: Optional[str] = None
    friday: Optional[str] = None
    saturday: Optional[str] = None
    sunday: Optional[str] = None
    timezone: Optional[str] = None


class Drinks(BaseModel):
    """Drinks information."""
    serves_alcohol: bool = False
    special_drinks: List[str] = Field(default_factory=list)


class SocialMedia(BaseModel):
    """Social media handles and URLs."""
    instagram: Optional[str] = None
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    tiktok: Optional[str] = None
    tripadvisor: Optional[str] = None


class RestaurantData(BaseModel):
    """Complete restaurant information (matches OpenAI response structure)."""
    id: str
    restaurant_name: str
    description: Optional[str] = None
    google_maps_url: Optional[str] = None
    website: Optional[str] = None
    menu_url: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    phone_number: Optional[str] = None
    hours: Optional[Hours] = None
    cuisine: Optional[str] = None
    type: Optional[str] = None
    drinks: Optional[Drinks] = None
    diet_type: Optional[str] = None
    social_media: Optional[SocialMedia] = None
    known_for: List[str] = Field(default_factory=list)
    images: List[str] = Field(default_factory=list)


# Search Endpoints
class RestaurantSearchRequest(BaseModel):
    """Request for searching restaurants."""
    query: str = Field(..., min_length=1, max_length=200, 
                      description="Restaurant name or search query")
    location: str = Field(..., min_length=2, max_length=100,
                         description="City or location to search in (e.g., 'Dubai', 'New York', 'Tokyo')")
    mode: int = Field(default=3, ge=1, le=3,
                     description="Search mode: 1=OpenAI only, 2=Foursquare only, 3=Hybrid (both)")


class RestaurantSearchResponse(BaseModel):
    """Response containing array of restaurants."""
    restaurants: List[RestaurantData]


# Quick Search (Fast, Google Custom Search based)
class QuickSearchRequest(BaseModel):
    """Request for quick restaurant search (fast, lightweight)."""
    query: str = Field(..., min_length=1, max_length=200, 
                      description="Restaurant name or search query")
    location: str = Field(..., min_length=2, max_length=100,
                         description="City or location (e.g., 'Dubai', 'New York')")


class QuickSearchResult(BaseModel):
    """Lightweight restaurant search result from quick search."""
    id: str = Field(..., description="Unique identifier (generated from name + location)")
    name: str = Field(..., description="Restaurant name")
    snippet: str = Field(..., description="Brief description or snippet")
    url: Optional[str] = Field(None, description="Website or Google Maps URL")
    images: List[str] = Field(default_factory=list, description="Restaurant image URLs")
    location: str = Field(..., description="Location/city")


class QuickSearchResponse(BaseModel):
    """Response for quick search endpoint."""
    results: List[QuickSearchResult]
    total: int = Field(..., description="Total number of results")


# Saved Restaurants Endpoints
class SaveRestaurantRequest(BaseModel):
    """Request to save a restaurant to user's list."""
    restaurant_data: RestaurantData
    visited: bool = False
    personal_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    notes: Optional[str] = Field(None, max_length=1000)
    tags: List[str] = Field(default_factory=list, max_items=10)


class UpdateSavedRestaurantRequest(BaseModel):
    """Request to update a saved restaurant."""
    visited: Optional[bool] = None
    personal_rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)
    tags: Optional[List[str]] = Field(None, max_items=10)


class SavedRestaurantResponse(BaseModel):
    """Response for a saved restaurant."""
    id: str
    user_id: str
    restaurant_id: str
    restaurant_data: RestaurantData
    visited: bool
    personal_rating: Optional[int] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    added_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

