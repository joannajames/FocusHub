from idlelib.query import Query

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector

app = FastAPI()

# ✅ CORS Middleware (must be before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vue frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/study_spots")
def get_study_spots():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLPassCod3!",
        database="study_spots_db"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, location AS address, hours FROM study_spots")

    spots = cursor.fetchall()
    cursor.close()
    conn.close()

    return spots

# NEW: Search route
@app.get("/study_spots/search")
def search_study_spots(q: str = Query(...)):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLPassCod3!",
        database="study_spots_db"
    )
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT id, name, location AS address, hours
    FROM study_spots
    WHERE LOWER(name) LIKE %s OR LOWER(location) LIKE %s
    """
    cursor.execute(query, (f"%{q.lower()}%", f"%{q.lower()}%"))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results