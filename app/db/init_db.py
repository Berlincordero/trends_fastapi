# app/db/init_db.py
from app.db.session import engine
from app.db.base import Base
from app.users.models import User  # importa modelos
from app.profile.models import Profile  # 👈 importa para registro en metadata

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
