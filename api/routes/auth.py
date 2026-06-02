from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from typing import Optional
import secrets

# Import schemas
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from schemas.auth import (
    Token, 
    LoginRequest, 
    LoginResponse,
    AdminLogin, 
    AdminResponse,
    LogoutResponse
)

router = APIRouter()

# Security
SECRET_KEY = "your-secret-key-change-in-production-12345"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# In-memory user database
USERS_DB = {
    "admin1": {
        "username": "admin1",
        "password": "admin123",
        "role": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User"
    },
    "user1": {
        "username": "user1",
        "password": "user123",
        "role": "user",
        "email": "user@example.com",
        "full_name": "Regular User"
    }
}

# Active tokens storage
active_tokens = {}

# Helper functions
def verify_password(plain_password: str, stored_password: str) -> bool:
    """Verify password (simple comparison - use hashing in production)"""
    return plain_password == stored_password

def create_access_token(username: str) -> str:
    """Create a new access token"""
    token = secrets.token_urlsafe(32)
    active_tokens[token] = {
        "username": username,
        "created_at": datetime.utcnow()
    }
    return token

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Get current user from token"""
    if token not in active_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    username = active_tokens[token]["username"]
    if username not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return USERS_DB[username]

def get_current_active_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Get current active user"""
    if current_user.get("disabled", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

# ==========================================
#  ROUTES
# ==========================================

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint - OAuth2 compatible
    Accepts: username and password (form data)
    Returns: JWT token
    """
    print(f"[AUTH] Login attempt - Username: {form_data.username}")
    
    # Check if user exists
    if form_data.username not in USERS_DB:
        print(f"[AUTH] User not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    user = USERS_DB[form_data.username]
    
    # Verify password
    if not verify_password(form_data.password, user["password"]):
        print(f"[AUTH] Invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Create token
    access_token = create_access_token(form_data.username)
    
    print(f"[AUTH] Login successful - User: {form_data.username}, Token: {access_token[:10]}...")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/admin/login", response_model=AdminResponse)
async def admin_login(login_data: AdminLogin):
    """
    Admin login endpoint (JSON body)
    """
    if login_data.username not in USERS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    user = USERS_DB[login_data.username]
    
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return {
        "username": user["username"],
        "role": user["role"],
        "message": "Admin login successful"
    }

@router.post("/logout", response_model=LogoutResponse)
async def logout(current_user: dict = Depends(get_current_active_user)):
    """
    Logout endpoint
    Invalidates the current token
    """
    print(f"[AUTH] Logout - User: {current_user['username']}")
    
    # Note: In production, you'd remove the token from active_tokens
    # For now, we just return success
    
    return {
        "status": "success",
        "message": "Successfully logged out"
    }

@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_active_user)):
    """
    Get current user information
    """
    return {
        "username": current_user["username"],
        "email": current_user.get("email"),
        "full_name": current_user.get("full_name"),
        "role": current_user.get("role", "user")
    }

@router.get("/verify")
async def verify_token(current_user: dict = Depends(get_current_active_user)):
    """
    Verify if current token is valid
    """
    return {
        "status": "valid",
        "username": current_user["username"],
        "role": current_user.get("role", "user")
    }

@router.get("/users")
async def list_users(current_user: dict = Depends(get_current_active_user)):
    """
    List all users (admin only)
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    users = []
    for username, user_data in USERS_DB.items():
        users.append({
            "username": user_data["username"],
            "email": user_data.get("email"),
            "role": user_data.get("role", "user"),
            "full_name": user_data.get("full_name")
        })
    
    return users