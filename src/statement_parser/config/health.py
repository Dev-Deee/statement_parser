from fastapi import APIRouter, Response
from sqlalchemy import text

from statement_parser.config.database import engine
from statement_parser.config.redis import redis_client

router = APIRouter()


@router.get("/health")
def health(response: Response):
    status = {"database": "up", "redis": "up"}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception:
        status["database"] = "down"
    try:
        redis_client.ping()
    except Exception:
        status["redis"] = "down"

    if "down" in status.values():
        response.status_code = 503
    return status