"""
Application Configuration Module
Loads settings from environment variables and provides sensible defaults.
"""
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv

# Resolve base directories
BACKEND_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BACKEND_DIR.parent

# Load .env file from backend directory if present, fallback to workspace directory
env_path = BACKEND_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    workspace_env = WORKSPACE_DIR / ".env"
    if workspace_env.exists():
        load_dotenv(dotenv_path=workspace_env)


class Settings:
    """Central configuration class for backend application."""

    # Application Info
    APP_NAME: str = os.getenv("APP_NAME", "Karthik Portfolio API")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

    # Database Configuration
    # Default: persistent SQLite database in the backend directory
    DEFAULT_DB_FILE = BACKEND_DIR / "portfolio.db"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DEFAULT_DB_FILE.as_posix()}"
    )

    # CORS Allowed Origins
    _raw_origins: str = os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:5500,http://localhost:5500,http://127.0.0.1:8000,http://localhost:8000,http://127.0.0.1:3000,http://localhost:3000"
    )

    @property
    def FRONTEND_ORIGINS(self) -> List[str]:
        """Parse comma-separated origins into a list of strings."""
        return [origin.strip() for origin in self._raw_origins.split(",") if origin.strip()]

    # SMTP Email Configuration
    SMTP_HOST: str = os.getenv("SMTP_HOST", "").strip()
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "").strip()
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "").strip()
    SMTP_USE_TLS: bool = os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes")
    SMTP_TIMEOUT: int = int(os.getenv("SMTP_TIMEOUT", "10"))
    
    # Sender and Recipient Email Addresses
    SENDER_EMAIL: str = os.getenv("SENDER_EMAIL", "").strip()
    RECIPIENT_EMAIL: str = os.getenv(
        "RECIPIENT_EMAIL",
        "karanamvenkatjaykarthik@gmail.com"
    ).strip()

    # Rate Limiting & Abuse Prevention
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "5"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "600"))

    # Request Size Limits (Bytes) - default 64 KB
    MAX_REQUEST_SIZE_BYTES: int = int(os.getenv("MAX_REQUEST_SIZE_BYTES", "65536"))

    def is_smtp_configured(self) -> bool:
        """
        Check if SMTP is fully configured with required credentials.
        Returns False if any required setting is missing.
        """
        return bool(
            self.SMTP_HOST
            and self.SMTP_PORT
            and self.SMTP_USERNAME
            and self.SMTP_PASSWORD
            and self.SENDER_EMAIL
            and self.RECIPIENT_EMAIL
        )


settings = Settings()
