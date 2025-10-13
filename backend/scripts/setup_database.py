"""
Database initialization script.
Run this to create all tables in the database.
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import init_db, engine, Base
from app.models import User, WatchlistItem, UserSetting


def setup_database():
    """Initialize database with all tables."""
    print("🗄️  Setting up database...")
    print(f"📍 Database URL: {engine.url}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database setup complete!")
    print("\nTables created:")
    print("  - users")
    print("  - watchlist_items")
    print("  - user_settings")


if __name__ == "__main__":
    setup_database()

