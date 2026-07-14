from fastapi import APIRouter

from app.schemas.user import UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter()


@router.get("", response_model=list[UserOut])
def list_users() -> list[UserOut]:
    return UserService.list_users()


@router.post("", response_model=UserOut)
def create_user(payload: UserCreate) -> UserOut:
    return UserService.create_user(payload)
