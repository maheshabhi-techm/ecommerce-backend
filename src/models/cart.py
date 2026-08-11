from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from src.database import Base


class Cart(Base):

    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    user = relationship("User")
    product = relationship("Product", back_populates="cart_items")
