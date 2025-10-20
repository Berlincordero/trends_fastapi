# app/profile/router.py
from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.core.security import decode_access_token
from app.users.repository import get_by_id
from app.profile.repository import get_by_user_id
from app.profile.schemas import ProfileOut

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/me/", response_model=ProfileOut)
async def my_profile(
    db: AsyncSession = Depends(get_session),
    token: str | None = Query(None),
    authorization: str | None = Header(None),
):
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
    if not token:
        raise HTTPException(status_code=401, detail="missing token")

    try:
        user_id = int(decode_access_token(token))
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")

    user = await get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    prof = await get_by_user_id(db, user_id)
    if not prof:
        # si aún no existe, entregamos vacío con user_id
        return {"user_id": user_id, "birth_date": None, "sex": None, "avatar": None, "cover": None}
    return prof
