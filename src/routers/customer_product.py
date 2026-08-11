from fastapi import APIRouter, Depends
from src.schemas.product import ProductListResponse
from src.database import get_db
import src.services.customer_product_service as product_service
from sqlalchemy.orm import Session

router = APIRouter(prefix="", tags=["Customer Products"])


@router.get("/products", response_model=ProductListResponse)
def get_products(
    db: Session = Depends(get_db),
    keyword: str | None = None,
    category_id: int | None = None,
    brand: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock: bool = False,
    sort_by: str = "created_at",
    order: str = "desc",
    page: int = 1,
    size: int = 10,
):
    return product_service.get_all_products(
        db=db,
        keyword=keyword,
        category_id=category_id,
        brand=brand,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        sort_by=sort_by,
        order=order,
        page=page,
        size=size,
    )
