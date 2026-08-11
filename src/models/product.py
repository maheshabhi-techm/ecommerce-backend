from src.database import Base
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Enum as SqlEnum,
)
from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from src.models.product_status import ProductStatus


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    sku = Column(String(100), unique=True, nullable=False)
    brand = Column(String(100), nullable=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float)
    stock_quantity = Column(Integer, default=0)
    status = Column(SqlEnum(ProductStatus), default=ProductStatus.PENDING)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    seller = relationship("User", back_populates="products")
    category = relationship("Category", back_populates="products")
    cart_items = relationship("Cart", back_populates="product")
