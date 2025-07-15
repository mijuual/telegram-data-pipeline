# routers/channels.py

from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/api/channels", tags=["Channels"])

@router.get("/{channel_name}/activity")
def channel_activity(channel_name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT d.date, COUNT(*) as message_count
        FROM fct_messages f
        JOIN dim_channels c ON f.channel_id = c.channel_id
        JOIN dim_dates d ON f.date_id = d.date
        WHERE c.channel_title = %s
        GROUP BY d.date
        ORDER BY d.date
    """
    cur.execute(query, (channel_name,))
    result = cur.fetchall()
    conn.close()
    return {"activity": result}
