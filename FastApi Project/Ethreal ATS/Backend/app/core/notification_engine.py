import uuid
from sqlalchemy.orm import Session
from app.Model import models
from typing import List, Dict, Any

class NotificationEngine:
    def __init__(self, db: Session):
        self.db = db

    def dispatch(self, template_name: str, recipients: List[str], context: Dict[str, Any], idempotency_key: str):
        """
        Dispatches notifications async.
        """
        # Check idempotency
        existing_log = self.db.query(models.NotificationLog).filter(
            models.NotificationLog.idempotency_key == idempotency_key
        ).first()
        if existing_log:
            return  # Skip, already dispatched
            
        # Load template
        template = self.db.query(models.NotificationTemplate).filter(
            models.NotificationTemplate.name == template_name,
            models.NotificationTemplate.is_active == True
        ).first()
        
        if not template:
            # If no template found, we can't send, but we might log a failure
            return
            
        for recipient_id in recipients:
            # Enqueue to Celery 
            from app.core.celery_worker import send_email_task
            send_email_task.delay(template.subject, template.body_text, recipient_id, context)
            
            # Write delivery outcome to log
            log = models.NotificationLog(
                id=str(uuid.uuid4()),
                idempotency_key=f"{idempotency_key}_{recipient_id}",
                template_name=template_name,
                recipient_id=recipient_id,
                channel=template.channel,
                status="sent"
            )
            self.db.add(log)
            
        self.db.commit()

def get_notification_engine(db: Session) -> NotificationEngine:
    return NotificationEngine(db)
