import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def _send_email_sync(to_email: str, subject: str, body_html: str):
    """
    Synchronous email sender.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.info("SMTP settings not configured. Printing email to console.")
        print(f"=========================================")
        print(f"DEBUG EMAIL to {to_email}: {subject}")
        print(f"BODY:\n{body_html}")
        print(f"=========================================")
        return

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = f"{settings.EMAIL_FROM_NAME} <{settings.SMTP_USER}>"
    msg['To'] = to_email

    part2 = MIMEText(body_html, 'html')
    msg.attach(part2)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, to_email, msg.as_string())
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")

async def send_email(to_email: str, subject: str, body_html: str):
    """
    Asynchronously sends an email by running the synchronous sender in a separate thread.
    This can be used globally across all modules (auth, ats, etc.).
    """
    await asyncio.to_thread(_send_email_sync, to_email, subject, body_html)
