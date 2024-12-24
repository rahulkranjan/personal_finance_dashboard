from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from services.auth import create_access_token, create_refresh_token, decode_access_token, verify_password, get_password_hash
from schemas.auth import RequestDetails, UserCreate, UserOut
from models.user import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(req_user: RequestDetails, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req_user.username).first()
    if not user or not verify_password(req_user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(user.username)
    
    # Set tokens in HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # Ensure secure=True in production (HTTPS only)
        samesite="Strict",
        max_age=3600,  # Set expiration time (e.g., 1 hour)
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=3600 * 24 * 7,  # Example: 7 days for refresh token
    )
    
    return {"message": "Logged in successfully"}

# Middleware for blacklist
token_blacklist = set()

@router.post("/logout")
def logout(response: Response, access_token: Optional[str] = Depends(oauth2_scheme)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token provided",
        )

    # Add the token to the blacklist
    token_blacklist.add(access_token)

    # Clear cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Logged out successfully"}
