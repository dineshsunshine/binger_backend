"""
Restaurant API endpoints for search and saved restaurants management.
"""
import secrets
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User
from ....models.restaurant import SavedRestaurant, RestaurantShareableLink
from ....schemas.restaurant import (
    RestaurantSearchRequest,
    RestaurantSearchResponse,
    SaveRestaurantRequest,
    UpdateSavedRestaurantRequest,
    SavedRestaurantResponse,
    RestaurantShareableLinkResponse,
    RestaurantShareableLinkDelete
)
from ....services.openai_service import OpenAIRestaurantService

logger = logging.getLogger(__name__)
router = APIRouter()


# Restaurant Search (OpenAI)
@router.post("/search", response_model=RestaurantSearchResponse)
async def search_restaurants(
    request: RestaurantSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search for restaurants using OpenAI with web search.
    Returns array of 0-5 matching restaurants.
    """
    try:
        service = OpenAIRestaurantService()
        restaurants = service.search_restaurants(request.query)
        
        return RestaurantSearchResponse(restaurants=restaurants)
    
    except Exception as e:
        logger.error(f"Restaurant search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


# Saved Restaurants Management
@router.post("/saved", response_model=SavedRestaurantResponse, status_code=201)
async def save_restaurant(
    request: SaveRestaurantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save a restaurant to user's list."""
    # Check if restaurant already saved
    existing = db.query(SavedRestaurant).filter(
        and_(
            SavedRestaurant.user_id == current_user.id,
            SavedRestaurant.restaurant_id == request.restaurant_data.id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant already saved")
    
    # Create new saved restaurant
    saved_restaurant = SavedRestaurant(
        user_id=current_user.id,
        restaurant_id=request.restaurant_data.id,
        restaurant_data=request.restaurant_data.model_dump(),
        visited=request.visited,
        personal_rating=request.personal_rating,
        notes=request.notes,
        tags=request.tags
    )
    
    db.add(saved_restaurant)
    db.commit()
    db.refresh(saved_restaurant)
    
    return saved_restaurant


@router.get("/saved", response_model=List[SavedRestaurantResponse])
async def get_saved_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: str = Query("date_added", regex="^(name|date_added|city|cuisine)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    visited: Optional[str] = Query(None, regex="^(true|false|all)$"),
    city: Optional[str] = None,
    cuisine: Optional[str] = None,
    country: Optional[str] = None
):
    """
    Get user's saved restaurants with filters and sorting.
    
    Query parameters:
    - sort_by: name, date_added, city, cuisine (default: date_added)
    - order: asc, desc (default: desc)
    - visited: true, false, all (default: all)
    - city: filter by city name
    - cuisine: filter by cuisine type
    - country: filter by country name
    """
    query = db.query(SavedRestaurant).filter(SavedRestaurant.user_id == current_user.id)
    
    # Apply filters
    if visited == "true":
        query = query.filter(SavedRestaurant.visited == True)
    elif visited == "false":
        query = query.filter(SavedRestaurant.visited == False)
    
    # Note: Filtering by JSON fields (city, cuisine, country) requires custom logic
    # For now, we'll fetch and filter in Python (for simplicity)
    results = query.all()
    
    # Filter by JSON fields
    if city:
        results = [r for r in results if r.restaurant_data.get('city', '').lower() == city.lower()]
    if cuisine:
        results = [r for r in results if cuisine.lower() in r.restaurant_data.get('cuisine', '').lower()]
    if country:
        results = [r for r in results if r.restaurant_data.get('country', '').lower() == country.lower()]
    
    # Sort
    if sort_by == "name":
        results.sort(key=lambda x: x.restaurant_data.get('restaurant_name', '').lower(), 
                    reverse=(order == "desc"))
    elif sort_by == "city":
        results.sort(key=lambda x: x.restaurant_data.get('city', '').lower(), 
                    reverse=(order == "desc"))
    elif sort_by == "cuisine":
        results.sort(key=lambda x: x.restaurant_data.get('cuisine', '').lower(), 
                    reverse=(order == "desc"))
    else:  # date_added
        results.sort(key=lambda x: x.added_at, reverse=(order == "desc"))
    
    return results


@router.get("/saved/{restaurant_id}", response_model=SavedRestaurantResponse)
async def get_saved_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single saved restaurant by ID."""
    saved_restaurant = db.query(SavedRestaurant).filter(
        and_(
            SavedRestaurant.id == restaurant_id,
            SavedRestaurant.user_id == current_user.id
        )
    ).first()
    
    if not saved_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    return saved_restaurant


@router.put("/saved/{restaurant_id}", response_model=SavedRestaurantResponse)
async def update_saved_restaurant(
    restaurant_id: str,
    request: UpdateSavedRestaurantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a saved restaurant (mark as visited, add notes, rating, tags)."""
    saved_restaurant = db.query(SavedRestaurant).filter(
        and_(
            SavedRestaurant.id == restaurant_id,
            SavedRestaurant.user_id == current_user.id
        )
    ).first()
    
    if not saved_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    # Update fields
    if request.visited is not None:
        saved_restaurant.visited = request.visited
    if request.personal_rating is not None:
        saved_restaurant.personal_rating = request.personal_rating
    if request.notes is not None:
        saved_restaurant.notes = request.notes
    if request.tags is not None:
        saved_restaurant.tags = request.tags
    
    db.commit()
    db.refresh(saved_restaurant)
    
    return saved_restaurant


@router.delete("/saved/{restaurant_id}", status_code=204)
async def delete_saved_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a restaurant from saved list."""
    saved_restaurant = db.query(SavedRestaurant).filter(
        and_(
            SavedRestaurant.id == restaurant_id,
            SavedRestaurant.user_id == current_user.id
        )
    ).first()
    
    if not saved_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(saved_restaurant)
    db.commit()
    
    return None


# Shareable Links
def get_base_url(request: Request) -> str:
    """Get base URL from request."""
    return f"{request.url.scheme}://{request.headers.get('host', request.client.host)}/Binger"


@router.post("/shareable-link", response_model=RestaurantShareableLinkResponse)
async def create_or_get_restaurant_shareable_link(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a shareable link for the current user's restaurant list.
    If a link already exists, reactivate and return it.
    """
    # Check if user already has a shareable link
    existing_link = db.query(RestaurantShareableLink).filter(
        RestaurantShareableLink.user_id == current_user.id
    ).first()
    
    if existing_link:
        # Reactivate if it was deactivated
        if not existing_link.is_active:
            existing_link.is_active = True
            db.commit()
            db.refresh(existing_link)
        
        # Return existing link
        base_url = get_base_url(request)
        existing_link.shareable_url = f"{base_url}/shared/restaurants/{existing_link.token}"
        return existing_link
    
    # Generate unique token
    token = secrets.token_urlsafe(16)
    
    # Create new shareable link
    shareable_link = RestaurantShareableLink(
        user_id=current_user.id,
        token=token,
        is_active=True
    )
    
    db.add(shareable_link)
    db.commit()
    db.refresh(shareable_link)
    
    # Add shareable URL
    base_url = get_base_url(request)
    shareable_link.shareable_url = f"{base_url}/shared/restaurants/{token}"
    
    return shareable_link


@router.get("/shareable-link", response_model=Optional[RestaurantShareableLinkResponse])
async def get_restaurant_shareable_link(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the current user's active shareable link."""
    shareable_link = db.query(RestaurantShareableLink).filter(
        RestaurantShareableLink.user_id == current_user.id,
        RestaurantShareableLink.is_active == True
    ).first()
    
    if not shareable_link:
        return None
    
    # Add shareable URL
    base_url = get_base_url(request)
    shareable_link.shareable_url = f"{base_url}/shared/restaurants/{shareable_link.token}"
    
    return shareable_link


@router.delete("/shareable-link", response_model=RestaurantShareableLinkDelete)
async def delete_restaurant_shareable_link(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Revoke the current user's shareable link."""
    shareable_link = db.query(RestaurantShareableLink).filter(
        RestaurantShareableLink.user_id == current_user.id
    ).first()
    
    if not shareable_link:
        raise HTTPException(status_code=404, detail="No shareable link found")
    
    # Deactivate the link instead of deleting it
    shareable_link.is_active = False
    db.commit()
    
    return {
        "message": "Shareable link revoked successfully. The same URL will be restored if you create a new link.",
        "success": True
    }

