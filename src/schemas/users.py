from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: str

class UserWithHashedPassword(User):
    hashed_password: str
