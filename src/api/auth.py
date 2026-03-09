

from fastapi import APIRouter, HTTPException, Response

from src.services.auth import AuthService
from src.database import async_session_maker
from src.schemas.users import UserRequest, UserAdd
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign_up")
async def sign_up(
        data: UserRequest,
):
    hashed_password = AuthService().hash_password(data.password)
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


@router.post("/sign_in")
async def sign_in(
        data: UserRequest,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect email")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}



