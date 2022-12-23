from app.config import JWT_ALGORITHM, JWT_SECRET_KEY
import time
from typing import Dict
import jwt
import bcrypt 

def hash_password(password):
    my_salt = bcrypt.gensalt()
    bytePass = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytePass, my_salt)
    return hashed_password

def check_password(password, hashed_password):
    return bcrypt.checkpw(password, hashed_password)

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 6000
    }

    token = jwt.encode(payload, str(JWT_SECRET_KEY), str(JWT_ALGORITHM))

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, str(JWT_SECRET_KEY), str(JWT_ALGORITHM))
        return decoded_token if decoded_token['expires'] >= time.time() else None 
    except:
        return {}

