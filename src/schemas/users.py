from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserReg(BaseModel):
    name: str
    email: EmailStr
    password: str
