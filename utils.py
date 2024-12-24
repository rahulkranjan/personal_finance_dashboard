from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from typing import Optional

from models.user import User  # Your user model
from database import get_db  # Dependency to get database session
from services.auth import decode_access_token  # Your token decoding function

# In-memory token blacklist
token_blacklist = set()

def get_current_user(
    access_token: Optional[str] = Cookie(None), 
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    if access_token in token_blacklist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is revoked",
        )
    try:
        # Decode the token (remove "Bearer " prefix)
        payload = decode_access_token(access_token.split("Bearer ")[1])
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
