import mysql.connector


# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLPassCod3!",
        database="study_spots_db"
    )


# Function to fetch study spots from the database
def get_all_study_spots():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, location AS address, hours FROM study_spots")

    spots = cursor.fetchall()

    cursor.close()
    conn.close()

    return spots
