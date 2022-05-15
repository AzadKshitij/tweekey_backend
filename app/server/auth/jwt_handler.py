import time
import jwt
from decouple import config

JWT_SECRET = config('SECRET')
JWT_ALGORITHM = config('ALGORITHM')

# Returns genereted tokens


def token_responce(token: str):
    return {
        "token": token,
        "expires": time.time() + 3600
    }


# Generating JWT tokens


def signJWT(userId: str):
    payload = {
        "user_id": userId,
        "exp": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_responce(token)


def decodeJWT(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired, please login again."}
