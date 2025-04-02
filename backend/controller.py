from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user, get_current_admin, create_access_token, authenticate_user
from crud import get_all_study_spots, add_study_spot, update_study_spot, delete_study_spot
from datetime import timedelta

router = APIRouter()

# User Login - Generates JWT Token
@router.post("/token")
def login(email: str, password: str):
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["email"]}, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

# Fetch all study spots (Publicly accessible)
@router.get("/study_spots")
def get_study_spots():
    return {"data": get_all_study_spots()}

# Add a new study spot (Admin Only)
@router.post("/study_spots")
def create_study_spot(name: str, location: str, wifi: bool, outlets: bool, quiet: bool, food: bool, user: dict = Depends(get_current_admin)):
    return add_study_spot(name, location, wifi, outlets, quiet, food)

# Update a study spot (Admin Only)
@router.put("/study_spots/{spot_id}")
def modify_study_spot(spot_id: int, name: str, location: str, wifi: bool, outlets: bool, quiet: bool, food: bool, user: dict = Depends(get_current_admin)):
    return update_study_spot(spot_id, name, location, wifi, outlets, quiet, food)

# Delete a study spot (Admin Only)
@router.delete("/study_spots/{spot_id}")
def remove_study_spot(spot_id: int, user: dict = Depends(get_current_admin)):
    return delete_study_spot(spot_id)
