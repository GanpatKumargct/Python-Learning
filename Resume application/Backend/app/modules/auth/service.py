import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token, hash_password
from app.modules.auth.models import User, RefreshToken, AuthOTP
from app.modules.ats.candidates.models import Candidate

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user or not user.password_hash:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def create_tokens_for_user(db: AsyncSession, user: User) -> dict:
    access_token = create_access_token(user_id=str(user.id), role=user.role.value if hasattr(user.role, 'value') else user.role)
    refresh_token = create_refresh_token(user_id=str(user.id))
    
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=hashlib.sha256(refresh_token.encode('utf-8')).hexdigest(),
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(db_refresh_token)
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def refresh_access_token(db: AsyncSession, refresh_token: str) -> dict:
    payload = decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = await get_user_by_id(db, user_id)
    
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        
    return await create_tokens_for_user(db, user)

async def generate_and_send_otp(db: AsyncSession, email: str, purpose: str) -> None:
    otp = "".join([str(secrets.randbelow(10)) for _ in range(6)])
    otp_hash = hash_password(otp)
    
    db_otp = AuthOTP(
        email=email,
        otp_hash=otp_hash,
        purpose=purpose,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
    )
    db.add(db_otp)
    await db.commit()
    
    # In a real app, this sends an email via Celery
    print(f"=========================================")
    print(f"DEBUG: OTP for {email} is {otp}")
    print(f"=========================================")

async def verify_otp(db: AsyncSession, email: str, otp: str, purpose: str) -> AuthOTP:
    result = await db.execute(
        select(AuthOTP)
        .where(AuthOTP.email == email, AuthOTP.purpose == purpose, AuthOTP.used_at == None)
        .order_by(AuthOTP.created_at.desc())
    )
    db_otp = result.scalars().first()
    
    if not db_otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
    
    if db_otp.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired")
        
    if not verify_password(otp, db_otp.otp_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
        
    db_otp.used_at = datetime.now(timezone.utc)
    await db.commit()
    
    return db_otp

async def verify_candidate_otp(db: AsyncSession, email: str, otp: str) -> dict:
    await verify_otp(db, email, otp, purpose="magic_link")
    
    result = await db.execute(select(Candidate).where(Candidate.email == email))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        candidate = Candidate(email=email, full_name="Candidate")
        db.add(candidate)
        await db.commit()
        await db.refresh(candidate)
        
    access_token = create_access_token(user_id=str(candidate.id), role="candidate")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
