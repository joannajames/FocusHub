#Importing FastAPI, dependencies, and connection between front/backend
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth import get_current_user  # Authentication
from controller import router
import logging
from dotenv import load_dotenv

load_dotenv()


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open to intranet users
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safely include the router
try:
    app.include_router(router)
    logger.info("Router successfully loaded.")
except Exception as e:
    logger.error(f"Failed to load router: {e}")

@app.get("/")
async def root():
    return {"message": "FocusHub API is running"}

@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {user['email']}"}

