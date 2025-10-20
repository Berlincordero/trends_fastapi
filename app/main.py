# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.limiter import init_limiter
from app.users.router import router as users_router

app = FastAPI(title="Trends API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# media local
os.makedirs(settings.MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=settings.MEDIA_DIR), name="media")

@app.on_event("startup")
async def on_startup():
    await init_limiter()

@app.get("/api/health/")
async def health():
    return {"ok": True, "service": "fastapi", "msg": "healthy"}

# Módulos
app.include_router(users_router)
