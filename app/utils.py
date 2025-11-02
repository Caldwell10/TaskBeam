import bcrypt
import time
from typing import Dict
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# function to hash password
def hash_password(password: str):
    # generate a salt
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password

# verify password match
def verify_password(provided_password, hashed_password):
    return  bcrypt.checkpw(provided_password, hashed_password)

# return token response
def token_response(token: str):
    return {
        "access_token": token
    }

# sign and decode JWT string
def sign_jwt(user_id: str) -> Dict[str, str]:
    payload =  {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms = [JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
