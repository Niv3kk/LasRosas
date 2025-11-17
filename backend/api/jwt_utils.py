# backend/api/jwt_utils.py
import datetime
import jwt
from django.conf import settings


def create_jwt(payload: dict, minutes=60):
    """
    Crea un JWT con exp/iat. Fuerza 'sub' a string (PyJWT v2 lo requiere).
    """
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    to_encode = {**payload, 'exp': exp, 'iat': datetime.datetime.utcnow()}
    if 'sub' in to_encode:
        to_encode['sub'] = str(to_encode['sub'])
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm='HS256')


def decode_jwt(token: str):
    """
    Valida el JWT con leve tolerancia de reloj.
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=['HS256'],
        options={"require": ["exp", "iat"]},
        leeway=10,  # ±10s por si el reloj está levemente desfasado
    )
