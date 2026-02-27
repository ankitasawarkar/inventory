from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class InventoryCategory(Base):
    """Inventory classification for raw materials, hardware, finishes, etc.

    Top-level examples: MAT, HRD, FIN, PKG.
    Child examples: PLK, SCR, LAC, etc.
    """

    __tablename__ = "inventory_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    code = Column(String, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("inventory_categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Self-referential relationship
    parent = relationship("InventoryCategory", remote_side=[id], backref="children")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    # High-level inventory code, e.g. MAT-PLK-SAO-25X3M
    item_code = Column(String, unique=True, nullable=True, index=True)
    # Material shorthand, e.g. SAO, MDF, PLY18
    material_code = Column(String, nullable=True, index=True)
    # Optional links to inventory categories for reporting and filtering
    category_id = Column(Integer, ForeignKey("inventory_categories.id"), nullable=True)
    subcategory_id = Column(Integer, ForeignKey("inventory_categories.id"), nullable=True)
    unit = Column(String, nullable=False)  # e.g., "kg", "pcs", "liters"
    quantity = Column(Numeric(10, 2), nullable=False, default=0)
    reorder_level = Column(Numeric(10, 2), nullable=True)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("InventoryCategory", foreign_keys=[category_id])
    subcategory = relationship("InventoryCategory", foreign_keys=[subcategory_id])
