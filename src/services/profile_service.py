from src.models.user import User
from src.models.address import Address
from fastapi import HTTPException


def _split_name(full_name: str, fallback_last_name: str) -> tuple[str, str]:
    cleaned = full_name.strip()

    if not cleaned:
        return "", fallback_last_name

    parts = cleaned.split()

    if len(parts) == 1:
        return parts[0], fallback_last_name

    return parts[0], " ".join(parts[1:])


def get_user_details(current_user, db):
    return db.query(User).filter(User.id == current_user["user_id"]).first()


def update_user_details(request, db, current_user):
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    first_name, last_name = _split_name(request.name, db_user.last_name)

    if not first_name:
        raise HTTPException(status_code=400, detail="Name is required")

    db_user.first_name = first_name
    db_user.last_name = last_name
    db.commit()
    db.refresh(db_user)
    return db_user


def add_user_address(request, db, current_user):
    address = Address(user_id=current_user["user_id"], **request.model_dump())

    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_user_address(current_user, db):
    return (
        db.query(Address)
        .filter(Address.user_id == current_user["user_id"])
        .order_by(Address.id.desc())
        .all()
    )


def update_address(id, request, current_user, db):
    address = (
        db.query(Address)
        .filter(
            Address.id == id,
            Address.user_id == current_user["user_id"],
        )
        .first()
    )

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    for key, value in request.model_dump().items():
        setattr(address, key, value)

    db.commit()
    db.refresh(address)

    return address


def set_user_default_address(id, current_user, db):
    db.query(Address).filter(Address.user_id == current_user["user_id"]).update(
        {"is_default": False}
    )
    address = (
        db.query(Address)
        .filter(Address.id == id, Address.user_id == current_user["user_id"])
        .first()
    )

    if not address:
        raise HTTPException(status_code=400, detail="Address not found")

    address.is_default = True
    db.commit()

    return {"message": "Default address updated"}


def delete_user_address(id, current_user, db):
    address = (
        db.query(Address)
        .filter(
            Address.id == id,
            Address.user_id == current_user["user_id"],
        )
        .first()
    )

    if not address:
        raise HTTPException(status_code=400, detail="Address not found")

    db.delete(address)
    db.commit()

    return {"message": "Address deleted successfully!"}
