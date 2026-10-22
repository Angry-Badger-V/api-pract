from fastapi import APIRouter, HTTPException

from src.schemas.users import UserAuth, UserReg
from src.services.auth import authorise_user, register_user

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user_auth: UserAuth):
    token = authorise_user(user_auth)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {"token": token}

@router.post("/register", status_code=201)
def register(user_reg: UserReg):
    user = register_user(user_reg)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return {"user": user}
