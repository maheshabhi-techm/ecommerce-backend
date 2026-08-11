from fastapi import Depends, APIRouter, Request
from src.schemas.payment import (
    CreatePaymentOrderRequest,
    VerifyPaymentRequest,
    MarkPaymentFailureRequest,
)
from src.database import get_db
from src.dependencies.auth import get_current_user
import src.services.payment as payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/create-order")
def create_payment_order_api(
    request: CreatePaymentOrderRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return payment_service.create_payment_order(request, db, current_user)


@router.post("/verify")
def verify_payment_api(
    request: VerifyPaymentRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return payment_service.verify_payment(request, db, current_user)


@router.post("/failure")
def mark_payment_failure_api(
    request: MarkPaymentFailureRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return payment_service.mark_payment_failure(request, db, current_user)


@router.post("/webhook")
async def payment_webhook_api(request: Request, db=Depends(get_db)):
    return payment_service.payment_webhook(db, request)
