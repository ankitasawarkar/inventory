from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime


class InventoryItemBase(BaseModel):
    name: str
    sku: str
    item_code: Optional[str] = None
    material_code: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    unit: str
    quantity: condecimal(max_digits=10, decimal_places=2)
    reorder_level: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    cost_per_unit: condecimal(max_digits=10, decimal_places=2)


class InventoryItemCreate(InventoryItemBase):
    pass


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    item_code: Optional[str] = None
    material_code: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    unit: Optional[str] = None
    quantity: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    reorder_level: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    cost_per_unit: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class InventoryAdjustment(BaseModel):
    quantity_change: condecimal(max_digits=10, decimal_places=2)
    reason: Optional[str] = None


class InventoryItemResponse(InventoryItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
