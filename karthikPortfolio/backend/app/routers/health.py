"""
Health Check Endpoints
Provides system liveness and database connectivity status.
"""
from datetime import datetime, timezone
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import HealthResponse, DBHealthResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Application Health Status",
    description="Check whether the FastAPI backend application is running."
)
async def check_app_health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="portfolio-backend",
        timestamp=datetime.now(timezone.utc)
    )


@router.get(
    "/health/db",
    response_model=DBHealthResponse,
    summary="Database Connectivity Status",
    description="Check whether the application can successfully query the database."
)
async def check_database_health(db: Session = Depends(get_db)):
    try:
        # Simple test query that works across SQLite, PostgreSQL, and MySQL
        db.execute(text("SELECT 1"))
        return DBHealthResponse(
            status="healthy",
            database="connected",
            timestamp=datetime.now(timezone.utc)
        )
    except Exception as exc:
        # Log generic failure without leaking credentials or private schema
        logger.error(f"Database health check failed: {exc.__class__.__name__}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )
