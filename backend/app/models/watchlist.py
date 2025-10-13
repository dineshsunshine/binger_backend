"""
WatchlistItem model for storing user's movie watchlist.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Index, JSON
from sqlalchemy.orm import relationship
from ..core.database import Base


class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    movie_id = Column(String(100), nullable=False)  # e.g., "movie-550" or "tv-1396"
    movie_data = Column(JSON, nullable=False)  # Full Movie object as JSON
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="watchlist_items")
    
    # Composite unique constraint to prevent duplicate movies per user
    __table_args__ = (
        Index('idx_user_movie', 'user_id', 'movie_id', unique=True),
    )

