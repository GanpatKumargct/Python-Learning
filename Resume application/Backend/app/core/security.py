from jose import jwt, JWTError

from datetime import datetime, timedelta, timezone
from app.core.config import settings
from typing import Optional



def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user_id), "role": role, "type": "access", "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "access":
            return None
        return payload
    except JWTError:
        return None

def decode_refresh_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            return None
        return payload
    except JWTError:
        return None
