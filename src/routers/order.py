from fastapi import Depends, APIRouter
from src.database import get_db
from src.dependencies.auth import get_current_user
import src.services.order_service as order_service
from src.schemas.order import OrderCheckoutRequest, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderResponse])
def get_orders_api(db=Depends(get_db), current_user=Depends(get_current_user)):
    return order_service.get_orders(db, current_user)


@router.post("/checkout")
def orders_checkout_api(
    request: OrderCheckoutRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
):
    return order_service.order_checkout(request, db, current_user)
