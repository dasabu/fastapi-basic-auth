import jwt
import time
from decouple import config
from bcrypt import checkpw, hashpw, gensalt

JWT_SECRET = config("JWT_SECRET")
JWT_ALGO = config("JWT_ALGO")

def sign_jwt(user_id: int):
    payload = {
        "user_id": user_id,
        "expires": time.time() + 900, # current_time + 900s (15min from now)   
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGO)
    return token

def decode_jwt(token: str) -> dict: # payload
    try:
        # decode token to get payload
        decoded_token = jwt.decode(jwt=token, key=JWT_SECRET, algorithms=[JWT_ALGO])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        print("Unable to decode token")
        return None
    

def verify_password(plain_password: str, hashed_password: str):
    return checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
    
def get_password_hash(plain_password: str):
    return hashpw(
        plain_password.encode("utf-8"),
        gensalt()
    ).decode("utf-8")