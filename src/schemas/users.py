from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserReg(BaseModel):
    name: str
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

class RegisterResponse(BaseModel):
    user: UserResponse
