from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.users.schemas import UserCreate, UserOut
from app.users import service as svc
from app.core.security import decode_access_token
from app.users.repository import get_by_id
from fastapi.security import OAuth2PasswordRequestForm  # <-- NUEVO

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register/")
async def register(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        token = await svc.register_user(db, payload)
        await db.commit()
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="internal error")

# ----- NUEVO -----
@router.post("/login/")
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """
    Acepta x-www-form-urlencoded con campos:
    - username
    - password
    (compatible con tu frontend)
    """
    try:
        token = await svc.login_user(db, form.username, form.password)
        await db.commit()
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        await db.rollback()
        raise HTTPException(status_code=401, detail="invalid credentials")
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="internal error")

@router.get("/me/", response_model=UserOut)
async def me(
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
    return user
 