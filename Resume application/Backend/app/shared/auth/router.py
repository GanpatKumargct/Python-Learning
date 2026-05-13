from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.config import settings
from app.shared.auth import schemas, service

router = APIRouter()

@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    payload: schemas.LoginRequest, 
    db: AsyncSession = Depends(get_db)
):
    user = await service.authenticate_user(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return await service.create_tokens_for_user(db, user)

@router.post("/refresh", response_model=schemas.TokenResponse)
async def refresh_token(
    payload: schemas.RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    return await service.refresh_access_token(db, payload.refresh_token)

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

@router.get("/zoho/callback", response_model=schemas.TokenResponse)
async def zoho_callback(
    code: str,
    db: AsyncSession = Depends(get_db)
):
    return await service.handle_zoho_callback(db, code)

@router.post("/candidate/send-magic-link", status_code=status.HTTP_200_OK)
async def send_candidate_magic_link(
    payload: schemas.SendMagicLinkRequest,
    db: AsyncSession = Depends(get_db)
):
    await service.generate_and_send_magic_link(db, payload.email, payload.purpose)
    return {"message": "Magic link sent successfully"}

@router.post("/candidate/verify-magic-link", response_model=schemas.CandidateMagicLinkVerifyResponse)
async def verify_candidate_magic_link(
    payload: schemas.VerifyMagicLinkRequest,
    db: AsyncSession = Depends(get_db)
):
    return await service.verify_candidate_magic_link(db, payload.email, payload.token)
