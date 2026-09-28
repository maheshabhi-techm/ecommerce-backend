from fastapi import Depends, HTTPException
from ..database import get_db
from ..models import User, EmailOTP, OTPType, RefreshToken, UserRole
from ..utils.otp import generate_otp
from src.utils.emailService import send_otp, send_email
from datetime import datetime, UTC, timedelta
from src.security.auth import verify_password, hash_password
from src.services.jwt_service import create_access_token, create_refresh_token
from src.utils.token import hash_token
from src.security.config import settings


async def register(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if user_exist:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_number=request.phone_number,
        hashed_password=hash_password(request.password),
        role=UserRole.CUSTOMER,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    otp = generate_otp()

    otp_record = EmailOTP(
        user_id=new_user.id,
        otp=otp,
        otp_type=OTPType.EMAIL_VERIFICATION,
        expires_at=datetime.now() + timedelta(minutes=10),
    )

    db.add(otp_record)
    db.commit()

    await send_otp(request.email, otp)

    return {"message": "Registration successful. Verify your email."}


async def login(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if not user_exist:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(request.password, user_exist.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user_exist.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token = create_access_token(user_exist)

    refresh_token = create_refresh_token(user_exist.id)

    token_record = RefreshToken(
        user_id=user_exist.id,
        token_hash=hash_token(refresh_token),
        expires_at=datetime.now() + timedelta(days=7),
    )

    db.add(token_record)
    db.commit()

    return {
        "message": "Login successful!",
        "token_type": "bearer",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


async def verify_email(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if not user_exist:
        raise HTTPException(status_code=400, detail="User not found")

    otp = (
        db.query(EmailOTP)
        .filter(
            EmailOTP.user_id == user_exist.id,
            EmailOTP.otp == request.otp,
            EmailOTP.otp_type == OTPType.EMAIL_VERIFICATION,
            EmailOTP.is_used == False,
        )
        .first()
    )

    if otp is None:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp.expires_at < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="OTP expired")

    otp.is_used = True

    user_exist.is_verified = True

    db.commit()

    return {"message": "Email verified successfully!"}


async def resend_otp(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if not user_exist:
        return {
            "message": "If the account exists, a new verification code has been sent."
        }

    # Invalidate the unused otps
    db.query(EmailOTP).filter(
        EmailOTP.user_id == user_exist.id, EmailOTP.is_used == False
    ).update({"is_used": True})

    otp = generate_otp()

    record = EmailOTP(
        user_id=user_exist.id,
        otp=otp,
        otp_type=OTPType.EMAIL_VERIFICATION,
        expires_at=datetime.now() + timedelta(minutes=10),
    )

    db.add(record)
    db.commit()

    await send_otp(user_exist.email, otp)

    return {"message": "Verification code sent"}


async def forgot_password(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if not user_exist:
        raise HTTPException(status_code=400, detail="User doesn't exist")

    db.query(EmailOTP).filter(
        EmailOTP.user_id == user_exist.id,
        EmailOTP.otp_type == OTPType.PASSWORD_RESET,
        EmailOTP.is_used == False,
    ).update({"is_used": True})

    otp = generate_otp()

    otp_record = EmailOTP(
        user_id=user_exist.id,
        otp=otp,
        otp_type=OTPType.PASSWORD_RESET,
        expires_at=datetime.now() + timedelta(minutes=10),
    )

    db.add(otp_record)
    db.commit()

    await send_email(
        user_exist.email,
        "Reset Password",
        f"""
            <h2>Password Reset</h2>

            <h1>{otp}</h1>

            <p>This OTP expires in 10 minutes.</p>
        """,
    )
    return {"message": "A password reset code has been sent"}


async def reset_password(request, db):
    user_exist = db.query(User).filter(User.email == request.email).first()

    if not user_exist:
        raise HTTPException(status_code=400, detail="User doesn't exists")

    otp = (
        db.query(EmailOTP)
        .filter(
            EmailOTP.user_id == user_exist.id,
            EmailOTP.otp == request.otp,
            EmailOTP.otp_type == OTPType.PASSWORD_RESET,
            EmailOTP.is_used == False,
        )
        .first()
    )

    if otp is None:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="OTP expired")

    otp.is_used = True

    user_exist.hashed_password = hash_password(request.new_password)

    db.commit()

    return {"message": "Password updated successfully!"}


async def get_token_form_data(request, db):
    user_exist = db.query(User).filter(User.email == request.username).first()

    if not user_exist:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(request.password, user_exist.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not user_exist.is_verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    access_token = create_access_token(user_exist)

    return {"access_token": access_token, "token_type": "bearer"}
