from database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch all study spots
def get_all_study_spots(has_outlets=None,has_meeting_rooms=None, has_food=None, has_spacious_seating=None, has_printing=None, has_prayer_space=None, on_campus=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT s.*, h.*
                FROM spots s
                         LEFT JOIN hours h ON s.spot_id = h.spot_id
                WHERE 1 = 1 \
                """
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
        cursor.close()
        conn.close()

# Add a new study spot
def add_study_spot(spot):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO spots (
                spot_name, address, has_outlets, has_food,
                has_printing, has_prayer_space, has_spacious_seating,
                has_meeting_rooms, on_campus, default_img, avg_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            spot.spot_name,
            spot.address,
            spot.has_outlets,
            spot.has_food,
            spot.has_printing,
            spot.has_prayer_space,
            spot.has_spacious_seating,
            spot.has_meeting_rooms,
            spot.on_campus,
            spot.default_img,
            spot.avg_rating
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
                has_outlets = %s,
                has_food = %s,
                has_printing = %s,
                has_prayer_space = %s,
                has_spacious_seating = %s,
                has_meeting_rooms = %s,
                on_campus = %s,
                default_img = %s,
                avg_rating = %s
            WHERE spot_id = %s
        """
        values = (
            spot.spot_name,
            spot.address,
            spot.has_outlets,
            spot.has_food,
            spot.has_printing,
            spot.has_prayer_space,
            spot.has_spacious_seating,
            spot.has_meeting_rooms,
            spot.on_campus,
            spot.default_img,
            spot.avg_rating,
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


def get_study_spot_by_id(spot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT s.*, \
                       h.day, \
                       h.opens, \
                       h.closes
                FROM spots s \
                         LEFT JOIN \
                     hours h \
                     ON \
                         s.spot_id = h.spot_id
                WHERE s.spot_id = %s
                ORDER BY h.day ASC \
                """
        cursor.execute(query, (spot_id,))
        rows = cursor.fetchall()
        if not rows:
            return None
        spot = {
            "spot_id": rows[0]["spot_id"],
            "spot_name": rows[0]["spot_name"],
            "default_img": rows[0]["default_img"],
            "address": rows[0]["address"],
            "avg_rating": rows[0]["avg_rating"],
            "has_outlets": rows[0]["has_outlets"],
            "has_meeting_rooms": rows[0]["has_meeting_rooms"],
            "has_food": rows[0]["has_food"],
            "has_spacious_seating": rows[0]["has_spacious_seating"],
            "has_printing": rows[0]["has_printing"],
            "has_prayer_space": rows[0]["has_prayer_space"],
            "on_campus": rows[0]["on_campus"],
            "hours": []
        }
        for row in rows:
            spot["hours"].append({
                "day": row["day"],
                "opens": row["opens"],
                "closes": row["closes"]
            })
        return spot
    except Exception as e:
        logger.error(f"Error fetching study spot by ID: {e}")
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
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT r.review_id, \
                       r.user_id, \
                       r.spot_id, \
                       r.review_content, \
                       r.rating, \
                       r.review_img, \
                       r.review_tags, \
                       r.timestamp, \
                       u.user_name, \
                       u.degree, \
                       u.academic_level, \
                       u.bu_college
                FROM reviews r
                         LEFT JOIN users u ON r.user_id = u.user_id
                WHERE r.spot_id = %s
                ORDER BY r.timestamp DESC
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

def get_top_tags_per_spot(limit=3):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT spot_id, LOWER(TRIM(tag)) AS tag, COUNT(*) AS count
            FROM (
                SELECT spot_id, SUBSTRING_INDEX(SUBSTRING_INDEX(review_tags, ',', numbers.n), ',', -1) AS tag
                FROM reviews
                JOIN (
                    SELECT 1 n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8
                ) numbers
                ON CHAR_LENGTH(review_tags)
                   -CHAR_LENGTH(REPLACE(review_tags, ',', '')) >= numbers.n - 1
            ) AS split_tags
            WHERE tag IS NOT NULL AND tag <> ''
            GROUP BY spot_id, tag
            ORDER BY spot_id, count DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Aggregate top unique tags per spot
        from collections import defaultdict
        tag_dict = defaultdict(list)
        seen_tags = defaultdict(set)

        for row in rows:
            spot_id = row['spot_id']
            tag = row['tag']
            if len(tag_dict[spot_id]) < limit and tag not in seen_tags[spot_id]:
                tag_dict[spot_id].append(tag)
                seen_tags[spot_id].add(tag)

        return tag_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

def check_user_review(user_id, spot_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT 1
            FROM reviews
            WHERE user_id = %s AND spot_id = %s
            LIMIT 1
        """
        cursor.execute(query, (user_id, spot_id))
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(f"Error checking if user has reviewed: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        conn.close()
