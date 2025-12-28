from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from sankalpa.backend.db.database import Base

class MarketplaceItem(Base):
    """Model for marketplace items (chain templates, agent configs, etc.)"""
    __tablename__ = "marketplace_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    type = Column(String(50), nullable=False, index=True)  # chain, agent, plugin, etc.
    tags = Column(JSON, nullable=True)
    preview_image = Column(String(255), nullable=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(JSON, nullable=False)  # The actual template content
    version = Column(String(20), nullable=False, default="1.0.0")
    is_public = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    download_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = relationship("User", back_populates="marketplace_items")
    reviews = relationship("MarketplaceReview", back_populates="item")
    
class MarketplaceReview(Base):
    """Model for marketplace item reviews"""
    __tablename__ = "marketplace_reviews"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_items.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5 stars
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    item = relationship("MarketplaceItem", back_populates="reviews")
    user = relationship("User")
    
class MarketplaceCategory(Base):
    """Model for marketplace categories"""
    __tablename__ = "marketplace_categories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_categories.id"), nullable=True)
    
    # Relationships
    subcategories = relationship("MarketplaceCategory", 
                                backref=relationship.backref("parent", remote_side=[id]))
    items = relationship("MarketplaceCategoryItem", back_populates="category")
    
class MarketplaceCategoryItem(Base):
    """Association table between categories and items"""
    __tablename__ = "marketplace_category_items"
    
    category_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_categories.id"), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_items.id"), primary_key=True)
    
    # Relationships
    category = relationship("MarketplaceCategory", back_populates="items")
    item = relationship("MarketplaceItem")
    
class MarketplaceCollection(Base):
    """Model for collections of marketplace items (curated lists)"""
    __tablename__ = "marketplace_collections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    curator_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    is_featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    curator = relationship("User")
    items = relationship("MarketplaceCollectionItem", back_populates="collection")
    
class MarketplaceCollectionItem(Base):
    """Association table between collections and items"""
    __tablename__ = "marketplace_collection_items"
    
    collection_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_collections.id"), primary_key=True)
    item_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_items.id"), primary_key=True)
    display_order = Column(Integer, default=0)
    
    # Relationships
    collection = relationship("MarketplaceCollection", back_populates="items")
    item = relationship("MarketplaceItem")