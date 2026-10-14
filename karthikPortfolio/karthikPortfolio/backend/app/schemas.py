"""
Pydantic Validation Schemas
Validates incoming contact submissions and formats outgoing API responses.
"""
import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class ContactCreate(BaseModel):
    """
    Schema for validating contact form submissions.
    Enforces non-empty values, trimmed strings, email format, and field boundaries.
    """
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the sender"
    )
    email: str = Field(
        ...,
        min_length=5,
        max_length=254,
        description="Valid email address of the sender"
    )
    subject: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Subject of the message"
    )
    message: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Body content of the message"
    )

    # Honeypot spam fields (should remain empty if submitted by real humans)
    gotcha: Optional[str] = Field(default=None, alias="_gotcha")
    honeypot: Optional[str] = Field(default=None)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Name cannot be empty or whitespace only.")
        if len(trimmed) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return trimmed

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Email cannot be empty.")
        if not EMAIL_REGEX.match(trimmed):
            raise ValueError("Please provide a valid email address (e.g. user@example.com).")
        return trimmed.lower()

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Subject cannot be empty or whitespace only.")
        if len(trimmed) < 3:
            raise ValueError("Subject must be at least 3 characters long.")
        # Prevent CRLF header injection in email subjects
        sanitized = re.sub(r"[\r\n]+", " ", trimmed)
        return sanitized

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        trimmed = v.strip()
        if not trimmed:
            raise ValueError("Message cannot be empty or whitespace only.")
        if len(trimmed) < 10:
            raise ValueError("Message must contain at least 10 characters.")
        return trimmed


class ContactResponse(BaseModel):
    """
    Schema for contact submission response.
    Truthfully reports both database persistence and email notification status.
    """
    status: str = Field(..., description="'success' or 'error'")
    message: str = Field(..., description="User-facing descriptive feedback")
    email_status: str = Field(
        ...,
        description="Status of email notification: 'sent', 'failed', 'unconfigured', or 'skipped_spam'"
    )
    ticket_id: Optional[int] = Field(default=None, description="Persisted message reference ID")


class HealthResponse(BaseModel):
    """Schema for basic application health check."""
    status: str
    service: str
    timestamp: datetime


class DBHealthResponse(BaseModel):
    """Schema for database connectivity health check."""
    status: str
    database: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Standardized error response schema."""
    status: str = "error"
    message: str
