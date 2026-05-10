from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.auth import schemas, service

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

@router.post("/candidate/send-otp", status_code=status.HTTP_200_OK)
async def send_candidate_otp(
    payload: schemas.SendOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    await service.generate_and_send_otp(db, payload.email, payload.purpose)
    return {"message": "OTP sent successfully"}

@router.post("/candidate/verify-otp", response_model=schemas.CandidateOTPVerifyResponse)
async def verify_candidate_otp(
    payload: schemas.VerifyOTPRequest,
    db: AsyncSession = Depends(get_db)
):
    return await service.verify_candidate_otp(db, payload.email, payload.otp)
