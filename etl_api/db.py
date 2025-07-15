# db.py

import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="raw",
        user="postgres",
        password="root"
    )
    return conn
