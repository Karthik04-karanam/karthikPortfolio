"""
Email Delivery Service
Manages SMTP transport, message construction, HTML formatting, and error sanitization.
"""
import html
import logging
import smtplib
import socket
from email.message import EmailMessage
from typing import Tuple
from app.config import settings

logger = logging.getLogger(__name__)


def send_contact_email(
    name: str,
    visitor_email: str,
    subject: str,
    message: str
) -> Tuple[bool, str, str]:
    """
    Attempt to deliver an email notification for a new contact message.

    Returns:
        (success: bool, status: str, error_message: str)
        status values: "sent", "unconfigured", "failed"
    """
    # 1. Check if SMTP configuration is present
    if not settings.is_smtp_configured():
        logger.info(
            "SMTP is not configured on this server. Contact message will be stored in database only."
        )
        return (
            False,
            "unconfigured",
            "SMTP email service is not configured on the server."
        )

    # 2. Build the Email Message
    msg = EmailMessage()
    msg["Subject"] = f"[Portfolio Contact] {subject}"
    msg["From"] = settings.SENDER_EMAIL
    msg["To"] = settings.RECIPIENT_EMAIL
    msg["Reply-To"] = visitor_email

    # Plain text fallback
    plain_content = (
        f"New Contact Message from Portfolio Website\n"
        f"-----------------------------------------\n"
        f"Name:       {name}\n"
        f"Email:      {visitor_email}\n"
        f"Subject:    {subject}\n"
        f"-----------------------------------------\n\n"
        f"Message:\n{message}\n\n"
        f"-----------------------------------------\n"
        f"Reply directly to this email to respond to {name} ({visitor_email}).\n"
    )
    msg.set_content(plain_content)

    # Safe HTML body with escaped visitor content
    safe_name = html.escape(name)
    safe_email = html.escape(visitor_email)
    safe_subject = html.escape(subject)
    safe_message = html.escape(message).replace("\n", "<br/>")

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1e293b; line-height: 1.6; margin: 0; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; }}
    .header {{ background: #0f172a; color: #00d2ff; padding: 20px; border-bottom: 3px solid #00d2ff; }}
    .header h2 {{ margin: 0; font-size: 18px; }}
    .content {{ padding: 24px; }}
    .field {{ margin-bottom: 12px; }}
    .label {{ font-size: 12px; font-weight: bold; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}
    .value {{ font-size: 15px; color: #0f172a; font-weight: 500; margin-top: 2px; }}
    .message-box {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 16px; margin-top: 16px; font-size: 14px; color: #334155; line-height: 1.6; }}
    .footer {{ background: #f1f5f9; padding: 14px 24px; font-size: 12px; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>New Portfolio Inquiry</h2>
    </div>
    <div class="content">
      <div class="field">
        <div class="label">Sender Name</div>
        <div class="value">{safe_name}</div>
      </div>
      <div class="field">
        <div class="label">Sender Email</div>
        <div class="value"><a href="mailto:{safe_email}">{safe_email}</a></div>
      </div>
      <div class="field">
        <div class="label">Subject</div>
        <div class="value">{safe_subject}</div>
      </div>
      <div class="field">
        <div class="label">Message</div>
        <div class="message-box">{safe_message}</div>
      </div>
    </div>
    <div class="footer">
      Sent via Karthik Portfolio Contact Form • Reply directly to this email to contact {safe_name}.
    </div>
  </div>
</body>
</html>"""
    msg.add_alternative(html_content, subtype="html")

    # 3. Transport via SMTP
    try:
        if settings.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                timeout=settings.SMTP_TIMEOUT
            )
        else:
            server = smtplib.SMTP(
                settings.SMTP_HOST,
                settings.SMTP_PORT,
                timeout=settings.SMTP_TIMEOUT
            )

        with server:
            if settings.SMTP_USE_TLS and settings.SMTP_PORT != 465:
                server.starttls()
            if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info(f"Notification email dispatched successfully for {visitor_email}.")
        return (True, "sent", "")

    except smtplib.SMTPAuthenticationError:
        error_msg = "SMTP Authentication failed: check username/password."
        logger.warning("SMTP Authentication failed.")
        return (False, "failed", error_msg)

    except (smtplib.SMTPConnectError, socket.timeout, TimeoutError):
        error_msg = "SMTP connection timed out or server unreachable."
        logger.warning(f"SMTP Connection timeout connecting to {settings.SMTP_HOST}.")
        return (False, "failed", error_msg)

    except smtplib.SMTPException as exc:
        # Sanitize exception message so internal details are not exposed
        error_msg = f"SMTP protocol error: {exc.__class__.__name__}"
        logger.warning(f"SMTP error occurred: {error_msg}")
        return (False, "failed", error_msg)

    except Exception as exc:
        error_msg = f"Unexpected email transport error: {exc.__class__.__name__}"
        logger.error(f"Unexpected error in email dispatch: {error_msg}")
        return (False, "failed", error_msg)
