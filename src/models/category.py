from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime
from src.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )
    updated_at = Column(
        DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now()
    )

    parent = relationship("Category", remote_side=[id], back_populates="children")
    children = relationship("Category", back_populates="parent", cascade="all")

    products = relationship("Product", back_populates="category")
