"""
Pydantic schemas for request/response validation.
"""
from .auth import GoogleAuthRequest, TokenResponse
from .user import UserResponse
from .watchlist import MovieSchema, WatchlistResponse, WatchlistUpdateRequest
from .settings import AppSettings
from .shareable_link import ShareableLinkResponse, ShareableLinkDelete

__all__ = [
    "GoogleAuthRequest",
    "TokenResponse",
    "UserResponse",
    "MovieSchema",
    "WatchlistResponse",
    "WatchlistUpdateRequest",
    "AppSettings",
    "ShareableLinkResponse",
    "ShareableLinkDelete"
]

