# app/profile/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.profile.repository import get_by_user_id, create_profile

async def ensure_profile(db: AsyncSession, user_id: int, *, birth_date=None, sex=None):
    prof = await get_by_user_id(db, user_id)
    if prof:
        # si ya existe, no lo toques (o actualiza si te conviene)
        return prof
    return await create_profile(db, user_id, birth_date=birth_date, sex=sex)
