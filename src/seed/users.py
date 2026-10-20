from argon2 import PasswordHasher

ph = PasswordHasher()

def name_normalisation(user):
    user["name"] = " ".join(
            user["name"].split())
    return user

def email_normalisation(user):
    user["email"] = "".join(
            user["email"].split()
            ).lower()
    return user

def password_hashing(user):
    user["password"] = ph.hash(
            user["password"])
    return user
