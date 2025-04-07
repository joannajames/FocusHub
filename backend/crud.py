from database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch all study spots
def get_all_study_spots(wifi=None, outlets=None, quiet=None, food=None, prayer_space=None, printing=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM study_spots WHERE 1=1"
        params = []

        if wifi is not None:
            query += " AND wifi = %s"
            params.append(wifi)
        if outlets is not None:
            query += " AND outlets = %s"
            params.append(outlets)
        if quiet is not None:
            query += " AND quiet = %s"
            params.append(quiet)
        if food is not None:
            query += " AND food = %s"
            params.append(food)
        if prayer_space is not None:
            query += " AND prayer_space = %s"
            params.append(prayer_space)
        if printing is not None:
            query += " AND printing = %s"
            params.append(printing)

        cursor.execute(query, tuple(params))
        study_spots = cursor.fetchall()
        return study_spots
    except Exception as e:
        logger.error(f"Error fetching study spots with filters: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()

# Add a new study spot
def add_study_spot(name, location, wifi, outlets, quiet, food):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO study_spots (name, location, wifi, outlets, quiet, food)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, location, wifi, outlets, quiet, food))
        conn.commit()
        return {"message": "Study spot added successfully"}
    except Exception as e:
        logger.error(f"Error adding study spot: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()

# Update an existing study spot
def update_study_spot(spot_id, name, location, wifi, outlets, quiet, food):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            UPDATE study_spots
            SET name = %s, location = %s, wifi = %s, outlets = %s, quiet = %s, food = %s
            WHERE id = %s
        """
        cursor.execute(query, (name, location, wifi, outlets, quiet, food, spot_id))
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
        cursor.execute("DELETE FROM study_spots WHERE id = %s", (spot_id,))
        conn.commit()
        return {"message": "Study spot deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting study spot: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()

# Add a new review
def add_review(user_email, spot_id, rating, comment):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO reviews (user_email, spot_id, rating, comment)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_email, spot_id, rating, comment))
        conn.commit()
        return {"message": "Review submitted successfully"}
    except Exception as e:
        logger.error(f"Error adding review: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()

# Fetch all reviews for a specific study spot
def get_reviews_for_spot(spot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT user_email, rating, comment, created_at
            FROM reviews
            WHERE spot_id = %s
            ORDER BY created_at DESC
        """
        cursor.execute(query, (spot_id,))
        reviews = cursor.fetchall()
        return reviews
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()
