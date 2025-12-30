from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Self-referential relationship for nested categories
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    
    # Relationships
    products = relationship("Product", back_populates="category", foreign_keys="Product.category_id")
    subcategory_products = relationship("Product", back_populates="subcategory", foreign_keys="Product.subcategory_id")
