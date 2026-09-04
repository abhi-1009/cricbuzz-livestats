import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import sys
import os

load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import get_secret


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=get_secret("MYSQL_HOST", "localhost"),
            port=int(get_secret("MYSQL_PORT", 3306)),
            user=get_secret("MYSQL_USER", "root"),
            password=get_secret("MYSQL_PASSWORD"),
            database=get_secret("MYSQL_DATABASE", "cricbuzz_livestats")
        )
        return conn
    except Error as e:
        print(f"Database connection failed: {e}")
        return None


if __name__ == "__main__":
    conn = get_connection()
    if conn and conn.is_connected():
        print("Connected to MySQL successfully")
        conn.close()
    else:
        print("Connection failed")
