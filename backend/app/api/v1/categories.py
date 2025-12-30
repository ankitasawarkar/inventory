from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.auth import require_admin

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    """List all categories with nested subcategories."""
    # Get root categories (those without parents)
    categories = db.query(Category).filter(Category.parent_id.is_(None)).all()
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a specific category by ID."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("", response_model=CategoryResponse)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new category (admin only)."""
    # Check if slug already exists
    if db.query(Category).filter(Category.slug == category_data.slug).first():
        raise HTTPException(status_code=400, detail="Category slug already exists")
    
    # Verify parent exists if provided
    if category_data.parent_id:
        parent = db.query(Category).filter(Category.id == category_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")
    
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update a category (admin only)."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check slug uniqueness if being updated
    if category_data.slug and category_data.slug != category.slug:
        if db.query(Category).filter(Category.slug == category_data.slug).first():
            raise HTTPException(status_code=400, detail="Category slug already exists")
    
    # Update fields
    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete a category (admin only). Soft delete by default."""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has products
    if category.products or category.subcategory_products:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with associated products"
        )
    
    # Check if category has subcategories
    if category.subcategories:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with subcategories"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}
