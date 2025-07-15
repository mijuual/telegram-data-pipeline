# routers/search.py

from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("/messages")
def search_messages(query: str):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """
        SELECT f.message_id, c.channel_title, f.message_text, d.date
        FROM fct_messages f
        JOIN dim_channels c ON f.channel_id = c.channel_id
        JOIN dim_dates d ON f.date_id = d.date
        WHERE f.message_text ILIKE %s
        ORDER BY d.date DESC
        LIMIT 50
    """
    cur.execute(sql, (f"%{query}%",))
    result = cur.fetchall()
    conn.close()
    return {"results": result}
