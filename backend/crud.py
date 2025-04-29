from database import get_db_connection
import logging
from fastapi import HTTPException

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#SPOTS LOGIC
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


#Get Spot by ID

def get_study_spot_by_id(spot_id: int):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                s.*,
                h.opens AS open_time,
                h.closes AS close_time,
                h.day
            FROM spots s
            JOIN hours h ON s.spot_id = h.spot_id
            WHERE s.spot_id = %s
        """
        cursor.execute(query, (spot_id,))
        spot_rows = cursor.fetchall()

        return spot_rows  # Could be multiple rows (one for each day)
    except Exception as e:
        import traceback
        print("DB ERROR:", e)
        traceback.print_exc()
        raise
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
                spot_name, address, has_outlets, has_food,
                has_printing, has_prayer_space, has_spacious_seating,
                has_meeting_rooms, on_campus, default_img_url, average_rating
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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


#REVIEW LOGIC
# Add a new review       
def add_review(user_id, spot_id, rating, review_content, review_tags, review_img_url):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO reviews (user_id, spot_id, rating, review_content, review_tags, review_img_url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (user_id, spot_id, rating, review_content, review_tags, review_img_url)
        cursor.execute(query, values)
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
# Fetch all reviews for a specific spot
def get_reviews_for_spot(spot_id):
    print(spot_id)
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        logger.info(f"Fetching reviews for spot_id={spot_id}")
        query = """
            SELECT 
                reviews.review_id,
                reviews.user_id,
                users.user_name,
                users.degree,
                users.academic_level,
                users.bu_college,
                reviews.spot_id,
                reviews.review_content,
                reviews.rating,
                reviews.review_img,
                reviews.review_tags,
                reviews.timestamp
            FROM reviews
            JOIN users ON reviews.user_id = users.user_id 
            WHERE reviews.spot_id = %s
            ORDER BY reviews.timestamp DESC
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


#USER LOGIC
def check_or_add_user(email: str):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT user_id FROM users WHERE bu_user_id = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            logger.info(f"User {email} already exists with user_id {user['user_id']}")
            return user['user_id']
        else:
            insert_query = """
                INSERT INTO users (bu_user_id, user_name)
                VALUES (%s, %s)
            """
            cursor.execute(insert_query, (email, email))  # same email for both fields initially
            conn.commit()
            logger.info(f"New user {email} added with user_id {cursor.lastrowid}")
            return cursor.lastrowid

    except Exception as e:
        logger.error(f"Error checking or adding user: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
def update_user_profile(user_id: int, degree: str, academic_level: str, bu_college: str):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE users
            SET degree = %s,
                academic_level = %s,
                bu_college = %s
            WHERE user_id = %s
        """
        values = (degree, academic_level, bu_college, user_id)
        cursor.execute(query, values)
        conn.commit()
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_user_info_by_email(email: str):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT user_id, bu_user_id, user_name, degree, academic_level, bu_college
            FROM users
            WHERE bu_user_id = %s
        """
        cursor.execute(query, (email,))
        user_info = cursor.fetchone()
        return user_info
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
