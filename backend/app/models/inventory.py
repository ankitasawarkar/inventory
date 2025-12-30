from sqlalchemy import Column, Integer, String, Numeric, DateTime
from datetime import datetime
from app.db import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    sku = Column(String, unique=True, nullable=False, index=True)
    unit = Column(String, nullable=False)  # e.g., "kg", "pcs", "liters"
    quantity = Column(Numeric(10, 2), nullable=False, default=0)
    reorder_level = Column(Numeric(10, 2), nullable=True)
    cost_per_unit = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
