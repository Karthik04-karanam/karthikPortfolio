"""
Database Engine, Session, and Base Declaration
Uses SQLAlchemy 2.x with SQLite by default and easily adaptable to PostgreSQL.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import settings

# Engine configuration
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a database session per request.
    Ensures session is always closed upon completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables defined in models.
    Safe to call repeatedly - will not overwrite existing tables.
    """
    # Import models here so Base knows about them before creation
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
