from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from app.db import get_db
from app.models.inventory import InventoryItem
from app.models.user import User
from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse,
    InventoryAdjustment
)
from app.auth import require_admin, require_staff_or_admin

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("", response_model=List[InventoryItemResponse])
def list_inventory(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """List all inventory items."""
    items = db.query(InventoryItem).offset(skip).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=InventoryItemResponse)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
):
    """Get specific inventory item."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.post("", response_model=InventoryItemResponse)
def create_inventory_item(
    item_data: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create a new inventory item (admin only)."""
    # Check if SKU already exists
    if db.query(InventoryItem).filter(InventoryItem.sku == item_data.sku).first():
        raise HTTPException(status_code=400, detail="SKU already exists")

    # Check if item_code already exists (if provided)
    if item_data.item_code and db.query(InventoryItem).filter(InventoryItem.item_code == item_data.item_code).first():
        raise HTTPException(status_code=400, detail="Item code already exists")
    
    item = InventoryItem(**item_data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item


@router.put("/{item_id}", response_model=InventoryItemResponse)
def update_inventory_item(
    item_id: int,
    item_data: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update inventory item details (admin only)."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Check SKU uniqueness if being updated
    if item_data.sku and item_data.sku != item.sku:
        if db.query(InventoryItem).filter(InventoryItem.sku == item_data.sku).first():
            raise HTTPException(status_code=400, detail="SKU already exists")

    # Check item_code uniqueness if being updated
    if item_data.item_code and item_data.item_code != item.item_code:
        if db.query(InventoryItem).filter(InventoryItem.item_code == item_data.item_code).first():
            raise HTTPException(status_code=400, detail="Item code already exists")
    
    update_data = item_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.patch("/{item_id}/adjust", response_model=InventoryItemResponse)
def adjust_inventory(
    item_id: int,
    adjustment: InventoryAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Adjust inventory quantity (admin only)."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    new_quantity = item.quantity + adjustment.quantity_change
    
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Insufficient inventory")
    
    item.quantity = new_quantity
    db.commit()
    db.refresh(item)
    
    # TODO: Log adjustment in audit log
    
    return item


@router.delete("/{item_id}")
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete an inventory item (admin only)."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    db.delete(item)
    db.commit()
    
    return {"message": "Inventory item deleted successfully"}
