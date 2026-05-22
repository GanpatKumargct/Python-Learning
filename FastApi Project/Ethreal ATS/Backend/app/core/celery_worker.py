import os
from celery import Celery

# Initialize Celery app
celery_app = Celery(
    "erp_celery",
    broker=os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//"),
    backend=os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def send_email_task(subject: str, body: str, recipient_id: str, context: dict):
    # Phase 1: Mock dispatch logic for Zoho Email API
    print(f"Dispatched email to {recipient_id}: {subject}")
    # Here we would use requests to post to Zoho Email API using ZOHO_EMAIL_TOKEN
    return {"status": "success"}
