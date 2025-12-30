from sqlalchemy import Column, Integer, String, ForeignKey, Text, Numeric, Boolean, DateTime, Enum as SQLEnum, Date
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PRODUCTION = "in_production"
    READY = "ready"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False, index=True)
    customer_name = Column(String, nullable=False)
    customer_contact = Column(String, nullable=False)
    customer_email = Column(String, nullable=True)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    notes = Column(Text, nullable=True)
    is_custom = Column(Boolean, default=False)
    expected_delivery_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    production_records = relationship("ProductionRecord", back_populates="order")
    profit_records = relationship("ProfitRecord", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_snapshot = Column(Text, nullable=False)  # JSON string with product data at time of order
    quantity = Column(Integer, nullable=False, default=1)
    custom_requirements = Column(Text, nullable=True)  # JSON string
    unit_price = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="items")
    production_records = relationship("ProductionRecord", back_populates="order_item")


class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    stage_name = Column(String, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="production_records")
    order_item = relationship("OrderItem", back_populates="production_records")
    operator = relationship("User", back_populates="production_records")


class ProfitRecord(Base):
    __tablename__ = "profit_records"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    revenue = Column(Numeric(10, 2), nullable=False)
    costs = Column(Numeric(10, 2), nullable=False)
    profit = Column(Numeric(10, 2), nullable=False)
    date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="profit_records")
