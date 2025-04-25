from backend.database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Get user by email
def get_user_by_email(bu_user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE bu_user_id = %s"
        cursor.execute(query, (bu_user_id,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        logger.error(f"Error fetching user by email: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Create user if they don't exist (for Google OAuth)
def create_user_if_not_exists(
        bu_user_id,
        user_name="New User",
        profile_img_url=None,
        bu_college="Unknown",
        role="user"
):
    conn = None
    cursor = None
    try:
        existing_user = get_user_by_email(bu_user_id)
        if existing_user:
            return existing_user  # Already exists

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO users (
                bu_user_id, user_name, profile_img_url, bu_college, role
            ) VALUES (%s, %s, %s, %s, %s)
        """
        values = (bu_user_id, user_name, profile_img_url, bu_college, role)
        cursor.execute(query, values)
        conn.commit()

        return {"message": "User created", "user_id": cursor.lastrowid}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# Fetch all study spots
def get_all_study_spots(has_outlets=None, has_meeting_rooms=None, has_food=None, has_spacious_seating=None,
                        has_printing=None, has_prayer_space=None, on_campus=None):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # noinspection SqlConstantExpression
        query = "SELECT * FROM spots WHERE 1=1" # surpassed always true stat
        params = []

        if has_outlets is not None:
            query += " AND has_outlets = %s"
            params.append(has_outlets)
        if has_meeting_rooms is not None:
            query += " AND has_meeting_rooms = %s"
            params.append(has_meeting_rooms)
        if has_food is not None:
            query += " AND has_food = %s"
            params.append(has_food)
        if has_spacious_seating is not None:
            query += " AND has_spacious_seating = %s"
            params.append(has_spacious_seating)
        if has_printing is not None:
            query += " AND has_printing = %s"
            params.append(has_printing)
        if has_prayer_space is not None:
            query += " AND has_prayer_space = %s"
            params.append(has_prayer_space)
        if on_campus is not None:
            query += " AND on_campus = %s"
            params.append(on_campus)

        cursor.execute(query, tuple(params))
        study_spots = cursor.fetchall()
        return study_spots
    except Exception as e:
        logger.error(f"Error fetching study spots with filters: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Add a new study spot
def add_study_spot(spot):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO spots (
                spot_name, address, open_early, open_late, has_outlets, has_food,
                has_printing, has_prayer_space, has_spacious_seating,
                has_meeting_rooms, on_campus, default_img, average_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            spot.spot_name,
            spot.address,
            spot.open_early,
            spot.open_late,
            spot.has_outlets,
            spot.has_food,
            spot.has_printing,
            spot.has_prayer_space,
            spot.has_spacious_seating,
            spot.has_meeting_rooms,
            spot.on_campus,
            spot.default_img_url,
            spot.average_rating
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Study spot added successfully", "spot_id": cursor.lastrowid}
    except Exception as e:
        logger.error(f"Error adding study spot: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Add or Edit spot hours
def add_spot_hours(spot_id, hours_list):
    """
    hours_list: a list of dicts like:
    [
        {"day_of_week": 0, "open_time": "08:00:00", "close_time": "21:00:00"},
        ...
    ]
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO spot_hours (spot_id, day_of_week, open_time, close_time)
            VALUES (%s, %s, %s, %s)
        """
        for hours in hours_list:
            cursor.execute(query, (
                spot_id,
                hours["day_of_week"],
                hours["open_time"],
                hours["close_time"]
            ))
        conn.commit()
    except Exception as e:
        logger.error(f"Error inserting spot hours: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Update an existing study spot
def update_study_spot(spot_id, spot):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE spots SET
                spot_name = %s,
                address = %s,
                open_early = %s,
                open_late = %s,
                has_outlets = %s,
                has_food = %s,
                has_printing = %s,
                has_prayer_space = %s,
                has_spacious_seating = %s,
                has_meeting_rooms = %s,
                on_campus = %s,
                default_img = %s,
                average_rating = %s
            WHERE spot_id = %s
        """
        values = (
            spot.spot_name,
            spot.address,
            spot.open_early,
            spot.open_late,
            spot.has_outlets,
            spot.has_food,
            spot.has_printing,
            spot.has_prayer_space,
            spot.has_spacious_seating,
            spot.has_meeting_rooms,
            spot.on_campus,
            spot.default_img_url,
            spot.average_rating,
            spot_id
        )
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Study spot updated successfully"}
    except Exception as e:
        logger.error(f"Error updating study spot: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Fetch study spots open on a specific day (0 = Sunday, ..., 6 = Saturday)
def get_study_spots_by_day(day_of_week: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT s.*
            FROM spots s
            JOIN spot_hours h ON s.spot_id = h.spot_id
            WHERE h.day_of_week = %s
        """
        cursor.execute(query, (day_of_week,))
        spots = cursor.fetchall()
        return spots
    except Exception as e:
        logger.error(f"Error fetching study spots for day {day_of_week}: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Delete a study spot
def delete_study_spot(spot_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM spots WHERE spot_id = %s", (spot_id,))
        conn.commit()
        return {"message": "Study spot deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting study spot: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Add a new review
def add_review(user_id, spot_id, rating, review_content):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO reviews (user_id, spot_id, rating, review_content)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, spot_id, rating, review_content))
        conn.commit()
        return {"message": "Review submitted successfully"}
    except Exception as e:
        logger.error(f"Error adding review: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Enforce 1 review per spot per user
def has_user_reviewed(user_id: int, spot_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT 1 FROM reviews WHERE user_id = %s AND spot_id = %s LIMIT 1"
        cursor.execute(query, (user_id, spot_id))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(f"Error checking if user {user_id} reviewed spot {spot_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()


# Fetch all reviews for a specific spot
def get_reviews_for_spot(spot_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 
                review_id,
                user_id,
                spot_id,
                review_content,
                rating,
                review_img_url,
                review_tags,
                timestamp
            FROM reviews
            WHERE spot_id = %s
            ORDER BY timestamp DESC
        """
        cursor.execute(query, (spot_id,))
        reviews = cursor.fetchall()
        return reviews
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Add a favorite
def add_favorite(user_email: str, spot_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
                INSERT INTO favorites (user_email, spot_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """
        cursor.execute(query, (user_email, spot_id))
        conn.commit()
        return {"message": "Favorite added"}
    except Exception as e:
        logger.error(f"Error adding favorite: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Remove a favorite
def remove_favorite(user_email: str, spot_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM favorites WHERE user_email = %s AND spot_id = %s;"
        cursor.execute(query, (user_email, spot_id))
        conn.commit()
        return {"message": "Favorite removed"}
    except Exception as e:
        logger.error(f"Error removing favorite: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# Fetch all favorite spots for a user
 def get_favorites_by_user(user_email: str):
     conn = None
     cursor = None
     try:
         conn = get_db_connection()
         cursor = conn.cursor(dictionary=True)
         query = """
             SELECT s.* FROM spots s
             JOIN favorites f ON s.spot_id = f.spot_id
             WHERE f.user_email = %s;
         """
         cursor.execute(query, (user_email,))
         favorites = cursor.fetchall()
         return favorites
     except Exception as e:
         logger.error(f"Error fetching favorites: {e}")
         raise HTTPException(status_code=500, detail="Database error")
     finally:
         if cursor:
             cursor.close()
         if conn:
             conn.close()
