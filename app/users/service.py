# app/users/service.py
from __future__ import annotations  # <-- evita evaluar anotaciones en tiempo de carga

from sqlalchemy.ext.asyncio import AsyncSession
from app.users.repository import get_by_username, get_by_email, create_user
from app.core.security import hash_password, create_access_token, verify_password
from app.users.schemas import UserCreate  # <-- IMPORT NECESARIO
# si usas perfil al registrar:
try:
    from app.profile.service import ensure_profile
except Exception:
    ensure_profile = None  # opcional si aún no tienes el módulo profile


async def register_user(db: AsyncSession, data: UserCreate) -> str:
    if await get_by_username(db, data.username):
        raise ValueError("username already exists")
    if await get_by_email(db, data.email):
        raise ValueError("email already exists")

    hashed = hash_password(data.password)
    user = await create_user(db, data.username, data.email, hashed)

    # crea perfil asociado si está disponible el módulo profile
    if ensure_profile is not None:
        await ensure_profile(db, user.id, birth_date=getattr(data, "birth_date", None), sex=getattr(data, "sex", None))

    token = create_access_token(sub=str(user.id))
    return token


async def authenticate_user(db: AsyncSession, username_or_email: str, password: str):
    # Permite login con usuario o email
    user = await get_by_username(db, username_or_email)
    if not user and "@" in username_or_email:
        user = await get_by_email(db, username_or_email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def login_user(db: AsyncSession, username_or_email: str, password: str) -> str:
    user = await authenticate_user(db, username_or_email, password)
    if not user:
        raise ValueError("invalid credentials")
    return create_access_token(sub=str(user.id))
