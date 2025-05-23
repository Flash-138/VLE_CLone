import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "host":       os.getenv("DB_HOST"),
    "user":       os.getenv("DB_USER"),
    "password":   os.getenv("DB_PASS"),
    "database":   os.getenv("DB_NAME"),
    "port":       int(os.getenv("DB_PORT", 3306)),
}

def get_db_connection():
    return mysql.connector.connect(**db_config)
