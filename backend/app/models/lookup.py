from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.db import Base


class Lookup(Base):
    """Generic lookup table for dropdown values across the app.

    Examples:
    - set = "INVENTORY_UNIT", key = "PCS", value = "Pieces"
    - set = "PRODUCT_FINISH", key = "WAL", value = "Walnut Finish"

    Scope allows you to distinguish between global and tenant-specific
    values if you later introduce multi-tenant support.
    """

    __tablename__ = "lookups"

    id = Column(Integer, primary_key=True, index=True)
    # Logical group / dropdown this belongs to, e.g. "INVENTORY_UNIT"
    set = Column(String, nullable=False, index=True)
    # Internal code used in your app or SKUs, e.g. "PCS", "WAL"
    key = Column(String, nullable=False, index=True)
    # Human-readable label shown in dropdowns
    value = Column(String, nullable=False)
    description = Column(String, nullable=True)
    # GLOBAL, TENANT, or other scopes as needed
    scope = Column(String, nullable=False, default="GLOBAL", index=True)
    order_by = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
