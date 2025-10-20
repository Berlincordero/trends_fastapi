# app/users/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    birth_date: date | None = None
    sex: str | None = None  # "male" | "female" | "other" u otro catálogo

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
