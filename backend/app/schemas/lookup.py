from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class LookupBase(BaseModel):
    set: str
    key: str
    value: str
    description: Optional[str] = None
    scope: str = "GLOBAL"  # e.g. GLOBAL, TENANT
    order_by: int = 0
    is_active: bool = True


class LookupCreate(LookupBase):
    pass


class LookupUpdate(BaseModel):
    set: Optional[str] = None
    key: Optional[str] = None
    value: Optional[str] = None
    description: Optional[str] = None
    scope: Optional[str] = None
    order_by: Optional[int] = None
    is_active: Optional[bool] = None


class LookupResponse(LookupBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
