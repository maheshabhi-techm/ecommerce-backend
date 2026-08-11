from fastapi import Depends, APIRouter
from src.dependencies.auth import get_current_user
from src.database import get_db
from src.schemas.auth import ProfileUpdate
from src.schemas.address import AddressCreate
from src.services.profile_service import (
    get_user_details,
    update_user_details,
    add_user_address,
    get_user_address,
    set_user_default_address,
    delete_user_address,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/profile")
def get_profile(current_user=Depends(get_current_user), db=Depends(get_db)):
    return get_user_details(current_user, db)


@router.put("/profile")
def update_profile(
    request: ProfileUpdate, db=Depends(get_db), current_user=Depends(get_current_user)
):
    return update_user_details(request, db, current_user)


@router.post("/addresses")
def add_address(
    request: AddressCreate, db=Depends(get_db), current_user=Depends(get_current_user)
):
    return add_user_address(request, db, current_user)


@router.get("/addresses")
def get_address(current_user=Depends(get_current_user), db=Depends(get_db)):
    return get_user_address(current_user, db)


@router.put("/addresss/{id}/default")
def set_default_address(
    id: int, current_user=Depends(get_current_user), db=Depends(get_db)
):
    return set_user_default_address(id, current_user, db)


@router.delete("/address/{id}")
def delete_address(id: int, current_user=Depends(get_current_user), db=Depends(get_db)):
    return delete_user_address(id, current_user, db)
