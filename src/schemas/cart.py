from pydantic import BaseModel, Field

class CartCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class CartUpdate(BaseModel):
    quantity: int = Field(gt=0)

class CartItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    subtotal: float

    model_config = {
        "from_attributes" : True
    }

class CartResponse(BaseModel):
    items: list[CartItemResponse]
    grand_total: float

    model_config = {
        "from_attributes" : True
    }