from uuid import uuid4


def generate_sku(prefix: str):
    return f"{prefix[:3].upper()}-" f"{uuid4().hex[:8].upper()}"
