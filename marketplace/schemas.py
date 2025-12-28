from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

# Base schemas
class MarketplaceItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    type: str = Field(..., pattern="^(chain|agent|plugin)$")
    tags: Optional[List[str]] = Field(None, max_items=10)
    preview_image: Optional[str] = None
    content: Dict[str, Any] = Field(...)
    version: str = Field("1.0.0", regex=r"^\d+\.\d+\.\d+$")
    is_public: bool = True

class MarketplaceItemCreate(MarketplaceItemBase):
    pass

class MarketplaceItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    tags: Optional[List[str]] = Field(None, max_items=10)
    preview_image: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    version: Optional[str] = Field(None, regex=r"^\d+\.\d+\.\d+$")
    is_public: Optional[bool] = None

class MarketplaceItemResponse(MarketplaceItemBase):
    id: uuid.UUID
    author_id: uuid.UUID
    is_verified: bool
    download_count: int
    rating: float
    rating_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class MarketplaceReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=10)

class MarketplaceReviewCreate(MarketplaceReviewBase):
    pass

class MarketplaceReviewResponse(MarketplaceReviewBase):
    id: uuid.UUID
    item_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class MarketplaceCategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0
    parent_id: Optional[uuid.UUID] = None

class MarketplaceCategoryCreate(MarketplaceCategoryBase):
    pass

class MarketplaceCategoryResponse(MarketplaceCategoryBase):
    id: uuid.UUID
    subcategories: Optional[List['MarketplaceCategoryResponse']] = None
    
    class Config:
        orm_mode = True

class MarketplaceCollectionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    is_featured: bool = False

class MarketplaceCollectionCreate(MarketplaceCollectionBase):
    items: List[uuid.UUID] = Field(..., min_items=1)

class MarketplaceCollectionItemResponse(BaseModel):
    item: MarketplaceItemResponse
    display_order: int
    
    class Config:
        orm_mode = True

class MarketplaceCollectionResponse(MarketplaceCollectionBase):
    id: uuid.UUID
    curator_id: uuid.UUID
    items: List[MarketplaceCollectionItemResponse]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

# Resolve circular reference
MarketplaceCategoryResponse.update_forward_refs()