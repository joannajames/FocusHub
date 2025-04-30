import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        auth_plugin= 'mysql_native_password'
    )
    return connection

