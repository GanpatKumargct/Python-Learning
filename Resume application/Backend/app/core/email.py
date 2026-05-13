import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
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
    msg['From'] = f"{settings.EMAIL_FROM_NAME} <{settings.OTP_EMAIL_SENDER}>"
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

async def send_templated_email(db: AsyncSession, to_email: str, template_name: str, context: dict, fallback_subject: str = "", fallback_body: str = ""):
    from app.shared.emails.models import EmailTemplate
    result = await db.execute(select(EmailTemplate).where(EmailTemplate.name == template_name))
    template = result.scalar_one_or_none()

    if template and template.is_active:
        subject = template.subject.format(**context)
        body_html = template.body_html.format(**context)
    else:
        if not fallback_subject or not fallback_body:
            logger.warning(f"Email template '{template_name}' not found and no fallback provided.")
            return
        subject = fallback_subject.format(**context)
        body_html = fallback_body.format(**context)

    await send_email(to_email, subject, body_html)
