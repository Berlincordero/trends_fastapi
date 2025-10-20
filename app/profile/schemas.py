# app/profile/schemas.py
from pydantic import BaseModel
from datetime import date

class ProfileOut(BaseModel):
    user_id: int
    birth_date: date | None = None
    sex: str | None = None
    avatar: str | None = None
    cover: str | None = None

    class Config:
        from_attributes = True
