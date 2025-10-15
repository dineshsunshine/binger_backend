"""
API v1 router that combines all endpoint routers.
"""
from fastapi import APIRouter
from .endpoints import auth, user, watchlist, settings, shareable, restaurants, admin

api_router = APIRouter()

# Auth endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User endpoints
api_router.include_router(user.router, prefix="", tags=["user"])

# Watchlist endpoints (movies)
api_router.include_router(watchlist.router, prefix="/watchlist", tags=["watchlist"])

# Restaurants endpoints
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])

# Settings endpoints
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])

# Shareable links endpoints
api_router.include_router(shareable.router, prefix="", tags=["shareable"])

# Admin endpoints (TEMPORARY - for migrations only)
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

