from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action_type = Column(String, nullable=False, index=True)  # e.g., "CREATE", "UPDATE", "DELETE"
    resource_type = Column(String, nullable=False, index=True)  # e.g., "product", "order", "inventory"
    resource_id = Column(Integer, nullable=True)
    meta = Column(Text, nullable=True)  # JSON string with additional details
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    actor = relationship("User", back_populates="audit_logs")
