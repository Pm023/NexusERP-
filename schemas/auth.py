from pydantic import BaseModel, EmailStr
from typing import Optional

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User schemas
class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[int] = None
    disabled: Optional[bool] = False
    role: Optional[str] = "user"

    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str

# Login schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    username: str
    role: Optional[str] = "user"

# Admin schemas
class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    username: str
    role: str
    message: str

# Logout schema
class LogoutResponse(BaseModel):
    status: str
    message: str