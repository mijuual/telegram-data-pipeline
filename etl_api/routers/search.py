from fastapi import APIRouter
from db import get_db_connection
from schemas import MessageResult
from typing import List

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("/messages", response_model=List[MessageResult])
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
    rows = cur.fetchall()
    conn.close()
    return [MessageResult(
        message_id=row[0],
        channel_title=row[1],
        message_text=row[2],
        date=row[3]
    ) for row in rows]
