from pydantic import BaseModel, Field, EmailStr

class AuthCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=1, max_length=20)
    email: EmailStr
    phone_number : str | None = None
    password: str = Field(min_length=8, max_length=20)
    is_active: bool = False

class AuthLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)
    
class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str
    
class ResendOTPRequest(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

class ProfileUpdate(BaseModel):
    name: str
    