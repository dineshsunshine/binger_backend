"""
Restaurant API endpoints for search and saved restaurants management.
"""
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User
from ....models.restaurant import SavedRestaurant
from ....schemas.restaurant import (
    RestaurantSearchRequest,
    RestaurantSearchResponse,
    SaveRestaurantRequest,
    UpdateSavedRestaurantRequest,
    SavedRestaurantResponse
)
from ....services.openai_service import OpenAIRestaurantService
from ....services.gemini_service import GeminiRestaurantService
from ....services.google_image_service import GoogleImageService

logger = logging.getLogger(__name__)
router = APIRouter()


# Restaurant Search (Multi-Mode: OpenAI, Foursquare, or Hybrid)
@router.post("/search", response_model=RestaurantSearchResponse)
async def search_restaurants(
    request: RestaurantSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search for restaurants using OpenAI, Google Gemini, or both (hybrid).
    
    Search Modes:
    - mode=1: OpenAI only (intelligent search, may have placeholder images)
    - mode=2: Google Gemini Flash 2.5 with internet search (real-time data with photos)
    - mode=3: Hybrid (combines both OpenAI and Gemini results - RECOMMENDED)
    
    Returns array of 0-5 matching restaurants in the specified location.
    """
    try:
        restaurants = []
        
        # Mode 1: OpenAI only
        if request.mode == 1:
            logger.info(f"Using OpenAI search for: {request.query} in {request.location}")
            openai_service = OpenAIRestaurantService()
            restaurants = openai_service.search_restaurants(request.query, request.location)
        
        # Mode 2: Google Gemini only
        elif request.mode == 2:
            logger.info(f"Using Gemini search for: {request.query} in {request.location}")
            gemini_service = GeminiRestaurantService()
            restaurants = gemini_service.search_restaurants(request.query, request.location)
        
        # Mode 3: Hybrid (OpenAI + Gemini)
        elif request.mode == 3:
            logger.info(f"Using Hybrid search for: {request.query} in {request.location}")
            
            # Get results from both services
            openai_service = OpenAIRestaurantService()
            gemini_service = GeminiRestaurantService()
            
            openai_restaurants = []
            gemini_restaurants = []
            
            try:
                openai_restaurants = openai_service.search_restaurants(request.query, request.location)
            except Exception as e:
                logger.warning(f"OpenAI search failed in hybrid mode: {str(e)}")
            
            try:
                gemini_restaurants = gemini_service.search_restaurants(request.query, request.location)
            except Exception as e:
                logger.warning(f"Gemini search failed in hybrid mode: {str(e)}")
            
            # Merge results: Prioritize Gemini for real-time data with photos, supplement with OpenAI
            restaurants = _merge_restaurant_results(openai_restaurants, gemini_restaurants)
        
        # Fetch real images using Google Custom Search API for all results
        if restaurants:
            logger.info("Fetching real images using Google Custom Search API")
            image_service = GoogleImageService()
            restaurants = image_service.fetch_images_for_restaurants(restaurants)
        
        return RestaurantSearchResponse(restaurants=restaurants)
    
    except Exception as e:
        logger.error(f"Restaurant search failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


def _merge_restaurant_results(openai_results: List[dict], gemini_results: List[dict]) -> List[dict]:
    """
    Merge OpenAI and Gemini results intelligently.
    Strategy: Use Gemini results (with real-time web data and photos) and supplement with OpenAI if needed.
    """
    merged = []
    
    # Start with Gemini results (they have real-time web data and photos)
    for gemini_restaurant in gemini_results:
        merged.append(gemini_restaurant)
    
    # Add OpenAI results that don't overlap (name/location similarity check)
    for ai_restaurant in openai_results:
        if not _is_duplicate_restaurant(ai_restaurant, merged):
            # If OpenAI result has real images, include it
            images = ai_restaurant.get("images", [])
            has_real_images = images and all(img for img in images if img and not img.endswith("placeholder.jpg"))
            
            if has_real_images or len(merged) < 3:  # Include if has images OR we need more results
                merged.append(ai_restaurant)
    
    # Limit to top 5 results
    return merged[:5]


def _is_duplicate_restaurant(restaurant: dict, existing_list: List[dict]) -> bool:
    """Check if a restaurant is already in the existing list (fuzzy match by name and city)."""
    name = restaurant.get("restaurant_name", "").lower()
    city = restaurant.get("city", "").lower()
    
    for existing in existing_list:
        existing_name = existing.get("restaurant_name", "").lower()
        existing_city = existing.get("city", "").lower()
        
        # Simple fuzzy match: check if names are very similar and same city
        if _similarity(name, existing_name) > 0.7 and city == existing_city:
            return True
    
    return False


def _similarity(s1: str, s2: str) -> float:
    """Calculate simple similarity ratio between two strings."""
    if not s1 or not s2:
        return 0.0
    
    # Simple word overlap ratio
    words1 = set(s1.split())
    words2 = set(s2.split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0


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


@router.get("/saved/ids", response_model=List[str])
async def get_saved_restaurant_ids(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of saved restaurant IDs for the current user.
    Useful for checking which restaurants are already saved.
    """
    saved_restaurants = db.query(SavedRestaurant.restaurant_id).filter(
        SavedRestaurant.user_id == current_user.id
    ).all()
    
    return [r.restaurant_id for r in saved_restaurants]


@router.get("/saved", response_model=List[SavedRestaurantResponse])
async def get_saved_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: str = Query("added_at", regex="^(name|added_at|city|cuisine)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    visited: Optional[str] = Query(None, regex="^(true|false|all)$"),
    city: Optional[str] = None,
    cuisine: Optional[str] = None,
    country: Optional[str] = None
):
    """
    Get user's saved restaurants with filters and sorting.
    
    Query parameters:
    - sort_by: name, added_at, city, cuisine (default: added_at)
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
    else:  # added_at
        results.sort(key=lambda x: x.added_at, reverse=(order == "desc"))
    
    return results


@router.get("/saved/{restaurant_id}", response_model=SavedRestaurantResponse)
async def get_saved_restaurant(
    restaurant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single saved restaurant by restaurant_id (e.g., 'bla_bla_jbr_dubai')."""
    saved_restaurant = db.query(SavedRestaurant).filter(
        and_(
            SavedRestaurant.restaurant_id == restaurant_id,
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
            SavedRestaurant.restaurant_id == restaurant_id,
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
            SavedRestaurant.restaurant_id == restaurant_id,
            SavedRestaurant.user_id == current_user.id
        )
    ).first()
    
    if not saved_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(saved_restaurant)
    db.commit()
    
    return None
