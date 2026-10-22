from fastapi import APIRouter, HTTPException
import src.models.users as users

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(user_auth: users.UserAuth):
    token = users.authorise_user(user_auth)

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {"token": token}


@router.post("/register", status_code=201)
def register(user_reg: users.UserReg):
    user = users.register_user(user_reg)

    if user is None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return {"user": user}
