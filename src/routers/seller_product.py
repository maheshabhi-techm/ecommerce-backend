from fastapi import APIRouter, Depends
from src.database import get_db
from src.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from src.dependencies.role import require_roles
from src.models.user import UserRole
import src.services.seller_product_service as product_service

router = APIRouter(prefix="/seller/products", tags=["Seller Products"])


@router.post("/", response_model=ProductResponse)
def create_product_api(
    request: ProductCreate,
    db=Depends(get_db),
    current_user=Depends(require_roles(UserRole.SELLER, UserRole.ADMIN)),
):
    return product_service.create_product(request, db, current_user)


@router.get("/", response_model=list[ProductResponse])
def get_products_api(db=Depends(get_db)):
    return product_service.get_all_procuts(db)


@router.get("/{id}", response_model=ProductResponse)
def get_product_api(id: int, db=Depends(get_db)):
    return product_service.get_product_by_id(id, db)


@router.put("/{id}", response_model=ProductResponse)
def update_product_api(
    id: int,
    request: ProductUpdate,
    db=Depends(get_db),
    current_user=Depends(require_roles(UserRole.SELLER)),
):
    return product_service.update_product(id, request, db, current_user)


@router.delete("/{id}")
def delete_product_api(
    id: int, db=Depends(get_db), current_user=Depends(require_roles(UserRole.SELLER))
):
    return product_service.delete_product(id, db, current_user)
