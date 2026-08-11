from uuid import uuid4


def generate_order_number():
    return "ORD-" + uuid4().hex[:10].upper()
