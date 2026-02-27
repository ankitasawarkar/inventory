from pydantic import BaseModel, condecimal
from typing import Optional, List
from datetime import datetime
from app.models.product import ProductStatus, StageStatus


class ProductImageResponse(BaseModel):
    id: int
    product_id: int
    stage_id: Optional[int] = None
    file_path: str
    original_name: str
    width: Optional[int] = None
    height: Optional[int] = None
    size: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ProductDevelopmentStageBase(BaseModel):
    stage_order: int
    stage_name: str
    stage_description: Optional[str] = None
    materials_used: Optional[str] = None
    labor_hours_estimate: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    expected_days: Optional[int] = None
    actual_days: Optional[int] = None
    quality_checklist: Optional[str] = None
    stage_status: StageStatus = StageStatus.NOT_STARTED
    responsible_person: Optional[int] = None
    notes: Optional[str] = None


class ProductDevelopmentStageCreate(ProductDevelopmentStageBase):
    product_id: int


class ProductDevelopmentStageUpdate(BaseModel):
    stage_order: Optional[int] = None
    stage_name: Optional[str] = None
    stage_description: Optional[str] = None
    materials_used: Optional[str] = None
    labor_hours_estimate: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    expected_days: Optional[int] = None
    actual_days: Optional[int] = None
    quality_checklist: Optional[str] = None
    stage_status: Optional[StageStatus] = None
    responsible_person: Optional[int] = None
    notes: Optional[str] = None


class ProductDevelopmentStageResponse(ProductDevelopmentStageBase):
    id: int
    product_id: int
    images: List[ProductImageResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    title: str
    sku: Optional[str] = None
    model_code: Optional[str] = None
    category_id: int
    subcategory_id: Optional[int] = None
    description: Optional[str] = None
    base_price: condecimal(max_digits=10, decimal_places=2)
    is_customizable: bool = False
    status: ProductStatus = ProductStatus.DRAFT


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    sku: Optional[str] = None
    model_code: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    description: Optional[str] = None
    base_price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    is_customizable: Optional[bool] = None
    status: Optional[ProductStatus] = None


class ProductResponse(ProductBase):
    id: int
    uuid: str
    created_by: Optional[int] = None
    development_stages: List[ProductDevelopmentStageResponse] = []
    images: List[ProductImageResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    id: int
    uuid: str
    title: str
    sku: Optional[str] = None
    model_code: Optional[str] = None
    base_price: condecimal(max_digits=10, decimal_places=2)
    status: ProductStatus
    category_id: int
    created_at: datetime

    class Config:
        from_attributes = True
