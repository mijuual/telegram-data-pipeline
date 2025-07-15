# routers/reports.py

from fastapi import APIRouter
from db import get_db_connection

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/top-products")
def top_products(limit: int = 10):
    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        SELECT object_class, COUNT(*) AS mentions
        FROM fct_image_detections
        GROUP BY object_class
        ORDER BY mentions DESC
        LIMIT %s
    """
    cur.execute(query, (limit,))
    result = cur.fetchall()
    conn.close()
    return {"top_products": result}
