from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.logger import logger
from pydantic import BaseModel
from auth import get_current_user, login_with_firebase, verify_firebase_token, get_current_admin
from crud import get_all_study_spots, add_study_spot, update_study_spot, delete_study_spot, add_review, \
    get_reviews_for_spot, get_top_tags_per_spot, check_user_review, get_study_spot_by_id, check_or_add_user, \
    get_user_info_by_email
from datetime import timedelta
from fastapi import Path
from crud import update_user_profile,get_db_connection

router = APIRouter()

#Debugging

@router.get("/db_health")
def db_health_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "fail", "error": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()



# Authorization and Authentication

@router.post("/token")
def login(firebase_token: str):
    return login_with_firebase(firebase_token)


# controller.py
@router.get("/users/me")
def get_my_profile(current: dict = Depends(get_current_user)):
    # current["email"] is pulled straight from Firebase
    user_id = check_or_add_user(current["email"])
    user    = get_user_info_by_email(current["email"])
    return {"user_id": user_id, "is_new_user": False, "user_info": user}


@router.post("/users/{user_id}/complete_profile")
def complete_user_profile(user_id: int,
                           degree: str = Body(...),
                           academic_level: str = Body(...),
                           bu_college: str = Body(...)):
    update_user_profile(user_id, degree, academic_level, bu_college)
    return {"message": "Profile updated successfully"}


# Spots
@router.get("/study_spots/top_tags")
def fetch_top_tags():
    tags = get_top_tags_per_spot()
    return {"data": dict(tags)}

# Fetch all study spots (Publicly accessible)
@router.get("/study_spots")
def fetch_all_study_spots():
    spots = get_all_study_spots()
    return {"data": spots}

# Fetch study spots by ID (Publicly accessible)
@router.get("/study_spots/{spot_id}")
def read_study_spot(spot_id: int):
    try:
        spot_rows = get_study_spot_by_id(spot_id)

        if not spot_rows:
            raise HTTPException(status_code=404, detail="Study spot not found")

        return {"data": spot_rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/study_spots/day/{day_index}")
def route_study_spots_open_on_day(
        day_index: int = Path(ge=0, le=6),
        has_outlets: str = None,
        has_meeting_rooms: str = None,
        has_food: str = None,
        has_spacious_seating: str = None,
        has_printing: str = None,
        has_prayer_space: str = None,
        on_campus: str = None
):
    import calendar
    weekday = calendar.day_name[day_index]

    # Log the request for debugging
    logger.info(f"Fetching study spots for {weekday} with filters: outlets={has_outlets}, food={has_food}, etc.")

    # Get the study spots
    results = get_all_study_spots(
        has_outlets,
        has_meeting_rooms,
        has_food,
        has_spacious_seating,
        has_printing,
        has_prayer_space,
        on_campus,
        weekday  # Pass the weekday name
    )

    # Log the number of results for debugging
    logger.info(f"Found {len(results)} study spots for {weekday}")

    return {"data": results}

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
    default_img: str = None,
    avg_rating: float = 0.0,
    user: dict = Depends(get_current_admin)
):
    return add_study_spot(spot_name, address, has_outlets, has_food,
                          has_printing, has_prayer_space, has_spacious_seating,
                          has_meeting_rooms, on_campus, default_img, avg_rating)


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
    default_img: str = None,
    avg_rating: float = 0.0,
    user: dict = Depends(get_current_admin)
):
    return update_study_spot(spot_id, spot_name, address, has_outlets, has_food,
                             has_printing, has_prayer_space, has_spacious_seating,
                             has_meeting_rooms, on_campus, default_img, avg_rating)


# Delete a study spot (Admin Only)
@router.delete("/study_spots/{spot_id}")
def remove_study_spot(spot_id: int, user: dict = Depends(get_current_admin)):
    return delete_study_spot(spot_id)


from pydantic import BaseModel
from typing import Optional

class ReviewCreate(BaseModel):
    spot_id: int
    rating: int
    review_content: str
    review_tags: Optional[str] = None
    review_img: Optional[str] = None

from fastapi import Body
from typing import Optional


@router.post("/reviews")
def create_review(
    spot_id: int = Body(...),
    rating: int = Body(...),
    review_content: str = Body(...),
    review_tags: Optional[str] = Body(default=""),        # optional default ""
    review_img: Optional[str] = Body(default=None),      # optional default None
    user: dict = Depends(get_current_user)
):
    # 1) Use email to find user_id from DB
    email = user["email"]
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT user_id FROM users WHERE bu_user_id = %s", (email,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(404, detail="User not found in DB")

        user_id = result["user_id"]

        # 2) Prevent duplicates
        if check_user_review(user_id, spot_id):
            raise HTTPException(400, "You’ve already reviewed this spot")

        # 3) Insert review
        print(f"Inserting review for user_id={user_id}, spot_id={spot_id}")

        return add_review(user_id, spot_id, rating, review_content, review_tags, review_img)

    finally:
        cursor.close()
        conn.close()
# Get reviews for a specific study spot (Public)
@router.get("/reviews/{spot_id}")
def read_reviews(spot_id: int):
    return {"data": get_reviews_for_spot(spot_id)}

@router.get("/reviews/{spot_id}/exists")
def check_if_user_reviewed_spot(
    spot_id: int,
    current_user: dict = Depends(get_current_user)
):
    email = current_user["email"]
    user_id = check_or_add_user(email)
    exists = check_user_review(user_id, spot_id)
    return {"review_exists": exists}