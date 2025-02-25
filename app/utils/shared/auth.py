import random
import string
import bcrypt
import yagmail
from dotenv import load_dotenv
import os
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import PyJWTError
from app.db.redis_db import redis_client


load_dotenv()
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TOKEN_KEY = os.getenv("TOKEN_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 30

def generate_random_password(length=12):
    """Generate a random password with letters, digits, and special characters."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(characters) for _ in range(length))

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def send_password_to_email(user_email: str, password: str) -> bool:
    """
    Send password to email.
    """
    sender_email = "carolmkaysmamba14@gmail.com"
    subject = "Finish logging in to your account."
    body = f"Hello Minion, \n\nYour password is: {password}\n\nPlease use this password to login to your account.\n\nThank you!"
    try:
        yag = yagmail.SMTP(sender_email, EMAIL_PASSWORD)
        yag.send(to=user_email, subject=subject, contents=body)
        print("Email sent successfully!")
        yag.close()
        return True
    except Exception as e:
        print("Error sending email: ", e)
        return False

def generate_access_token(payload: dict) -> str:
    """
    Generate access token.
    """
    payload["token_type"] = "access"
    payload["exp"] = int((datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    session_id = payload.get("session_id")
    print("Token key is: ", TOKEN_KEY)
    token = jwt.encode(payload, TOKEN_KEY, algorithm="HS256")
    redis_client.setex(f"{session_id}_access_token", ACCESS_TOKEN_EXPIRE_MINUTES * 60, token)
    return token

def generate_refresh_token(payload: dict) -> str:
    """
    Generate refresh token.
    """
    payload["token_type"] = "refresh"
    payload["exp"] = int((datetime.now() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)).timestamp())
    session_id = payload.get("session_id")
    token = jwt.encode(payload, TOKEN_KEY, algorithm="HS256")
    redis_client.setex(f"{session_id}_refresh_token", REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60, token)
    return token

def get_refresh_token_from_session(session_id: str) -> str:
    """
    Get refresh token from session.
    """
    try:
        token = redis_client.get(f"{session_id}_refresh_token")
        if not token:
            return None
        return token.decode("utf-8")
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error getting refresh token.") from exc

def get_access_token_from_session(session_id: str) -> str:
    """
    Get access token from session.
    """
    token = redis_client.get(f"{session_id}_access_token")
    if not token:
        return None
    return token.decode("utf-8")

def decode_token(token: str) -> dict:
    """
    Decode token.
    """
    try:
        return jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}
    except PyJWTError as e:
        return {"error": str(e)}

def validate_token(token: str, token_type: str) -> dict:
    """
    Validate token.
    """
    from app.utils.admin.db import find_admin_by_email

    payload = decode_token(token)
    error = payload.get("error")
    if error:
        print("Error decoding token:", error)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized access.")

    session_id = payload.get("session_id")
    is_right_type = payload.get("token_type") == token_type
    if not is_right_type:
        print(f"Token type - {token_type} not equal to {payload.get('token_type')}.")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized access.")

    token_functions = {
        "access": get_access_token_from_session,
        "refresh": get_refresh_token_from_session
    }
    stored_token = token_functions[token_type](session_id)
    if stored_token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Unauthorized access.")

    user_email = payload.get("sub")
    user = find_admin_by_email(user_email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Unauthorized access.")
    return payload

def delete_tokens_from_session(session_id: str):
    """
    Delete tokens from session.
    """
    access_is_deleted = redis_client.delete(f"{session_id}_access_token")
    refresh_is_deleted = redis_client.delete(f"{session_id}_refresh_token")
    return access_is_deleted and refresh_is_deleted


