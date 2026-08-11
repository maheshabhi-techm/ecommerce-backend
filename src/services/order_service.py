from src.models.cart import Cart
from src.models.orders import Order
from src.models.order_item import OrderItem
from fastapi import HTTPException
from src.utils.order_number import generate_order_number


def get_orders(db, current_user):
    orders = db.query(Order).filter(Order.user_id == current_user["user_id"]).all()

    if not orders:
        raise HTTPException(status_code=404, detail="No orders found")

    result = []

    for order in orders:
        items = []

        for item in order.items:
            items.append(
                {
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "subtotal": item.subtotal,
                }
            )

        result.append(
            {
                "order_id": order.id,
                "order_number": order.order_number,
                "total_amount": order.total_amount,
                "order_status": order.order_status,
                "payment_status": order.payment_status,
                "payment_method": order.payment_method,
                "items": items,
            }
        )

    return result


def order_checkout(request, db, current_user):

    cart_items = db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    for item in cart_items:
        if item.quantity > item.product.stock_quantity:
            raise HTTPException(
                status_code=400, detail=f"{item.product.name} is out of stock"
            )

    total = 0

    for item in cart_items:
        price = (
            item.product.discount_price
            if item.product.discount_price
            else item.product.price
        )

        total += price * item.quantity

    order = Order(
        order_number=generate_order_number(),
        user_id=current_user["user_id"],
        address_id=request.address_id,
        total_amount=total,
        payment_method=request.payment_method,
    )

    db.add(order)
    db.flush()

    for item in cart_items:
        price = (
            item.product.discount_price
            if item.product.discount_price
            else item.product.price
        )

        db.add(
            OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                seller_id=item.product.seller_id,
                quantity=item.quantity,
                price=price,
                subtotal=price * item.quantity,
            )
        )

    item.product.stock_quantity -= item.quantity

    db.query(Cart).filter(Cart.user_id == current_user["user_id"]).delete()

    db.commit()
    db.refresh(order)
    return order
