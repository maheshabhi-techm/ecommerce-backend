from src.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class ProductImage(Base):

    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
