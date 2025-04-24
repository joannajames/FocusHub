import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="focushub_user",
        password="SQLPassCod3!",
        database="study_spots_db",
        auth_plugin = 'mysql_native_password'
    )