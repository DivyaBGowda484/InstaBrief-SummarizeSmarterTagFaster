from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from config.settings import settings
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.services.storage import StorageService


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes or settings.access_token_expire_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


auth_scheme = HTTPBearer(auto_error=False)
storage_singleton = StorageService()


async def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(auth_scheme)):
    if not creds or not creds.scheme.lower() == 'bearer':
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = creds.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await storage_singleton.db.users.find_one({"_id": __import__('bson').ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": user_id, "email": user.get('email')}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


