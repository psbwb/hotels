from typing import Annotated

from fastapi import Query, Depends, Request, HTTPException
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page:   Annotated[
        int | None,
        Query(1, ge=1)
    ]
    per_page: Annotated[
        int | None,
        Query(None, ge=1, le=30)
    ]

PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) ->  str:
    token = request.cookies.get("access_token", None)
    if token is None:
        raise HTTPException(status_code=401, detail="No token provided")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data["user_id"]


UserDep = Annotated[int, Depends(get_current_user_id)]
