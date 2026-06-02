"""
Authentication Utilities
"""

import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import Admin

# Configuration
SECRET_KEY = "unified_secret_key_2026"
ALGORITHM = "HS256"

# ==================== 3 ADMINS CREDENTIALS ====================
ADMIN_CREDENTIALS = {
    "admin1": {
        "username": "admin1",
        "password": "admin123",
        "email": "admin1@nexuserp.io",
        "full_name": "Admin One"
    },
    "admin2": {
        "username": "admin2",
        "password": "admin123",
        "email": "admin2@nexuserp.io",
        "full_name": "Admin Two"
    },
    "admin3": {
        "username": "admin3",
        "password": "admin123",
        "email": "admin3@nexuserp.io",
        "full_name": "Admin Three"
    }
}

security = HTTPBearer()

def create_token(admin_id: int, username: str) -> str:
    """Create JWT token"""
    payload = {
        "admin_id": admin_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Admin:
    """Get current authenticated admin"""
    token = credentials.credentials
    payload = verify_token(token)
    
    admin = db.query(Admin).filter(Admin.id == payload.get("admin_id")).first()
    
    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")
    
    return admin

def validate_credentials(username: str, password: str) -> dict:
    """Validate admin credentials"""
    if username in ADMIN_CREDENTIALS:
        admin_data = ADMIN_CREDENTIALS[username]
        if admin_data["password"] == password:
            return admin_data
    return None