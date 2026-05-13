from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.config import settings
from app.shared.auth import schemas, service

router = APIRouter()

# Refresh access token using refresh token (Any user with valid refresh token)
@router.post("/refresh", response_model=schemas.TokenResponse)
async def refresh_token(
    payload: schemas.RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    return await service.refresh_access_token(db, payload.refresh_token)

# Redirect to Zoho SSO login (Public)
@router.get("/zoho/login")
async def zoho_login():
    if not settings.ZOHO_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Zoho SSO not configured")
        
    zoho_auth_url = (
        "https://accounts.zoho.com/oauth/v2/auth?"
        "response_type=code&"
        f"client_id={settings.ZOHO_CLIENT_ID}&"
        "scope=AaaServer.profile.READ&"
        f"redirect_uri={settings.ZOHO_REDIRECT_URI}&"
        "access_type=online"
    )
    return RedirectResponse(zoho_auth_url)

# Handle callback from Zoho SSO and generate token (Public)
@router.get("/zoho/callback")
async def zoho_callback(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    tokens = await service.handle_zoho_callback(db, code)
    # Redirect to frontend with token
    redirect_url = f"{settings.FRONTEND_URL}/login/success?token={tokens['access_token']}"
    return RedirectResponse(redirect_url)

# Send OTP to candidate's email for passwordless login (Public)
@router.post("/candidate/send-otp", status_code=status.HTTP_200_OK)
async def send_candidate_otp(
    payload: schemas.SendOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    await service.generate_and_send_otp(db, payload.email, payload.purpose)
    return {"message": "OTP sent successfully"}

# Verify candidate's OTP and generate access token (Public)
@router.post("/candidate/verify-otp", response_model=schemas.CandidateOTPVerifyResponse)
async def verify_candidate_otp(
    payload: schemas.VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    return await service.verify_candidate_otp(db, payload.email, payload.otp)
