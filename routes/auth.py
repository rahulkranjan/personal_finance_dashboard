from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from services.auth import create_access_token, create_refresh_token, verify_password, get_password_hash
from schemas.auth import RequestDetails, UserCreate, UserOut, Token
from models.user import User, TokenTable
from database import get_db

router = APIRouter()


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


@router.post("/login", response_model=Token)
def login(req_user: RequestDetails, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req_user.username).first()
    if not user or not verify_password(req_user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    refresh = create_refresh_token(user.username)

    token_db = TokenTable(user_id=user.id,  access_toke=access_token,  refresh_toke=refresh, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)

    return {"access_token": access_token, "refresh_token": refresh, "token_type": "bearer"}
