from src.models.product import Product
from src.models.cart import Cart
from src.models.product_status import ProductStatus
from fastapi import HTTPException


def add_to_cart(request, db, current_user):
    db_product = (
        db.query(Product)
        .filter(
            Product.id == request.product_id,
            Product.status == ProductStatus.APPROVED,
            Product.is_active == True,
        )
        .first()
    )

    if not db_product:
        raise HTTPException(status_code=400, detail="Product not found")

    if request.quantity > db_product.stock_quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart_item = (
        db.query(Cart)
        .filter(
            Cart.product_id == request.product_id,
            Cart.user_id == current_user["user_id"],
        )
        .first()
    )

    if cart_item:
        cart_item.quantity += request.quantity

    else:
        cart_item = Cart(
            user_id=current_user["user_id"],
            product_id=request.product_id,
            quantity=request.quantity,
        )
        db.add(cart_item)

    db.commit()

    return {"message": "The product has been added to the cart"}


def get_cart_details(db, current_user):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()

    if len(cart_items) == 0:
        raise HTTPException(status_code=400, detail="Cart is empty")

    items = []
    grand_total = 0

    for cart in cart_items:
        subtotal = cart.quantity * cart.product.price

        items.append(
            {
                "product_id": cart.product.id,
                "name": cart.product.name,
                "quantity": cart.quantity,
                "price": cart.product.price,
                "subtotal": subtotal,
            }
        )

        grand_total += subtotal

    return {"items": items, "grand_total": grand_total}


def update_cart(id, request, db, current_user):
    cart_exist = (
        db.query(Cart)
        .filter(Cart.id == id, Cart.user_id == current_user["user_id"])
        .first()
    )

    if not cart_exist:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if request.quantity > cart_exist.product.stock_quantity:
        raise HTTPException(status_code=409, detail="Insufficient stock")

    cart_exist.quantity = request.quantity

    db.commit()
    db.refresh(cart_exist)

    return {
        "message": "Cart updated successfully",
        "cart_id": cart_exist.id,
        "quantity": cart_exist.quantity,
    }


def delete_cart_by_id(id, db, current_user):
    cart_exist = (
        db.query(Cart)
        .filter(Cart.id == id, Cart.user_id == current_user["user_id"])
        .first()
    )

    if not cart_exist:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_exist)
    db.commit()

    return {"message": "Item has been deleted from the cart successfully!"}


def clear_cart(db, current_user):
    cart_items = db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is already empty")

    for item in cart_items:
        db.delete(item)

    db.commit()
    return {"message": "Cart cleared successfully!"}
