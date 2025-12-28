from fastapi import APIRouter, Depends, HTTPException, Query, status, Body, Path
from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_

from sankalpa.backend.db.database import get_db
from sankalpa.core.security import get_current_user
from sankalpa.marketplace.models import (
    MarketplaceItem, MarketplaceReview, MarketplaceCategory,
    MarketplaceCategoryItem, MarketplaceCollection, MarketplaceCollectionItem
)
from sankalpa.marketplace.schemas import (
    MarketplaceItemCreate, MarketplaceItemUpdate, MarketplaceItemResponse,
    MarketplaceReviewCreate, MarketplaceReviewResponse,
    MarketplaceCategoryResponse, MarketplaceCollectionResponse
)
from sankalpa.core import get_logger
from sankalpa.core.caching import cache, cached

router = APIRouter()
logger = get_logger("marketplace")

# Item routes
@router.get("/items", response_model=List[MarketplaceItemResponse])
@cached("marketplace_items", ttl=300)  # Cache for 5 minutes
async def get_marketplace_items(
    type: Optional[str] = Query(None, description="Filter by item type"),
    category_id: Optional[str] = Query(None, description="Filter by category ID"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    author_id: Optional[str] = Query(None, description="Filter by author ID"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    sort_by: str = Query("created_at", description="Sort field: created_at, rating, download_count"),
    sort_order: str = Query("desc", description="Sort order: asc, desc"),
    limit: int = Query(20, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: Session = Depends(get_db)
):
    """Get marketplace items with filtering and sorting"""
    query = db.query(MarketplaceItem).filter(MarketplaceItem.is_public == True)
    
    # Apply filters
    if type:
        query = query.filter(MarketplaceItem.type == type)
    
    if category_id:
        query = query.join(MarketplaceCategoryItem).filter(
            MarketplaceCategoryItem.category_id == uuid.UUID(category_id)
        )
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                MarketplaceItem.name.ilike(search_term),
                MarketplaceItem.description.ilike(search_term)
            )
        )
    
    if author_id:
        query = query.filter(MarketplaceItem.author_id == uuid.UUID(author_id))
    
    if is_verified is not None:
        query = query.filter(MarketplaceItem.is_verified == is_verified)
    
    # Apply sorting
    if sort_order.lower() == "asc":
        query = query.order_by(getattr(MarketplaceItem, sort_by))
    else:
        query = query.order_by(desc(getattr(MarketplaceItem, sort_by)))
    
    # Apply pagination
    items = query.offset(offset).limit(limit).all()
    
    return items

@router.get("/items/{item_id}", response_model=MarketplaceItemResponse)
async def get_marketplace_item(
    item_id: str = Path(..., description="Item ID"),
    db: Session = Depends(get_db)
):
    """Get a specific marketplace item by ID"""
    item = db.query(MarketplaceItem).filter(
        MarketplaceItem.id == uuid.UUID(item_id),
        MarketplaceItem.is_public == True
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Increment download count
    item.download_count += 1
    db.commit()
    
    return item

@router.post("/items", response_model=MarketplaceItemResponse, status_code=status.HTTP_201_CREATED)
async def create_marketplace_item(
    item: MarketplaceItemCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new marketplace item"""
    new_item = MarketplaceItem(
        name=item.name,
        description=item.description,
        type=item.type,
        tags=item.tags,
        preview_image=item.preview_image,
        author_id=uuid.UUID(current_user["id"]),
        content=item.content,
        version=item.version,
        is_public=item.is_public
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    # Clear cache
    cache.delete("sankalpa:marketplace_items:")
    
    return new_item

@router.put("/items/{item_id}", response_model=MarketplaceItemResponse)
async def update_marketplace_item(
    item_id: str,
    item_update: MarketplaceItemUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a marketplace item"""
    db_item = db.query(MarketplaceItem).filter(
        MarketplaceItem.id == uuid.UUID(item_id)
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if str(db_item.author_id) != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")
    
    # Update fields
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    # Clear cache
    cache.delete("sankalpa:marketplace_items:")
    
    return db_item

@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_marketplace_item(
    item_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a marketplace item"""
    db_item = db.query(MarketplaceItem).filter(
        MarketplaceItem.id == uuid.UUID(item_id)
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if str(db_item.author_id) != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")
    
    db.delete(db_item)
    db.commit()
    
    # Clear cache
    cache.delete("sankalpa:marketplace_items:")
    
    return None

# Review routes
@router.post("/items/{item_id}/reviews", response_model=MarketplaceReviewResponse)
async def create_item_review(
    item_id: str,
    review: MarketplaceReviewCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a review for a marketplace item"""
    # Check if item exists
    db_item = db.query(MarketplaceItem).filter(
        MarketplaceItem.id == uuid.UUID(item_id)
    ).first()
    
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check if user has already reviewed this item
    existing_review = db.query(MarketplaceReview).filter(
        MarketplaceReview.item_id == uuid.UUID(item_id),
        MarketplaceReview.user_id == uuid.UUID(current_user["id"])
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this item")
    
    # Create review
    new_review = MarketplaceReview(
        item_id=uuid.UUID(item_id),
        user_id=uuid.UUID(current_user["id"]),
        rating=review.rating,
        comment=review.comment
    )
    
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # Update item rating
    reviews = db.query(MarketplaceReview).filter(
        MarketplaceReview.item_id == uuid.UUID(item_id)
    ).all()
    
    total_rating = sum(r.rating for r in reviews)
    avg_rating = total_rating / len(reviews)
    
    db_item.rating = avg_rating
    db_item.rating_count = len(reviews)
    db.commit()
    
    return new_review

@router.get("/items/{item_id}/reviews", response_model=List[MarketplaceReviewResponse])
async def get_item_reviews(
    item_id: str,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get reviews for a marketplace item"""
    reviews = db.query(MarketplaceReview).filter(
        MarketplaceReview.item_id == uuid.UUID(item_id)
    ).order_by(desc(MarketplaceReview.created_at)).offset(offset).limit(limit).all()
    
    return reviews

# Category routes
@router.get("/categories", response_model=List[MarketplaceCategoryResponse])
@cached("marketplace_categories", ttl=3600)  # Cache for 1 hour
async def get_categories(
    db: Session = Depends(get_db)
):
    """Get all marketplace categories"""
    categories = db.query(MarketplaceCategory).order_by(
        MarketplaceCategory.display_order
    ).all()
    
    return categories

# Collection routes
@router.get("/collections", response_model=List[MarketplaceCollectionResponse])
@cached("marketplace_collections", ttl=1800)  # Cache for 30 minutes
async def get_collections(
    featured_only: bool = Query(False, description="Get only featured collections"),
    db: Session = Depends(get_db)
):
    """Get marketplace collections"""
    query = db.query(MarketplaceCollection)
    
    if featured_only:
        query = query.filter(MarketplaceCollection.is_featured == True)
    
    collections = query.order_by(desc(MarketplaceCollection.created_at)).all()
    
    return collections

@router.get("/collections/{collection_id}", response_model=MarketplaceCollectionResponse)
async def get_collection(
    collection_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific marketplace collection"""
    collection = db.query(MarketplaceCollection).filter(
        MarketplaceCollection.id == uuid.UUID(collection_id)
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    return collection