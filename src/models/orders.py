from src.database import Base
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey,
    DateTime,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from src.models.order_status import OrderStatus, PaymentStatus, PaymentMethod


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    address_id = Column(Integer, ForeignKey("address.id"))
    total_amount = Column(Float)
    order_status = Column(SqlEnum(OrderStatus), default=OrderStatus.PLACED)
    payment_status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_method = Column(SqlEnum(PaymentMethod))

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    user = relationship("User")
    address = relationship("Address")
    items = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan"
    )
    payment = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
