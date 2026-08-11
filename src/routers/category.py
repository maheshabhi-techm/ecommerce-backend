from fastapi import APIRouter, Depends
from src.database import get_db
from src.dependencies.role import require_roles
from src.models.user import UserRole
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from src.dependencies.auth import get_current_user
import src.services.category_service as category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse)
def create_category_api(
    request: CategoryCreate,
    db=Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN)),
):
    return category_service.create_category(request, db)


@router.get("", response_model=list[CategoryResponse])
def get_categories_api(db=Depends(get_db)):
    return category_service.get_categories(db)


@router.put("/{id}", response_model=CategoryResponse)
def update_category_api(
    id: int,
    request: CategoryUpdate,
    db=Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN.value)),
):
    return category_service.update_category(id, request, db)


@router.delete("/{id}")
def delete_category_api(
    id: int,
    db=Depends(get_db),
    current_user=Depends(require_roles(UserRole.ADMIN.value)),
):
    return category_service.delete_category(id, db)
