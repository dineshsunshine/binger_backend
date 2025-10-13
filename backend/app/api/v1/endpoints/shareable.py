"""
Shareable Link Endpoints
Manage shareable watchlist links
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import Optional
import secrets
import os

from ....core.database import get_db
from ....core.auth import get_current_user
from ....models.user import User
from ....models.shareable_link import ShareableLink
from ....models.watchlist import WatchlistItem
from ....schemas.shareable_link import ShareableLinkResponse, ShareableLinkDelete

router = APIRouter()


def get_base_url(request: Request) -> str:
    """Get the base URL from request"""
    # Use the request's base URL
    return str(request.base_url).rstrip('/')


@router.post("/shareable-link", response_model=ShareableLinkResponse)
async def create_or_get_shareable_link(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a shareable link for the current user's watchlist.
    If a link already exists (active or inactive), reactivate and return it.
    This ensures users always get the same URL even after deletion/recreation.
    """
    # Check if user already has a shareable link (active or inactive)
    existing_link = db.query(ShareableLink).filter(
        ShareableLink.user_id == current_user.id
    ).first()
    
    if existing_link:
        # Reactivate if it was deactivated
        if not existing_link.is_active:
            existing_link.is_active = True
            db.commit()
            db.refresh(existing_link)
        
        # Return existing link (same URL every time)
        base_url = get_base_url(request)
        existing_link.shareable_url = f"{base_url}/shared/watchlist/{existing_link.token}"
        return existing_link
    
    # Generate unique token (only for first-time creation)
    token = secrets.token_urlsafe(16)
    
    # Create new shareable link
    shareable_link = ShareableLink(
        user_id=current_user.id,
        token=token,
        is_active=True
    )
    
    db.add(shareable_link)
    db.commit()
    db.refresh(shareable_link)
    
    # Add shareable URL
    base_url = get_base_url(request)
    shareable_link.shareable_url = f"{base_url}/shared/watchlist/{token}"
    
    return shareable_link


@router.get("/shareable-link", response_model=Optional[ShareableLinkResponse])
async def get_shareable_link(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the current user's shareable link if it exists.
    """
    shareable_link = db.query(ShareableLink).filter(
        ShareableLink.user_id == current_user.id,
        ShareableLink.is_active == True
    ).first()
    
    if not shareable_link:
        return None
    
    # Add shareable URL
    base_url = get_base_url(request)
    shareable_link.shareable_url = f"{base_url}/shared/watchlist/{shareable_link.token}"
    
    return shareable_link


@router.delete("/shareable-link", response_model=ShareableLinkDelete)
async def delete_shareable_link(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Revoke the current user's shareable link.
    The link is deactivated but not deleted, so recreating it will return the same URL.
    """
    shareable_link = db.query(ShareableLink).filter(
        ShareableLink.user_id == current_user.id
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


# Note: The public watchlist viewing endpoint is now in main.py
# to make it accessible at /Binger/shared/watchlist/{token} (not under /api)

# Keeping this function here for reference but it's defined in main.py
def _view_shared_watchlist_implementation(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Public endpoint to view a shared watchlist.
    No authentication required.
    """
    # Find the shareable link
    shareable_link = db.query(ShareableLink).filter(
        ShareableLink.token == token,
        ShareableLink.is_active == True
    ).first()
    
    if not shareable_link:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Watchlist Not Found - Binger</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                }
                .container {
                    text-align: center;
                    padding: 40px;
                }
                h1 { font-size: 72px; margin-bottom: 20px; }
                p { font-size: 24px; opacity: 0.9; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬</h1>
                <h1>404</h1>
                <p>Watchlist not found or has been removed</p>
            </div>
        </body>
        </html>
        """, status_code=404)
    
    # Get user and watchlist
    user = shareable_link.user
    watchlist_items = db.query(WatchlistItem).filter(
        WatchlistItem.user_id == user.id
    ).order_by(WatchlistItem.added_at.desc()).all()
    
    # Generate HTML
    html_content = generate_public_watchlist_html(user, watchlist_items)
    
    return HTMLResponse(content=html_content)


def generate_public_watchlist_html(user: User, watchlist_items: list) -> str:
    """Generate beautiful HTML for public watchlist page"""
    
    # Import the sleek template
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../templates'))
    from watchlist_page import generate_sleek_watchlist_html
    
    # Convert watchlist items to JSON for JavaScript
    movies_json = "["
    for item in watchlist_items:
        movie_data = item.movie_data or {}
        
        # Extract data - handle both TMDb format and custom format
        title = movie_data.get('title', 'Untitled')
        
        # Handle poster/image
        poster = (movie_data.get('posterUrl', '') or 
                 movie_data.get('poster', '') or 
                 movie_data.get('poster_path', '') or 
                 movie_data.get('image', ''))
        if poster and not poster.startswith('http'):
            poster = f"https://image.tmdb.org/t/p/w500{poster}"
        
        # Handle description
        description = (movie_data.get('synopsis', '') or 
                      movie_data.get('description', '') or 
                      movie_data.get('overview', '') or 
                      'No description available')
        
        # Handle year/release date
        year = movie_data.get('year', '')
        if not year:
            release_date = movie_data.get('release_date', '')
            if release_date:
                year = release_date.split('-')[0] if '-' in release_date else release_date
        
        # Handle type (Film/TV Series)
        media_type = movie_data.get('type', '') or movie_data.get('media_type', '')
        if not media_type:
            media_type = 'Film' if movie_data.get('id', '').startswith('movie') else 'TV Series'
        
        # Handle genres
        genres = movie_data.get('genres', [])
        if isinstance(genres, list):
            genres_str = ', '.join(genres[:3])  # Max 3 genres
        else:
            genres_str = str(genres) if genres else ''
        
        # Handle languages
        languages = movie_data.get('languages', [])
        if isinstance(languages, list):
            lang_str = ', '.join(languages[:2])  # Max 2 languages
        else:
            lang_str = str(languages) if languages else ''
        
        # Handle rating
        rating = 0
        ratings_data = movie_data.get('ratings', {})
        if isinstance(ratings_data, dict):
            if 'imdb' in ratings_data:
                rating = ratings_data['imdb'].get('score', 0)
            elif 'tmdb' in ratings_data:
                rating = ratings_data['tmdb'].get('score', 0)
        if not rating:
            rating = movie_data.get('vote_average', 0) or movie_data.get('rating', 0)
        
        watched = movie_data.get('watched', False)
        added_at = item.added_at.isoformat() if hasattr(item, 'added_at') and item.added_at else ''
        
        movies_json += f"""{{
            "title": {repr(title)},
            "poster": {repr(poster)},
            "description": {repr(description)},
            "year": {repr(year)},
            "type": {repr(media_type)},
            "genres": {repr(genres_str)},
            "languages": {repr(lang_str)},
            "rating": {rating},
            "watched": {str(watched).lower()},
            "addedAt": {repr(added_at)}
        }},"""
    movies_json = movies_json.rstrip(',') + "]"
    
    user_name = user.name or "User"
    
    # Use the new sleek template
    return generate_sleek_watchlist_html(user_name, movies_json)

