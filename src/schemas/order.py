from pydantic import BaseModel
from src.models.order_status import OrderStatus, PaymentMethod, PaymentStatus


class OrderCheckoutRequest(BaseModel):
    address_id: int
    payment_method: str


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float
    subtotal: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    order_id: int
    order_number: str
    total_amount: float
    order_status: OrderStatus
    payment_status: PaymentStatus
    payment_method: PaymentMethod
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True

