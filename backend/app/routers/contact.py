"""
Contact Form Submission Router
Handles input validation, database persistence, email dispatch, and response formatting.
"""
import logging
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ContactMessage
from app.schemas import ContactCreate, ContactResponse
from app.dependencies import check_contact_rate_limit
from app.email_service import send_contact_email

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/contact",
    response_model=ContactResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_contact_rate_limit)],
    summary="Submit Contact Message",
    description="Validates and persists a visitor inquiry in the database and dispatches an email notification."
)
async def submit_contact_form(
    payload: ContactCreate,
    db: Session = Depends(get_db)
):
    # 1. Anti-Spam Honeypot Verification
    if payload.gotcha or payload.honeypot:
        logger.info("Spam submission intercepted by honeypot field. Skipping persistence.")
        # Silent success response to avoid informing the automated bot
        return ContactResponse(
            status="success",
            message="Your message has been received.",
            email_status="skipped_spam",
            ticket_id=None
        )

    # 2. Database Persistence
    # Create the contact message record with initial status 'pending'
    contact_record = ContactMessage(
        name=payload.name,
        email=payload.email,
        subject=payload.subject,
        message=payload.message,
        email_status="pending"
    )

    try:
        db.add(contact_record)
        db.commit()
        db.refresh(contact_record)
        logger.info(f"Contact message #{contact_record.id} stored in database.")
    except Exception as exc:
        db.rollback()
        logger.error(f"Database error saving contact message: {exc.__class__.__name__}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "error",
                "message": "Unable to save your message right now. Please try again later or contact directly."
            }
        )

    # 3. Notification Email Dispatch
    # Sent outside the active DB transaction to avoid blocking the database
    email_success, email_status, email_error = send_contact_email(
        name=payload.name,
        visitor_email=payload.email,
        subject=payload.subject,
        message=payload.message
    )

    # 4. Update Email Status in Database
    try:
        contact_record.email_status = email_status
        contact_record.email_error = email_error if email_error else None
        db.commit()
    except Exception as exc:
        db.rollback()
        logger.warning(f"Failed to update email status for record #{contact_record.id}: {exc}")

    # 5. Formulate Truthful User Feedback
    if email_status == "sent":
        user_message = "Your message has been sent successfully. Thank you for reaching out!"
    elif email_status == "unconfigured":
        user_message = (
            "Your message has been received and saved securely in our database. "
            "(Server email notification is currently unconfigured)."
        )
    else:  # email_status == "failed"
        user_message = (
            "Your message has been received and saved securely in our database, "
            "though notification email dispatch encountered an issue."
        )

    return ContactResponse(
        status="success",
        message=user_message,
        email_status=email_status,
        ticket_id=contact_record.id
    )
