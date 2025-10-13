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
    
    # Convert watchlist items to JSON for JavaScript
    movies_json = "["
    for item in watchlist_items:
        movie_data = item.movie_data or {}
        title = movie_data.get('title', 'Untitled')
        poster = movie_data.get('poster_path', '')
        if poster and not poster.startswith('http'):
            poster = f"https://image.tmdb.org/t/p/w500{poster}"
        overview = movie_data.get('overview', 'No description available')
        release_date = movie_data.get('release_date', 'Unknown')
        rating = movie_data.get('vote_average', 0)
        watched = movie_data.get('watched', False)
        
        movies_json += f"""{{
            "title": {repr(title)},
            "poster": {repr(poster)},
            "overview": {repr(overview)},
            "release_date": {repr(release_date)},
            "rating": {rating},
            "watched": {str(watched).lower()}
        }},"""
    movies_json = movies_json.rstrip(',') + "]"
    
    user_name = user.name or "User"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{user_name}'s Watchlist - Binger</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;900&display=swap" rel="stylesheet">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: #0a0a0a;
                color: #ffffff;
                min-height: 100vh;
                overflow-x: hidden;
            }}
            
            /* Hero Section */
            .hero {{
                background: linear-gradient(180deg, rgba(10,10,10,0) 0%, rgba(10,10,10,1) 100%),
                            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 400"><rect fill="%23E50914" width="1200" height="400"/><text x="50%%" y="50%%" text-anchor="middle" dominant-baseline="middle" font-size="120" font-family="Arial Black" fill="rgba(0,0,0,0.1)">BINGER</text></svg>');
                background-size: cover;
                background-position: center;
                padding: 100px 40px 60px;
                text-align: center;
                position: relative;
            }}
            
            .hero::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(135deg, #E50914 0%, #831010 100%);
                opacity: 0.9;
                z-index: 0;
            }}
            
            .hero-content {{
                position: relative;
                z-index: 1;
            }}
            
            .hero h1 {{
                font-family: 'Bebas Neue', sans-serif;
                font-size: clamp(48px, 8vw, 96px);
                font-weight: 900;
                letter-spacing: 4px;
                margin-bottom: 16px;
                text-shadow: 4px 4px 8px rgba(0,0,0,0.5);
                text-transform: uppercase;
            }}
            
            .hero .subtitle {{
                font-size: clamp(18px, 3vw, 28px);
                font-weight: 300;
                opacity: 0.95;
                letter-spacing: 1px;
            }}
            
            /* Stats Bar */
            .stats {{
                display: flex;
                justify-content: center;
                gap: 60px;
                padding: 40px 20px;
                background: rgba(255,255,255,0.05);
                backdrop-filter: blur(10px);
                margin: 0 40px;
                border-radius: 20px;
                transform: translateY(-30px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            }}
            
            .stat {{
                text-align: center;
            }}
            
            .stat-number {{
                font-size: 48px;
                font-weight: 900;
                color: #E50914;
                font-family: 'Bebas Neue', sans-serif;
                letter-spacing: 2px;
            }}
            
            .stat-label {{
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 2px;
                opacity: 0.7;
                margin-top: 8px;
                font-weight: 600;
            }}
            
            /* Filter Section */
            .filters {{
                display: flex;
                justify-content: center;
                gap: 16px;
                padding: 40px 40px 20px;
                flex-wrap: wrap;
            }}
            
            .filter-btn {{
                background: rgba(255,255,255,0.1);
                border: 2px solid transparent;
                color: white;
                padding: 14px 32px;
                border-radius: 50px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 1px;
                transition: all 0.3s ease;
                text-transform: uppercase;
            }}
            
            .filter-btn:hover {{
                background: rgba(229,9,20,0.2);
                border-color: #E50914;
                transform: translateY(-2px);
            }}
            
            .filter-btn.active {{
                background: #E50914;
                border-color: #E50914;
                box-shadow: 0 8px 20px rgba(229,9,20,0.4);
            }}
            
            /* Movies Grid */
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 40px;
            }}
            
            .movies-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
                gap: 30px;
                margin-top: 20px;
            }}
            
            .movie-card {{
                background: #141414;
                border-radius: 12px;
                overflow: hidden;
                transition: all 0.3s ease;
                cursor: pointer;
                position: relative;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            }}
            
            .movie-card:hover {{
                transform: translateY(-8px) scale(1.02);
                box-shadow: 0 12px 30px rgba(229,9,20,0.3);
            }}
            
            .movie-poster {{
                width: 100%;
                height: 420px;
                object-fit: cover;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: block;
            }}
            
            .movie-info {{
                padding: 20px;
            }}
            
            .movie-title {{
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 8px;
                line-height: 1.3;
            }}
            
            .movie-meta {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
                font-size: 14px;
            }}
            
            .movie-year {{
                color: #999;
            }}
            
            .movie-rating {{
                display: flex;
                align-items: center;
                gap: 6px;
                color: #FFD700;
                font-weight: 600;
            }}
            
            .movie-overview {{
                font-size: 14px;
                line-height: 1.6;
                color: #ccc;
                display: -webkit-box;
                -webkit-line-clamp: 3;
                -webkit-box-orient: vertical;
                overflow: hidden;
            }}
            
            .watched-badge {{
                position: absolute;
                top: 16px;
                right: 16px;
                background: #10B981;
                color: white;
                padding: 8px 16px;
                border-radius: 50px;
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 12px rgba(16,185,129,0.4);
            }}
            
            .empty-state {{
                text-align: center;
                padding: 100px 40px;
                opacity: 0.7;
            }}
            
            .empty-state-icon {{
                font-size: 96px;
                margin-bottom: 24px;
            }}
            
            .empty-state-text {{
                font-size: 24px;
                font-weight: 300;
            }}
            
            /* Footer */
            .footer {{
                text-align: center;
                padding: 60px 40px 40px;
                opacity: 0.5;
                font-size: 14px;
            }}
            
            /* Responsive */
            @media (max-width: 768px) {{
                .stats {{
                    flex-direction: column;
                    gap: 30px;
                    margin: 0 20px;
                }}
                
                .filters {{
                    padding: 20px;
                }}
                
                .container {{
                    padding: 20px;
                }}
                
                .movies-grid {{
                    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
                    gap: 16px;
                }}
                
                .movie-poster {{
                    height: 240px;
                }}
                
                .movie-info {{
                    padding: 12px;
                }}
                
                .movie-title {{
                    font-size: 16px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="hero">
            <div class="hero-content">
                <h1>{user_name}'s Watchlist</h1>
                <p class="subtitle">Shared via Binger</p>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat">
                <div class="stat-number" id="total-count">0</div>
                <div class="stat-label">Total Movies</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="watched-count">0</div>
                <div class="stat-label">Watched</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="towatch-count">0</div>
                <div class="stat-label">To Watch</div>
            </div>
        </div>
        
        <div class="filters">
            <button class="filter-btn active" data-filter="all">All</button>
            <button class="filter-btn" data-filter="watched">Watched</button>
            <button class="filter-btn" data-filter="towatch">To Watch</button>
        </div>
        
        <div class="container">
            <div class="movies-grid" id="movies-grid"></div>
            <div class="empty-state" id="empty-state" style="display: none;">
                <div class="empty-state-icon">🎬</div>
                <div class="empty-state-text">No movies found</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by Binger • Share your watchlist with friends</p>
        </div>
        
        <script>
            const movies = {movies_json};
            let currentFilter = 'all';
            
            function updateStats() {{
                const totalCount = movies.length;
                const watchedCount = movies.filter(m => m.watched).length;
                const toWatchCount = totalCount - watchedCount;
                
                document.getElementById('total-count').textContent = totalCount;
                document.getElementById('watched-count').textContent = watchedCount;
                document.getElementById('towatch-count').textContent = toWatchCount;
            }}
            
            function renderMovies() {{
                const grid = document.getElementById('movies-grid');
                const emptyState = document.getElementById('empty-state');
                
                let filteredMovies = movies;
                if (currentFilter === 'watched') {{
                    filteredMovies = movies.filter(m => m.watched);
                }} else if (currentFilter === 'towatch') {{
                    filteredMovies = movies.filter(m => !m.watched);
                }}
                
                if (filteredMovies.length === 0) {{
                    grid.innerHTML = '';
                    emptyState.style.display = 'block';
                    return;
                }}
                
                emptyState.style.display = 'none';
                
                grid.innerHTML = filteredMovies.map(movie => `
                    <div class="movie-card">
                        ${{movie.watched ? '<div class="watched-badge">✓ Watched</div>' : ''}}
                        <img src="${{movie.poster || 'https://via.placeholder.com/280x420/1a1a1a/666666?text=No+Poster'}}" 
                             alt="${{movie.title}}" 
                             class="movie-poster"
                             onerror="this.src='https://via.placeholder.com/280x420/1a1a1a/666666?text=No+Poster'">
                        <div class="movie-info">
                            <div class="movie-title">${{movie.title}}</div>
                            <div class="movie-meta">
                                <span class="movie-year">${{movie.release_date ? movie.release_date.split('-')[0] : 'N/A'}}</span>
                                <span class="movie-rating">⭐ ${{movie.rating ? movie.rating.toFixed(1) : 'N/A'}}</span>
                            </div>
                            <div class="movie-overview">${{movie.overview}}</div>
                        </div>
                    </div>
                `).join('');
            }}
            
            // Filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {{
                btn.addEventListener('click', () => {{
                    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    currentFilter = btn.dataset.filter;
                    renderMovies();
                }});
            }});
            
            // Initial render
            updateStats();
            renderMovies();
        </script>
    </body>
    </html>
    """
    
    return html

