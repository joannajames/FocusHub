from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "780726687923-hqvono1d8ln6900o0gcdatahjditpqp8.apps.googleusercontent.com"

def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo['email']
        return {
            "email": email,
            "is_admin": email.endswith("@yourorg.edu")  # Adjust logic as needed
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google token verification failed: {str(e)}")

# Secret key for JWT signing (Change this & store securely)
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token expires in 1 hour

# Simulated user database (Replace with real DB authentication)
fake_users_db = {
    "admin@example.com": {"password": "admin123", "is_admin": True},
    "user@example.com": {"password": "user123", "is_admin": False},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to authenticate user (Replace with database authentication)
def authenticate_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user or user["password"] != password:
        return None
    return {"email": email, "is_admin": user["is_admin"]}

# Function to verify JWT token
def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "is_admin": fake_users_db.get(email, {}).get("is_admin", False)}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Function to check if the user is an admin
def get_current_admin(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
