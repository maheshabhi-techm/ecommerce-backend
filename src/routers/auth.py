from fastapi import APIRouter, Depends, HTTPException
from src.database import get_db
from src.schemas.auth import (
    AuthCreate,
    AuthLogin,
    VerifyOTPRequest,
    ResendOTPRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from src.services.auth_service import (
    register,
    login,
    verify_email,
    resend_otp,
    forgot_password,
    reset_password,
    get_token_form_data,
)
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def auth_register(request: AuthCreate, db=Depends(get_db)):
    return await register(request, db)


@router.post("/login")
async def auth_login(request: AuthLogin, db=Depends(get_db)):
    return await login(request, db)


@router.post("/verify-email")
async def verifyEmail(request: VerifyOTPRequest, db=Depends(get_db)):
    return await verify_email(request, db)


@router.post("/resend-otp")
async def resendOTP(request: ResendOTPRequest, db=Depends(get_db)):
    return await resend_otp(request, db)


@router.post("/forgot-password")
async def forgotPassword(request: ForgotPasswordRequest, db=Depends(get_db)):
    return await forgot_password(request, db)


@router.post("/reset-password")
async def resetPassword(request: ResetPasswordRequest, db=Depends(get_db)):
    return await reset_password(request, db)


@router.post("/token")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)
):
    return await get_token_form_data(form_data, db)
