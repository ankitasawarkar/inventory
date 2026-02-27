from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.inventory import InventoryCategory, InventoryItem
from app.models.user import User
from app.schemas.inventory_category import (
    InventoryCategoryCreate,
    InventoryCategoryUpdate,
    InventoryCategoryResponse,
)
from app.auth import require_admin, require_staff_or_admin


router = APIRouter(prefix="/api/inventory-categories", tags=["Inventory Categories"])


@router.get("", response_model=List[InventoryCategoryResponse])
def list_inventory_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin),
):
    """Return all root inventory categories with nested children."""
    roots = (
        db.query(InventoryCategory)
        .filter(InventoryCategory.parent_id.is_(None))
        .order_by(InventoryCategory.name)
        .all()
    )
    return roots


@router.post("", response_model=InventoryCategoryResponse)
def create_inventory_category(
    category_data: InventoryCategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Create a new inventory category or subcategory (admin only)."""
    # Ensure parent exists if provided
    if category_data.parent_id:
        parent = (
            db.query(InventoryCategory)
            .filter(InventoryCategory.id == category_data.parent_id)
            .first()
        )
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    category = InventoryCategory(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=InventoryCategoryResponse)
def update_inventory_category(
    category_id: int,
    category_data: InventoryCategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Update an inventory category (admin only)."""
    category = (
        db.query(InventoryCategory)
        .filter(InventoryCategory.id == category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Inventory category not found")

    # Ensure new parent (if provided) exists and is not the category itself
    if category_data.parent_id is not None:
        if category_data.parent_id == category_id:
            raise HTTPException(status_code=400, detail="Category cannot be its own parent")
        parent = (
            db.query(InventoryCategory)
            .filter(InventoryCategory.id == category_data.parent_id)
            .first()
        )
        if not parent:
            raise HTTPException(status_code=404, detail="Parent category not found")

    update_data = category_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_inventory_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Delete an inventory category (admin only).

    Prevent deletion if it has children or is referenced by any inventory items.
    """
    category = (
        db.query(InventoryCategory)
        .filter(InventoryCategory.id == category_id)
        .first()
    )
    if not category:
        raise HTTPException(status_code=404, detail="Inventory category not found")

    # Check children
    if category.children:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category with subcategories",
        )

    # Check usage by inventory items
    in_use = (
        db.query(InventoryItem)
        .filter(
            (InventoryItem.category_id == category_id)
            | (InventoryItem.subcategory_id == category_id)
        )
        .first()
    )
    if in_use:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category that is used by inventory items",
        )

    db.delete(category)
    db.commit()
    return {"message": "Inventory category deleted successfully"}
