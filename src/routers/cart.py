from fastapi import APIRouter, Depends, status
from src.schemas.cart import CartCreate, CartUpdate, CartResponse
from src.database import get_db
from src.dependencies.auth import get_current_user
from src.dependencies.role import require_roles
from src.models.user import UserRole
import src.services.cart_service as cart_service

router = APIRouter(prefix="/cart", tags=["Product Cart"])


@router.post("")
def add_to_cart_api(
    request: CartCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    role=Depends(require_roles(UserRole.CUSTOMER.value, UserRole.ADMIN.value)),
):
    return cart_service.add_to_cart(request, db, current_user)


@router.get("", response_model=CartResponse)
def get_cart_details_api(
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    role=Depends(require_roles(UserRole.CUSTOMER.value, UserRole.ADMIN.value)),
):
    return cart_service.get_cart_details(db, current_user)


@router.put("/{id}", response_model=CartUpdate)
def update_cart_api(
    id: int,
    request: CartUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    role=Depends(require_roles(UserRole.CUSTOMER, UserRole.ADMIN)),
):
    return cart_service.update_cart(id, request, db, current_user)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_cart_by_id_api(
    id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    role=Depends(require_roles(UserRole.ADMIN, UserRole.CUSTOMER)),
):
    return cart_service.delete_cart_by_id(id, db, current_user)


@router.delete("", status_code=status.HTTP_200_OK)
def clear_cart_api(
    db=Depends(get_db),
    current_user=Depends(get_current_user),
    role=Depends(require_roles(UserRole.ADMIN, UserRole.CUSTOMER)),
):
    return cart_service.clear_cart(db, current_user)
