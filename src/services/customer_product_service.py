from src.models.product import Product
from sqlalchemy import asc, desc, or_
from fastapi import HTTPException
from src.models.product_status import ProductStatus
import math


def get_all_products(
    db,
    keyword=None,
    category_id=None,
    brand=None,
    min_price=None,
    max_price=None,
    in_stock=None,
    sort_by="created_at",
    order="desc",
    page=1,
    size=10,
):

    page = max(1, int(page or 1))
    size = max(1, int(size or 10))

    query = db.query(Product).filter(
        Product.status == ProductStatus.APPROVED, Product.is_active == True
    )

    if keyword:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{keyword}%"),
                Product.description.ilike(f"%{keyword}%"),
                Product.brand.ilike(f"%{keyword}%"),
            )
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if brand:
        query = query.filter(Product.brand.ilike(f"%{brand}%"))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if in_stock:
        query = query.filter(Product.stock_quantity > 0)

    if sort_by == "price":
        query = query.order_by(
            asc(Product.price) if order == "asc" else desc(Product.price)
        )

    elif sort_by == "name":
        query = query.order_by(
            asc(Product.name) if order == "asc" else desc(Product.name)
        )

    else:
        query = query.order_by(
            asc(Product.created_at) if order == "asc" else desc(Product.created_at)
        )

    total = query.count()

    products = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": products,
        "page": page,
        "size": size,
        "total": total,
        "total_pages": math.ceil(total / size) if total else 0,
    }


def get_product(id, db):
    db_product = (
        db.query(Product)
        .filter(
            Product.id == id,
            Product.status == ProductStatus.APPROVED,
            Product.is_active == True,
        )
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=400, detail="Product not found")

    return db_product
