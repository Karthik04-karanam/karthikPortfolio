"""
Tests for Database Operations and ContactMessage Model
"""
import pytest
from sqlalchemy.exc import IntegrityError
from app.models import ContactMessage


def test_create_contact_message(db_session):
    """Test creating a ContactMessage record and verifying all fields."""
    msg = ContactMessage(
        name="Test Recruiter",
        email="recruiter@techcorp.com",
        subject="Senior Developer Opportunity",
        message="Hello Karthik, we reviewed your projects and would like to discuss a position.",
        email_status="pending"
    )
    db_session.add(msg)
    db_session.commit()
    db_session.refresh(msg)

    assert msg.id is not None
    assert msg.name == "Test Recruiter"
    assert msg.email == "recruiter@techcorp.com"
    assert msg.subject == "Senior Developer Opportunity"
    assert msg.created_at is not None
    assert msg.email_status == "pending"
    assert msg.email_error is None


def test_contact_message_persistence(db_session):
    """Test that records persist and can be queried back accurately."""
    msg = ContactMessage(
        name="Alex Smith",
        email="alex@startup.io",
        subject="Contract Project",
        message="Interested in working together on a Python FastAPI project.",
        email_status="sent"
    )
    db_session.add(msg)
    db_session.commit()

    # Query from database
    retrieved = db_session.query(ContactMessage).filter_by(email="alex@startup.io").first()
    assert retrieved is not None
    assert retrieved.name == "Alex Smith"
    assert retrieved.email_status == "sent"


def test_contact_message_email_status_update(db_session):
    """Test updating email status and storing sanitized error info."""
    msg = ContactMessage(
        name="Jordan Lee",
        email="jordan@agency.com",
        subject="Inquiry",
        message="Would like to know more about your availability.",
        email_status="pending"
    )
    db_session.add(msg)
    db_session.commit()

    # Update to failed with error
    msg.email_status = "failed"
    msg.email_error = "SMTP connection timed out"
    db_session.commit()

    updated = db_session.query(ContactMessage).filter_by(id=msg.id).first()
    assert updated.email_status == "failed"
    assert updated.email_error == "SMTP connection timed out"


def test_contact_message_missing_required_fields(db_session):
    """Test that missing non-nullable fields raises IntegrityError."""
    bad_msg = ContactMessage(
        name=None,  # Nullable=False
        email="broken@test.com",
        subject="Broken",
        message="Content"
    )
    db_session.add(bad_msg)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
