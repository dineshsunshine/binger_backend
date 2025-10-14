"""
FastAPI application initialization and configuration.
"""
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .core.config import settings
from .core.database import init_db, get_db
from .api.v1.router import api_router
from .models.shareable_link import ShareableLink
from .models.watchlist import WatchlistItem
from .models.restaurant import SavedRestaurant

# Initialize database
init_db()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    root_path="/Binger",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*" else ["*"]
allow_credentials = settings.CORS_ORIGINS != "*"

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Binger API"}


# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


# Public shareable watchlist endpoint (not under /api)
@app.get("/shared/watchlist/{token}", response_class=HTMLResponse)
async def view_shared_watchlist(
    token: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Public endpoint to view a shared list (movies and/or restaurants).
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
            <title>List Not Found - Binger</title>
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
                <p>List not found or has been removed</p>
            </div>
        </body>
        </html>
        """, status_code=404)
    
    # Get user and their data
    user = shareable_link.user
    entity_types = shareable_link.entity_types or ["movies", "restaurants"]
    
    # Query movies if needed
    watchlist_items = []
    if "movies" in entity_types:
        watchlist_items = db.query(WatchlistItem).filter(
            WatchlistItem.user_id == user.id
        ).order_by(WatchlistItem.added_at.desc()).all()
    
    # Query restaurants if needed
    saved_restaurants = []
    if "restaurants" in entity_types:
        saved_restaurants = db.query(SavedRestaurant).filter(
            SavedRestaurant.user_id == user.id
        ).order_by(SavedRestaurant.added_at.desc()).all()
    
    # Generate combined HTML
    from .templates.combined_shareable_page import generate_combined_shareable_html
    html_content = generate_combined_shareable_html(user, watchlist_items, saved_restaurants, entity_types)
    
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

