from fastapi import APIRouter
from db import get_db_connection
from schemas import TopProduct
from typing import List

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/top-products", response_model=List[TopProduct])
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
    rows = cur.fetchall()
    conn.close()
    return [TopProduct(object_class=row[0], mentions=row[1]) for row in rows]
