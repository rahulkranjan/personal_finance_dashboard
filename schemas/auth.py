from pydantic import BaseModel
import datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserBase(BaseModel):
    username: str
    email: str

class UserBaseV1(BaseModel):
    username: str

class UserCreate(UserBase):
    username: str
    email: str
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    is_admin: bool

class RequestDetails(BaseModel):
    username: str
    password: str

class TokenCreate(BaseModel):
    user_id:str
    access_token:str
    refresh_token:str
    status:bool
    created_date:datetime.datetime