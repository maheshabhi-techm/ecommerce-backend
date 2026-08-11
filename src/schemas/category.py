from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    parent_id: int | None = None

class CategoryUpdate(BaseModel):
    name: str
    description: str | None = None
    parent_id: str | None = None
    is_active: bool | None = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    parent_id: int | None
    is_active: bool

    class Config:
        from_attributes = True