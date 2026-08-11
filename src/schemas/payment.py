from pydantic import BaseModel


class CreatePaymentOrderRequest(BaseModel):
    order_id: int


class CreatePaymentOrderResponse(BaseModel):
    order_id: int
    razorpay_order_id: str
    amount: int


class VerifyPaymentRequest(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class MarkPaymentFailureRequest(BaseModel):
    order_id: int
    razorpay_order_id: str
    razorpay_payment_id: str | None = None
    error_code: str | None = None
    error_description: str | None = None


class VerifyPaymentResponse(BaseModel):
    success: bool
    message: str
