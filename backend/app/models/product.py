from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid
from app.db import Base


class ProductStatus(str, enum.Enum):
    DRAFT = "draft"
    DEVELOPMENT = "development"
    READY = "ready"
    ARCHIVED = "archived"


class StageStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False, index=True)
    # Full product code, e.g. CH-DIN-ROYC-WO-WAL-STD
    sku = Column(String, unique=True, nullable=True, index=True)
    # Short model segment used inside SKU, e.g. ROYC, MIST
    model_code = Column(String, nullable=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    subcategory_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    description = Column(Text, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_customizable = Column(Boolean, default=False)
    status = Column(SQLEnum(ProductStatus), default=ProductStatus.DRAFT, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category", back_populates="products", foreign_keys=[category_id])
    subcategory = relationship("Category", back_populates="subcategory_products", foreign_keys=[subcategory_id])
    creator = relationship("User", back_populates="created_products", foreign_keys=[created_by])
    development_stages = relationship("ProductDevelopmentStage", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    cart_items = relationship("CartItem", back_populates="product")


class ProductDevelopmentStage(Base):
    __tablename__ = "product_development_stages"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stage_order = Column(Integer, nullable=False)
    stage_name = Column(String, nullable=False)
    stage_description = Column(Text, nullable=True)
    materials_used = Column(Text, nullable=True)  # JSON string
    labor_hours_estimate = Column(Numeric(10, 2), nullable=True)
    expected_days = Column(Integer, nullable=True)
    actual_days = Column(Integer, nullable=True)
    quality_checklist = Column(Text, nullable=True)  # JSON string
    stage_status = Column(SQLEnum(StageStatus), default=StageStatus.NOT_STARTED)
    responsible_person = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="development_stages")
    images = relationship("ProductImage", back_populates="stage")
    responsible = relationship("User")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stage_id = Column(Integer, ForeignKey("product_development_stages.id"), nullable=True)
    file_path = Column(String, nullable=False)  # Relative to MEDIA_ROOT
    original_name = Column(String, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    size = Column(Integer, nullable=True)  # File size in bytes
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    product = relationship("Product", back_populates="images")
    stage = relationship("ProductDevelopmentStage", back_populates="images")
    uploader = relationship("User", back_populates="uploaded_images")
