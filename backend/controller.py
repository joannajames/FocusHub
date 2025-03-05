from fastapi import APIRouter
from database import get_all_study_spots  # Import database function

router = APIRouter()

# ✅ Route to get study spots
@router.get("/study_spots")
def get_study_spots():
    return get_all_study_spots()
