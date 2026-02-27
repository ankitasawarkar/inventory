from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class InventoryCategoryBase(BaseModel):
    name: str
    code: str
    parent_id: Optional[int] = None


class InventoryCategoryCreate(InventoryCategoryBase):
    pass


class InventoryCategoryUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    parent_id: Optional[int] = None


class InventoryCategoryResponse(InventoryCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    children: Optional[List["InventoryCategoryResponse"]] = []

    class Config:
        from_attributes = True


InventoryCategoryResponse.model_rebuild()
