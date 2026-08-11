from pydantic import BaseModel

class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: str | None = None
    city: str
    state: str
    country: str
    postal_code: str

class AddressUpdate(AddressCreate):
    pass

class AddressResponse(AddressCreate):
    id: int
    is_default: bool

    class config:
        from_attributes: True