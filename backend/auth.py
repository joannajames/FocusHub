from fastapi import HTTPException, Security, BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from google.oauth2 import id_token
from google.auth.transport import requests
import random
import string

# DB functions (update import path as needed)
from backend.crud import get_user_by_email, create_user_if_not_exists

# CONFIG
GOOGLE_CLIENT_ID = "780726687923-hqvono1d8ln6900o0gcdatahjditpqp8.apps.googleusercontent.com"
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Temporary in-memory store for verification codes
verification_codes = {}

# GOOGLE TOKEN VERIFICATION
def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        email = idinfo['email']
        return email
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google token verification failed: {str(e)}")

# EMAIL FUNCTION
def send_verification_email(email, code):
    # Replace with actual email sending logic (e.g., focushub.bu@gmail.com)
    print(f"[EMAIL MOCK] Sent from hi.focushub@gmail.com to {email}|Verification code: {code}")

# ISSUE ACCESS TOKEN
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# DECODE ACCESS TOKEN
def get_current_user(token: str = Security(OAuth2PasswordBearer(tokenUrl="token"))):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ADMIN CHECK
def get_current_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

# STEP 1: START VERIFICATION
def start_email_verification(token: str, background_tasks: BackgroundTasks):
    email = verify_google_token(token)

    if not email.endswith("@bu.edu"):
        raise HTTPException(status_code=403, detail="Only @bu.edu emails are allowed")

    code = ''.join(random.choices(string.digits, k=6))
    verification_codes[email] = code

    background_tasks.add_task(send_verification_email, email, code)
    return {"message": f"Verification code sent to {email}"}

# STEP 2: VERIFY CODE AND LOGIN
def verify_code_and_login(email: str, code: str):
    expected = verification_codes.get(email)
    if not expected or code != expected:
        raise HTTPException(status_code=401, detail="Invalid or expired verification code")

    del verification_codes[email]

    # Create user if needed
    user = create_user_if_not_exists(
        bu_user_id=email,
        user_name=email.split("@")[0].capitalize(),
        profile_img_url=None,
        bu_college="Unknown",
        role="user"
    )

    access_token = create_access_token({"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}
