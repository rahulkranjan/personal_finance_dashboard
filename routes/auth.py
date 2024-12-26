from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from services.auth import create_access_token, create_refresh_token, decode_access_token, verify_password, get_password_hash
from schemas.auth import RequestDetails, UserCreate, UserOut
from models.user import User
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

token_blacklist = set()


@router.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    password = get_password_hash(user.password)
    new_user = User(username=user.username,
                    email=user.email, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(req_user: RequestDetails, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req_user.username).first()
    if not user or not verify_password(req_user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(user.username)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=False, 
        max_age=60 * 60 * 24 * 365 * 10,
        samesite=None,
        domain="personalfinancedashboard-production.up.railway.app",
    )

    return {"message": "Logged in successfully"}

@router.post("/logout")
def logout(response: Response, access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
    # Extract the token from "Bearer <token>" format
    token = access_token.split("Bearer ")[1] if "Bearer " in access_token else access_token
    token_blacklist.add(token)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}


@router.get("/check")
def check_auth(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    print(access_token, 'access_token')
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = access_token.split(
        "Bearer ")[1] if "Bearer " in access_token else access_token
    username = decode_access_token(token)
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return {"user": {"username": user.username, "email": user.email}}
