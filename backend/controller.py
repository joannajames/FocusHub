from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user, get_current_admin, create_access_token, authenticate_user
from crud import get_all_study_spots, add_study_spot, update_study_spot, delete_study_spot, add_review, get_reviews_for_spot
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
def get_study_spots(
    has_outlets: str = None,
    has_meeting_rooms: str = None,
    has_food: str = None,
    has_spacious_seating: str = None,
    has_printing: str = None,
    has_prayer_space: str = None,
    on_campus: str = None,
):
    return {"data": get_all_study_spots(has_outlets, has_meeting_rooms, has_food, has_spacious_seating, has_printing, has_prayer_space, on_campus)}

# Add a new study spot (Admin Only)
@router.post("/study_spots")
def create_study_spot(
    spot_name: str,
    address: str,
    has_outlets: str,
    has_meeting_rooms: str,
    has_food: str,
    has_spacious_seating: str,
    has_printing: str,
    has_prayer_space: str,
    on_campus: str,
    default_img_url: str = None,
    average_rating: float = 0.0,
    user: dict = Depends(get_current_admin)
):
    return add_study_spot(spot_name, address, "TBD", "TBD", has_outlets, has_food,
                          has_printing, has_prayer_space, has_spacious_seating,
                          has_meeting_rooms, on_campus, default_img_url, average_rating)


# Update a study spot (Admin Only)
@router.put("/study_spots/{spot_id}")
def modify_study_spot(
    spot_id: int,
    spot_name: str,
    address: str,
    has_outlets: str,
    has_meeting_rooms: str,
    has_food: str,
    has_spacious_seating: str,
    has_printing: str,
    has_prayer_space: str,
    on_campus: str,
    default_img_url: str = None,
    average_rating: float = 0.0,
    user: dict = Depends(get_current_admin)
):
    return update_study_spot(spot_id, spot_name, address, "TBD", "TBD", has_outlets, has_food,
                             has_printing, has_prayer_space, has_spacious_seating,
                             has_meeting_rooms, on_campus, default_img_url, average_rating)


# Delete a study spot (Admin Only)
@router.delete("/study_spots/{spot_id}")
def remove_study_spot(spot_id: int, user: dict = Depends(get_current_admin)):
    return delete_study_spot(spot_id)

# Submit a review (User only)
@router.post("/reviews")
def create_review(spot_id: int, rating: int, review_content: str, user: dict = Depends(get_current_user)):
    return add_review(user["user_id"], spot_id, rating, review_content)

# Get reviews for a specific study spot (Public)
@router.get("/reviews/{spot_id}")
def read_reviews(spot_id: int):
    return {"data": get_reviews_for_spot(spot_id)}

