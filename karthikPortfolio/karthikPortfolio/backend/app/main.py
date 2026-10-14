"""
Main FastAPI Application Entrypoint
Configures CORS, middleware, routers, lifespan database initialization, and root endpoints.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import init_db
from app.routers import health, contact

# Configure application logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("portfolio.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler.
    Initializes database schema on startup and performs clean teardown.
    """
    logger.info("Initializing database tables...")
    try:
        init_db()
        logger.info("Database schema initialized successfully.")
    except Exception as exc:
        logger.error(f"Critical error initializing database: {exc}")
    yield
    logger.info("Shutting down portfolio backend service.")


# FastAPI Application instance
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API and SQLite database service for Karthik's Developer Portfolio",
    version="1.0.0",
    lifespan=lifespan
)

# 1. Request Body Size Limiting Middleware
@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.MAX_REQUEST_SIZE_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "status": "error",
                "message": f"Request body exceeds maximum allowed size ({settings.MAX_REQUEST_SIZE_BYTES} bytes)."
            }
        )
    return await call_next(request)


# 2. CORS (Cross-Origin Resource Sharing) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=600
)


# 3. Mount Routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(contact.router, prefix="/api", tags=["Contact"])


# 4. Root Service Status Endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root Status",
    description="Returns the status of the portfolio backend service."
)
async def root_status():
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs",
        "health_check": "/api/health"
    }
