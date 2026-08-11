from src.models.orders import Order
from src.models.payment import Payment, PaymentStatus
from src.models.order_status import OrderStatus, PaymentStatus as OrderPaymentStatus
from fastapi import HTTPException
from src.security.razorpay import client


def create_payment_order(request, db, current_user):
    order = (
        db.query(Order)
        .filter(Order.id == request.order_id, Order.user_id == current_user["user_id"])
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.payment_status == OrderPaymentStatus.SUCCESS:
        raise HTTPException(status_code=400, detail="Order is already paid")

    if order.payment_method != "RAZORPAY":
        raise HTTPException(
            status_code=400,
            detail="Payment method is not Razorpay for this order",
        )

    amount = int(order.total_amount * 100)  # Razorpay expects a amout in paise

    razorpay_order = client.order.create(
        {"amount": amount, "currency": "INR", "payment_capture": 1}
    )

    payment = (
        db.query(Payment)
        .filter(Payment.order_id == order.id, Payment.status == PaymentStatus.CREATED)
        .order_by(Payment.id.desc())
        .first()
    )

    if payment:
        payment.transaction_id = razorpay_order["id"]
        payment.amount = order.total_amount
    else:
        payment = Payment(
            order_id=order.id,
            transaction_id=razorpay_order["id"],
            amount=order.total_amount,
            status=PaymentStatus.CREATED,
        )
        db.add(payment)

    db.commit()
    db.refresh(payment)

    return {
        "order_id": order.id,
        "payment_id": payment.id,
        "razorpay_order_id": razorpay_order["id"],
        "amount": order.total_amount,
    }


def verify_payment(request, db, current_user):
    params = {
        "razorpay_order_id": request.razorpay_order_id,
        "razorpay_payment_id": request.razorpay_payment_id,
        "razorpay_signature": request.razorpay_signature,
    }

    try:
        client.utility.verify_payment_signature(params)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid payment signature") from exc

    payment = (
        db.query(Payment)
        .join(Order, Order.id == Payment.order_id)
        .filter(
            Payment.transaction_id == request.razorpay_order_id,
            Payment.order_id == request.order_id,
            Order.user_id == current_user["user_id"],
        )
        .first()
    )

    if not payment:
        raise HTTPException(status_code=404, detail="Payment order not found")

    payment.gateway_payment_id = request.razorpay_payment_id
    payment.status = PaymentStatus.SUCCESS

    order = db.query(Order).filter(Order.id == payment.order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.payment_status = OrderPaymentStatus.SUCCESS
    order.order_status = OrderStatus.PAID

    db.commit()

    return {"success": True, "message": "Payment successful"}


def mark_payment_failure(request, db, current_user):
    payment = (
        db.query(Payment)
        .join(Order, Order.id == Payment.order_id)
        .filter(
            Payment.transaction_id == request.razorpay_order_id,
            Payment.order_id == request.order_id,
            Order.user_id == current_user["user_id"],
        )
        .first()
    )

    if not payment:
        return {"success": False, "message": "Payment record not found"}

    payment.status = PaymentStatus.FAILED
    payment.gateway_payment_id = request.razorpay_payment_id

    order = db.query(Order).filter(Order.id == request.order_id).first()
    if order and order.payment_status != OrderPaymentStatus.SUCCESS:
        order.payment_status = OrderPaymentStatus.FAILED

    db.commit()

    return {"success": True, "message": "Payment marked as failed"}


async def payment_webhook(db, request):
    payload = await request.json()

    event = payload["event"]

    if event == "payment.captured":
        payment_id = payload["payload"]["payment"]["entity"]["id"]

        payment = db.query(Payment).filter(Payment.gateway_payment_id == payment_id).first()

        if payment:
            payment.status = PaymentStatus.SUCCESS
            order = db.query(Order).filter(Order.id == payment.order_id).first()

            if order:
                order.payment_status = OrderPaymentStatus.SUCCESS
                order.order_status = OrderStatus.PAID

            db.commit()

    return {
        "status": "received"
    }


