from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from database import get_db_connection
from datetime import datetime, timedelta
import os

# --- Setup ---
GOOGLE_CLIENT_ID = "780726687923-hqvono1d8ln6900o0gcdatahjditpqp8.apps.googleusercontent.com"
SECRET_KEY = "faefdfafadfouhaoue34q8749813y45rh13qoquyrhq"  # use strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
bearer_scheme = HTTPBearer()

# --- Verify Firebase ID Token ---
def verify_firebase_token(firebase_token: str):
    try:
        idinfo = id_token.verify_oauth2_token(firebase_token, requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo['email']
        return email
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid Firebase token: {str(e)}")

# --- Create your own JWT Token (for your app sessions) ---
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Backend API to login: Frontend will send Firebase token here ---
def login_with_firebase(firebase_token: str):
    email = verify_firebase_token(firebase_token)

    # Lookup user info in your database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT user_id, admin_access
            FROM users
            WHERE bu_user_id = %s
        """
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        jwt_data = {
            "sub": email,
            "user_id": user["user_id"],
            "is_admin": bool(user["admin_access"]),
        }

        access_token = create_access_token(jwt_data)

        return {"access_token": access_token, "token_type": "bearer"}

    finally:
        cursor.close()
        conn.close()

# --- Verify your own JWT in protected routes ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "email": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "is_admin": payload.get("is_admin", False),
        }
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

# --- Check if user is admin ---
def get_current_admin(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
