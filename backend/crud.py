from database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_study_spots(
        has_outlets=None,
        has_meeting_rooms=None,
        has_food=None,
        has_spacious_seating=None,
        has_printing=None,
        has_prayer_space=None,
        on_campus=None,
        weekday=None  # Filter by day of week
):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Base query
        base_query = """
            SELECT 
                s.*,
                h.opens AS open_time,
                h.closes AS close_time,
                h.day
            FROM spots s
            JOIN hours h ON s.spot_id = h.spot_id
        """

        # Start with an empty WHERE clause
        where_clauses = []
        params = []

        # Add day filter if specified
        if weekday:
            where_clauses.append("h.day = %s")
            params.append(weekday)

        # Add other filters
        if has_outlets:
            where_clauses.append("s.has_outlets = %s")
            params.append(has_outlets)
        if has_meeting_rooms:
            where_clauses.append("s.has_meeting_rooms = %s")
            params.append(has_meeting_rooms)
        if has_food:
            where_clauses.append("s.has_food = %s")
            params.append(has_food)
        if has_spacious_seating:
            where_clauses.append("s.has_spacious_seating = %s")
            params.append(has_spacious_seating)
        if has_printing:
            where_clauses.append("s.has_printing = %s")
            params.append(has_printing)
        if has_prayer_space:
            where_clauses.append("s.has_prayer_space = %s")
            params.append(has_prayer_space)
        if on_campus:
            where_clauses.append("s.on_campus = %s")
            params.append(on_campus)

        # Construct the final query
        query = base_query
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        # Execute the query
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error fetching study spots: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
# Add a new study spot
def add_study_spot(spot):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO spots (
                spot_name, address, open_early, open_late, has_outlets, has_food,
                has_printing, has_prayer_space, has_spacious_seating,
                has_meeting_rooms, on_campus, default_img_url, average_rating
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
        cursor.close()
        conn.close()

# Update an existing study spot
def update_study_spot(spot_id, spot):
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
                default_img_url = %s,
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
        cursor.close()
        conn.close()

# Delete a study spot
def delete_study_spot(spot_id):
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
        cursor.close()
        conn.close()
        
# Add a new review       
def add_review(user_id, spot_id, rating, review_content):
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
        cursor.close()
        conn.close()
# Fetch all reviews for a specific spot
def get_reviews_for_spot(spot_id):
    print(spot_id)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        logger.info(f"Fetching reviews for spot_id={spot_id}")
        query = """
            SELECT 
                review_id,
                user_id,
                spot_id,
                review_content,
                rating,
                review_img,
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
        import traceback
        print("DB ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

