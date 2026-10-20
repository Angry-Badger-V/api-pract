import pytest
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from src.seed.users import name_normalisation, email_normalisation, password_hashing

ph = PasswordHasher()

@pytest.fixture
def make_user():
  user = {
    "name": " Alice     Rahman    ",
    "email": "  al   Ice@eXamplE  .com",
    "password": "password123"
  }
  return user

def test_name_normalisation(make_user):
    result = name_normalisation(make_user)
    assert result["name"] == "Alice Rahman"

def test_email_normalisation(make_user):
    result = email_normalisation(make_user)
    assert result["email"] == "alice@example.com"

def test_password_hasing_correct(make_user):
    result = password_hashing(make_user)
    assert result["password"] != "password123"
    assert ph.verify(result["password"], "password123")

def test_password_hasing_incorrect(make_user):
    make_user["password"] = "padsija"
    result = password_hashing(make_user)
    with pytest.raises(VerifyMismatchError):
        ph.verify(result["password"], "password123")
