"""
Automated Tests for Contact Form API Endpoint
Covers validation, database persistence, email mocking, rate limiting, and spam protection.
"""
from unittest.mock import patch
from fastapi import status
from app.models import ContactMessage


def test_valid_contact_submission_email_success(client, db_session):
    """Test full successful flow: valid input, DB save, email notification sent."""
    payload = {
        "name": "Jane Recruiter",
        "email": "jane@toptech.com",
        "subject": "Interview Request",
        "message": "Hi Karthik, we were very impressed by your portfolio and would like to schedule an interview."
    }

    with patch("app.routers.contact.send_contact_email", return_value=(True, "sent", "")):
        response = client.post("/api/contact", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["email_status"] == "sent"
    assert "sent successfully" in data["message"]
    assert data["ticket_id"] is not None

    # Verify message was persisted in database
    db_record = db_session.query(ContactMessage).filter_by(id=data["ticket_id"]).first()
    assert db_record is not None
    assert db_record.name == "Jane Recruiter"
    assert db_record.email == "jane@toptech.com"
    assert db_record.email_status == "sent"


def test_valid_contact_submission_email_failure(client, db_session):
    """Test that message persists in database even when SMTP dispatch encounters an error."""
    payload = {
        "name": "Sarah Connor",
        "email": "sarah@cyber.io",
        "subject": "Project Collaboration",
        "message": "I would like to discuss building an AI workspace project with you."
    }

    with patch(
        "app.routers.contact.send_contact_email",
        return_value=(False, "failed", "SMTP connection timed out")
    ):
        response = client.post("/api/contact", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["email_status"] == "failed"
    assert "saved securely" in data["message"]
    assert data["ticket_id"] is not None

    # Verify message was preserved in database with failure reason
    db_record = db_session.query(ContactMessage).filter_by(id=data["ticket_id"]).first()
    assert db_record is not None
    assert db_record.email_status == "failed"
    assert db_record.email_error == "SMTP connection timed out"


def test_valid_contact_submission_unconfigured_email(client, db_session):
    """Test that contact form works cleanly when SMTP is not yet configured."""
    payload = {
        "name": "David Brown",
        "email": "david@company.org",
        "subject": "Inquiry Regarding Full-Stack Role",
        "message": "We have an open role for a full-stack Python developer."
    }

    with patch(
        "app.routers.contact.send_contact_email",
        return_value=(False, "unconfigured", "SMTP service is not configured on the server.")
    ):
        response = client.post("/api/contact", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["email_status"] == "unconfigured"
    assert "saved securely" in data["message"]

    # Verify database persistence
    db_record = db_session.query(ContactMessage).filter_by(id=data["ticket_id"]).first()
    assert db_record is not None
    assert db_record.email_status == "unconfigured"


def test_missing_required_fields(client):
    """Test that omitting required fields returns 422 Unprocessable Entity."""
    # Missing email and message
    incomplete_payload = {
        "name": "Incomplete User",
        "subject": "Missing fields"
    }
    response = client.post("/api/contact", json=incomplete_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_invalid_email_format(client):
    """Test that malformed email addresses are rejected with 422."""
    bad_emails = [
        "not-an-email",
        "user@domain",
        "@missinguser.com",
        "spaces in@email.com"
    ]
    for bad_email in bad_emails:
        payload = {
            "name": "Test User",
            "email": bad_email,
            "subject": "Testing bad email",
            "message": "This is a valid length test message body."
        }
        response = client.post("/api/contact", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_empty_or_whitespace_message(client):
    """Test that empty or whitespace-only messages are rejected with 422."""
    payload = {
        "name": "Whitespace Tester",
        "email": "user@example.com",
        "subject": "Whitespace Subject",
        "message": "          "  # 10 spaces
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_message_too_short(client):
    """Test that messages under 10 characters are rejected with 422."""
    payload = {
        "name": "Shorty",
        "email": "short@example.com",
        "subject": "Hello",
        "message": "Too short"  # 9 chars
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_overly_long_fields(client):
    """Test that inputs exceeding maximum boundaries are rejected with 422."""
    payload = {
        "name": "A" * 105,  # Max is 100
        "email": "valid@example.com",
        "subject": "Valid Subject",
        "message": "Valid test message content here."
    }
    response = client.post("/api/contact", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_malformed_json_request(client):
    """Test that non-JSON or malformed payloads return 422 error."""
    response = client.post(
        "/api/contact",
        content="This is not valid JSON",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_honeypot_spam_detected(client, db_session):
    """Test that honeypot field traps bot submissions and skips database write."""
    bot_payload = {
        "name": "Spam Bot",
        "email": "bot@automatedspammer.com",
        "subject": "Buy SEO rankings",
        "message": "Cheap backlinks and traffic for your website.",
        "_gotcha": "hidden_bot_field_filled"
    }

    with patch("app.routers.contact.send_contact_email") as mock_email:
        response = client.post("/api/contact", json=bot_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["email_status"] == "skipped_spam"
    assert data["ticket_id"] is None

    # Verify no email was dispatched
    mock_email.assert_not_called()

    # Verify no database record was created
    count = db_session.query(ContactMessage).count()
    assert count == 0


def test_rate_limiting(client):
    """Test that exceeding RATE_LIMIT_MAX_REQUESTS triggers HTTP 429."""
    valid_payload = {
        "name": "Rate Tester",
        "email": "rate@example.com",
        "subject": "Rate Limit Test",
        "message": "Testing submission threshold for abuse prevention."
    }

    with patch("app.routers.contact.send_contact_email", return_value=(True, "sent", "")):
        # Submit 5 allowed requests
        for i in range(5):
            res = client.post("/api/contact", json=valid_payload)
            assert res.status_code == status.HTTP_200_OK

        # 6th request must trigger 429 Too Many Requests
        blocked_res = client.post("/api/contact", json=valid_payload)
        assert blocked_res.status_code == status.HTTP_429_TOO_MANY_REQUESTS
        assert "Too many requests" in blocked_res.json()["detail"]


def test_no_secrets_in_error_responses(client):
    """Verify that error responses do not leak server passwords or environment secrets."""
    payload = {
        "name": "T",  # Invalid short name
        "email": "invalid",
        "subject": "S",
        "message": "short"
    }
    response = client.post("/api/contact", json=payload)
    text = response.text
    assert "SMTP_PASSWORD" not in text
    assert "SECRET" not in text
    assert "password" not in text.lower()
