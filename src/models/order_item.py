from src.database import Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class OrderItem(Base):

    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    quantity = Column(Integer)
    price = Column(Float)
    subtotal = Column(Float)

    product = relationship("Product")
    order = relationship("Order", back_populates="items")
