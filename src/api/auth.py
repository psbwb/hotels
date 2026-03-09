from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/sign_up")
async def sign_up(
        data: UserRequestAdd,
):

    hashed_password = pwd_context.hash(data.password[:10])
    new_user_data = UserAdd(
        email=data.email,
        hashed_password=hashed_password
    )
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {
        "status": "OK",
        "message": "User created successfully",
    }