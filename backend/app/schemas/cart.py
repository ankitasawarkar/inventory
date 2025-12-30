from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CartItemBase(BaseModel):
    product_id: int
    quantity: int
    selected_options: Optional[str] = None


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None
    selected_options: Optional[str] = None


class CartItemResponse(CartItemBase):
    id: int
    cart_id: int
    added_at: datetime

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    items: list[CartItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
