# backend/api/security.py
from django.contrib.auth.hashers import check_password, make_password
def make_pwd(raw: str) -> str: return make_password(raw)
def check_pwd(raw: str, hashed: str) -> bool:
    if hashed and hashed.startswith('pbkdf2_'):
        return check_password(raw, hashed)
    return raw == hashed
