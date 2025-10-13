"""
Watchlist endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User
from ....models.watchlist import WatchlistItem
from ....schemas.watchlist import MovieSchema, WatchlistUpdateRequest

router = APIRouter()


@router.get("")
async def get_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all movies in user's watchlist.
    Returns array of Movie objects.
    """
    watchlist_items = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == current_user.id
    ).order_by(WatchlistItem.added_at.desc()).all()
    
    # Return just the movie_data (which is the Movie object)
    return [item.movie_data for item in watchlist_items]


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    movie: MovieSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add a movie to user's watchlist.
    Prevents duplicate movie IDs for the same user.
    """
    # Check if movie already exists in user's watchlist
    existing_item = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == current_user.id,
        WatchlistItem.movie_id == movie.id
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already in watchlist"
        )
    
    # Create new watchlist item
    watchlist_item = WatchlistItem(
        user_id=current_user.id,
        movie_id=movie.id,
        movie_data=movie.dict()
    )
    
    db.add(watchlist_item)
    db.commit()
    db.refresh(watchlist_item)
    
    return watchlist_item.movie_data


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_watchlist(
    movie_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove a movie from user's watchlist.
    """
    watchlist_item = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == current_user.id,
        WatchlistItem.movie_id == movie_id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found in watchlist"
        )
    
    db.delete(watchlist_item)
    db.commit()
    
    return None


@router.patch("/{movie_id}")
async def update_watchlist_item(
    movie_id: str,
    update_data: WatchlistUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a movie in user's watchlist.
    Primary use case: toggling watched status.
    """
    watchlist_item = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == current_user.id,
        WatchlistItem.movie_id == movie_id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found in watchlist"
        )
    
    # Update movie_data with new fields
    movie_data = watchlist_item.movie_data.copy()
    update_dict = update_data.dict(exclude_unset=True)
    movie_data.update(update_dict)
    
    watchlist_item.movie_data = movie_data
    db.commit()
    db.refresh(watchlist_item)
    
    return watchlist_item.movie_data

