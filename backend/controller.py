from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from backend.auth import (start_email_verification, verify_code_and_login, get_current_user, get_current_admin, create_access_token)
from backend.crud import (get_all_study_spots, get_study_spots_by_day, add_study_spot, update_study_spot, delete_study_spot, add_review, get_reviews_for_spot, add_spot_hours, has_user_reviewed, add_favorite, remove_favorite, get_favorites_by_user)
from datetime import timedelta

router = APIRouter()

# Step 1: Google OAuth login start - verifies and sends code
@router.post("/auth/google")
def google_oauth_start(token: str, background_tasks: BackgroundTasks):
    return start_email_verification(token, background_tasks)

# Step 2: User submits code to verify and receive JWT
@router.post("/auth/verify-code")
def verify_email_code(email: str, code: str):
    return verify_code_and_login(email, code)

# Fetch all study spots (with optional filters)
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
    return {
        "data": get_all_study_spots(
            has_outlets,
            has_meeting_rooms,
            has_food,
            has_spacious_seating,
            has_printing,
            has_prayer_space,
            on_campus
        )
    }

# Fetch study spots open on a specific day (Hub filter feature)
@router.get("/study_spots/day/{day_of_week}")
def get_study_spots_by_day_route(day_of_week: int):
    return {"data": get_study_spots_by_day(day_of_week)}

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

# Update study spot (Admin Only)
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

# Submit a review and check if user submitted already (User Only)
@router.post("/reviews")
def create_review(spot_id: int, rating: int, review_content: str, user: dict = Depends(get_current_user)):
    if has_user_reviewed(user["user_id"], spot_id):
        raise HTTPException(status_code=409, detail="You have already submitted a review for this spot.")
    return add_review(user["user_id"], spot_id, rating, review_content)

# Get reviews for a specific study spot (Public)
@router.get("/reviews/{spot_id}")
def read_reviews(spot_id: int):
    return {"data": get_reviews_for_spot(spot_id)}

# Add a favorite (User only)
@router.post("/favorites")
def mark_favorite(spot_id: int, user: dict = Depends(get_current_user)):
    return add_favorite(user["bu_user_id"], spot_id)

# Remove a favorite (User only)
@router.delete("/favorites")
def unmark_favorite(spot_id: int, user: dict = Depends(get_current_user)):
    return remove_favorite(user["bu_user_id"], spot_id)

# Get all favorite spots for a user (User only)
@router.get("/favorites")
def get_user_favorites(user: dict = Depends(get_current_user)):
    return {"data": get_favorites_by_user(user["bu_user_id"])}
