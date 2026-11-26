import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health")
def health_check(response: Response, session: Session = Depends(get_db)) -> dict[str, str]:
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.exception("Database health check failed")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "unavailable"}
    return {"status": "ok", "database": "ok"}
