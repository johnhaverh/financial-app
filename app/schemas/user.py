# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr | None = None
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class User(UserBase):
    disabled: bool | None = None

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str