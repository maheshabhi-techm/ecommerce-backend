from src.models.category import Category
from src.models.product import Product
from src.models.product_status import ProductStatus
from src.models.product_image import ProductImage
from src.utils.sku import generate_sku
from fastapi import HTTPException
import src.services.product_image_service as product_image_service


def create_product(request, db, current_user):
    category_exist = (
        db.query(Category)
        .filter(Category.id == request.category_id, Category.is_active == True)
        .first()
    )

    if not category_exist:
        raise HTTPException(status_code=400, detail="Category not found")

    if request.discount_price and request.discount_price > request.price:
        raise HTTPException(
            status_code=400, detail="Discount price should not exceed price"
        )

    product = Product(
        seller_id=current_user["user_id"],
        category_id=request.category_id,
        name=request.name,
        description=request.description,
        brand=request.brand,
        price=request.price,
        discount_price=request.discount_price,
        stock_quantity=request.stock_quantity,
        sku=generate_sku(request.name),
        status=ProductStatus.PENDING,
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all_procuts(db):
    products = db.query(Product).all()

    if len(products) < 0:
        raise HTTPException(status_code=400, detail="No products found")

    return products


def get_product_by_id(id, db):
    db_product = db.query(Product).filter(Product.id == id).first()

    if not db_product:
        raise HTTPException(status_code=400, detail="No product found")

    return db_product


def update_product(id, request, db, current_user):
    db_product = (
        db.query(Product)
        .filter(Product.id == id, Product.seller_id == current_user["user_id"])
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=400,
            detail="Product not found or You do not have permission to update it",
        )

    # Only get the fields sent by the client
    update_data = request.model_dump(exclude_unset=True)

    # update the product
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)

    return db_product


def delete_product(id, db, current_user):
    db_product = (
        db.query(Product)
        .filter(Product.id == id, Product.seller_id == current_user["user_id"])
        .first()
    )

    if not db_product:
        raise HTTPException(
            status_code=400,
            detail="Product not found or You do not have permission to delete it",
        )

    db.delete(db_product)
    db.commit()

    return {"message": "Product deleted successfully!"}


async def upload_product_image(product_id, image, db, current_user):
    db_product = db.query(Product).filter(Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail=" Product not found")

    if db_product.seller_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    ALLOWED_TYPES = ["image/jpeg", "image/jpg", "image/webp"]

    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported image format")

    MAX_SIZE = 5 * 1024 * 1024  # 5MB

    content = await image.read()

    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail=" Image exceeds 5 MB")

    await image.seek(0)

    image_url = product_image_service.upload_product_image_to_cloud(image, product_id)

    product_image = ProductImage(
        product_id=product_id, image_url=image_url, is_primary=False
    )

    db.add(product_image)
    db.commit()
    db.refresh(product_image)

    return product_image
