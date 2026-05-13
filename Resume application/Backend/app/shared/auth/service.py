import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
import httpx
from app.core.config import settings
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_refresh_token, hash_password
from app.shared.auth.models import User, RefreshToken, AuthOTP
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

async def get_zoho_user_info(code: str) -> dict:
    if not settings.ZOHO_CLIENT_ID or not settings.ZOHO_CLIENT_SECRET:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Zoho SSO not configured")
        
    async with httpx.AsyncClient() as client:
        # Exchange authorization code for access token
        response = await client.post(
            "https://accounts.zoho.com/oauth/v2/token",
            data={
                "grant_type": "authorization_code",
                "client_id": settings.ZOHO_CLIENT_ID,
                "client_secret": settings.ZOHO_CLIENT_SECRET,
                "redirect_uri": settings.ZOHO_REDIRECT_URI,
                "code": code
            }
        )
        token_data = response.json()
        if "access_token" not in token_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve access token from Zoho")
            
        access_token = token_data["access_token"]
        
        # Fetch user info using Zoho's OAuth API
        user_response = await client.get(
            "https://accounts.zoho.com/oauth/user/info",
            headers={"Authorization": f"Zoho-oauthtoken {access_token}"}
        )
        user_data = user_response.json()
        return user_data

async def handle_zoho_callback(db: AsyncSession, code: str) -> dict:
    user_info = await get_zoho_user_info(code)
    email = user_info.get("Email")
    
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No email associated with this Zoho account")
        
    user = await get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Your Zoho account is not authorized for this ERP. Please contact an Administrator to be invited."
        )
        
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Your account is inactive.")
        
    return await create_tokens_for_user(db, user)

async def generate_and_send_magic_link(db: AsyncSession, email: str, purpose: str = "magic_link") -> None:
    token = secrets.token_urlsafe(32)
    token_hash = hash_password(token)
    
    db_otp = AuthOTP(
        email=email,
        otp_hash=token_hash,
        purpose=purpose,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=15)
    )
    db.add(db_otp)
    await db.commit()
    
    # In a real app, this sends an email via Celery, but we use the global email module
    from app.core.email import send_email
    subject = "Login to Your Account"
    
    # Using a standard localhost frontend URL for dev. In prod, this should come from settings.
    frontend_url = "http://localhost:5173"
    magic_link = f"{frontend_url}/verify?token={token}&email={email}"
    
    body_html = f\"\"\"
    <h3>Login to Your Account</h3>
    <p>Click the secure link below to log in. This link will expire in 15 minutes.</p>
    <a href="{magic_link}" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">Login Now</a>
    <p>If the button doesn't work, copy and paste this URL into your browser:</p>
    <p><a href="{magic_link}">{magic_link}</a></p>
    \"\"\"
    await send_email(email, subject, body_html)

async def verify_magic_link(db: AsyncSession, email: str, token: str, purpose: str = "magic_link") -> AuthOTP:
    result = await db.execute(
        select(AuthOTP)
        .where(AuthOTP.email == email, AuthOTP.purpose == purpose, AuthOTP.used_at == None)
        .order_by(AuthOTP.created_at.desc())
    )
    db_otp = result.scalars().first()
    
    if not db_otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired magic link")
    
    if db_otp.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Magic link expired")
        
    if not verify_password(token, db_otp.otp_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid magic link")
        
    db_otp.used_at = datetime.now(timezone.utc)
    await db.commit()
    
    return db_otp

async def verify_candidate_magic_link(db: AsyncSession, email: str, token: str) -> dict:
    await verify_magic_link(db, email, token, purpose="magic_link")
    
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
