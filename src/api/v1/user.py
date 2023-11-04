from fastapi import APIRouter

from src.db.db_setup import SessionLocal
from src.models.model import DBUser
from src.schemas.user import UserCreate
from src.schemas.response import UserResponse
from src.utils.utils_funcs import get_password_hash

router = APIRouter()


@router.post("/user/", response_model=UserResponse)
async def create_user(user: UserCreate):
    db = SessionLocal()
    hashed_password = get_password_hash(user.password)

    new_user = DBUser(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return UserResponse(id=new_user.id, username=new_user.username)
