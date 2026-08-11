from src.database import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC


class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    PAID = "PAID"


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_gateway = Column(String(50), default="RAZORPAY")
    transaction_id = Column(String(255), nullable=True)
    gateway_payment_id = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.CREATED)
    created_at = Column(DateTime, default=datetime.now(UTC))

    order = relationship("Order", back_populates="payment")
