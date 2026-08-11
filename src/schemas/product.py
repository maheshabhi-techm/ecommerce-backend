from pydantic import BaseModel, Field
from src.models.product_status import ProductStatus

class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: str | None = None
    brand: str
    price: float = Field(gt=0)
    discount_price: float | None = Field(default=None, ge=0)
    stock_quantity: int = Field(ge=0)

class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    brand: str | None = None
    price: float | None = Field(default=None, gt=0)
    discount_price: float | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    sku: str
    price: float
    discount_price: float | None
    stock_quantity: int
    status: ProductStatus

    class Config:
        from_attributes = True

class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    page: int 
    size: int 
    total: int
    total_pages: int 
