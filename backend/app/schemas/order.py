from pydantic import BaseModel, condecimal, EmailStr
from typing import Optional, List
from datetime import datetime, date
from app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_snapshot: str  # JSON string
    quantity: int
    custom_requirements: Optional[str] = None
    unit_price: condecimal(max_digits=10, decimal_places=2)
    subtotal: condecimal(max_digits=10, decimal_places=2)


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    custom_requirements: Optional[str] = None


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: str
    customer_contact: str
    customer_email: Optional[EmailStr] = None
    notes: Optional[str] = None
    is_custom: bool = False
    expected_delivery_date: Optional[date] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_contact: Optional[str] = None
    customer_email: Optional[EmailStr] = None
    status: Optional[OrderStatus] = None
    notes: Optional[str] = None
    expected_delivery_date: Optional[date] = None


class OrderResponse(OrderBase):
    id: int
    order_number: str
    status: OrderStatus
    total_amount: condecimal(max_digits=10, decimal_places=2)
    items: List[OrderItemResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductionRecordBase(BaseModel):
    stage_name: str
    notes: Optional[str] = None


class ProductionRecordCreate(ProductionRecordBase):
    order_id: Optional[int] = None
    order_item_id: Optional[int] = None
    product_id: Optional[int] = None
    operator_id: Optional[int] = None


class ProductionRecordResponse(ProductionRecordBase):
    id: int
    order_id: Optional[int] = None
    order_item_id: Optional[int] = None
    product_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    operator_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
