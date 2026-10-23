from src.schemas.users import UserAuth, UserReg
from src.repositories import users as user_repo
from src.utils.normalisation import normalise_name, normalise_email
from src.utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

def authorise_user(user_auth: UserAuth) -> str | None:
    email = normalise_email(user_auth.email)

    user = user_repo.select_user_by_email(email)

    if user is None:
        return None

    if not verify_password(user_auth.password, user["password"]):
        return None

    return create_access_token(user["id"])

def register_user(user_reg: UserReg) -> dict | None:
    name = normalise_name(user_reg.name)
    email = normalise_email(user_reg.email)

    if user_repo.select_user_by_email(email) is not None:
        return None

    password_hash = hash_password(user_reg.password)

    return user_repo.insert_user(name, email, password_hash)
