import os, uuid, shutil
from fastapi import UploadFile
from app.core.config import settings

def save_local(file: UploadFile, subdir: str = "avatars") -> str:
    base = settings.MEDIA_DIR
    os.makedirs(os.path.join(base, subdir), exist_ok=True)
    ext = os.path.splitext(file.filename or "")[1] or ".bin"
    rel = f"{subdir}/{uuid.uuid4().hex}{ext}"
    abs_path = os.path.join(base, rel)
    with open(abs_path, "wb") as out:
        shutil.copyfileobj(file.file, out)
    return rel
