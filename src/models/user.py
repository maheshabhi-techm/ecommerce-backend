from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SqlEnum
from enum import Enum
from sqlalchemy.orm import relationship


class UserRole(str, Enum):
    CUSTOMER = "CUSTOMER"
    SELLER = "SELLER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False, index=True)
    last_name = Column(String(20), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True)
    role = Column(SqlEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    addresses = relationship("Address", back_populates="user", cascade="all, delete")
    products = relationship("Product", back_populates="seller")
    # created_at = Column(DateTime(timezone = True), server_default = func.now(), nullable = False)
    # updated_at = Column(DateTime(timezone = True), server_default = func.now(), onupdate = func.now(), nullable=False)
