import firebase_admin
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from firebase_admin import auth, credentials,_apps, initialize_app
from database import get_db_connection
from datetime import datetime, timedelta
import os

# --- Setup ---
# One-time Firebase initialization
if not firebase_admin._apps:
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
# --- Verify Firebase ID Token ---
def verify_firebase_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # includes 'email', 'uid', 'email_verified', etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")


# --- Backend API to login: Frontend will send Firebase token here ---

def login_with_firebase(firebase_token: str):
    decoded = verify_firebase_token(firebase_token)
    email = decoded["email"]

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

        return {
            "user_id": user["user_id"],
            "is_admin": bool(user["admin_access"]),
            "email": email,
        }

    finally:
        cursor.close()
        conn.close()

bearer = HTTPBearer()
# --- Verify your own JWT in protected routes ---
async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer)
):
    """
    Reads the raw Firebase ID-token from the Authorization header,
    verifies it, and returns the decoded payload (including 'email').
    """
    try:
        user_info = verify_firebase_token(creds.credentials)
        return user_info
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase token")

# Function to check if the user is an admin
def get_current_admin(user: dict = Depends(get_current_user)):
    if not user["is_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
