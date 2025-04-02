from database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch all study spots
def get_all_study_spots():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM study_spots")
        study_spots = cursor.fetchall()
        return study_spots
    except Exception as e:
        logger.error(f"Error fetching study spots: {e}")
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
