"""
Restaurant model for saving user's restaurant list.
"""
import uuid
from sqlalchemy import Column, String, Boolean, JSON, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class SavedRestaurant(Base):
    """Model for user's saved restaurants."""
    __tablename__ = "saved_restaurants"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    restaurant_id = Column(String, nullable=False, index=True)  # Unique identifier from OpenAI/search
    restaurant_data = Column(JSON, nullable=False)  # Full restaurant JSON data
    visited = Column(Boolean, default=False, nullable=False)  # Has user been there?
    personal_rating = Column(Integer, nullable=True)  # User's rating 1-5
    notes = Column(Text, nullable=True)  # Personal notes
    tags = Column(JSON, nullable=True)  # Array of tags like ["Anniversary", "Business"]
    added_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="saved_restaurants")

