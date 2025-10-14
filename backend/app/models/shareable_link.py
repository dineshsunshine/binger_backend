"""
Shareable Link Model
Allows users to create public shareable links to their watchlists and restaurant lists
"""
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import uuid


class ShareableLink(Base):
    """Model for shareable watchlist/restaurant links"""
    __tablename__ = "shareable_links"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    token = Column(String, unique=True, nullable=False, index=True)  # Unique token for the shareable URL
    entity_types = Column(JSON, default=["movies", "restaurants"], nullable=False)  # What to show: ["movies"], ["restaurants"], or ["movies", "restaurants"]
    is_active = Column(Boolean, default=True, nullable=False)  # Can be revoked
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", backref="shareable_link")
    
    def __repr__(self):
        return f"<ShareableLink(user_id={self.user_id}, token={self.token}, is_active={self.is_active}, entity_types={self.entity_types})>"

