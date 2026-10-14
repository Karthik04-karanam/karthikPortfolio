"""
SQLAlchemy ORM Models
Defines the ContactMessage table and related schema.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from app.database import Base


class ContactMessage(Base):
    """
    Model representing a contact form submission.
    Persists visitor inquiries and records email notification delivery status.
    """
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(254), nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    email_status = Column(
        String(50),
        nullable=False,
        default="pending"  # "pending", "sent", "failed", "unconfigured", "skipped_spam"
    )
    email_error = Column(Text, nullable=True)

    __table_args__ = (
        Index("ix_contact_messages_email_created", "email", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<ContactMessage(id={self.id}, name='{self.name}', email='{self.email}', status='{self.email_status}')>"
