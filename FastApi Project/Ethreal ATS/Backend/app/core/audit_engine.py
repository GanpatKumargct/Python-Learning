import uuid
from sqlalchemy.orm import Session
from app.Model import models
from typing import Any, Dict, Optional

class AuditEngine:
    def __init__(self, db: Session):
        self.db = db

    def log(self, 
            entity_name: str, 
            entity_id: str, 
            actor_id: Optional[str], 
            event_type: str, 
            old_value: Optional[Dict[str, Any]] = None, 
            new_value: Optional[Dict[str, Any]] = None, 
            metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Append-only, immutable log of every significant event.
        Returns the ID of the created audit log entry.
        """
        audit_entry = models.AuditLog(
            id=str(uuid.uuid4()),
            entity_name=entity_name,
            entity_id=entity_id,
            actor_id=actor_id,
            event_type=event_type,
            old_value=old_value,
            new_value=new_value,
            metadata_col=metadata
        )
        self.db.add(audit_entry)
        self.db.commit()
        return audit_entry.id

    def query(self, entity_name: str, entity_id: str):
        """
        Query audit logs for a specific entity record.
        """
        return self.db.query(models.AuditLog).filter(
            models.AuditLog.entity_name == entity_name,
            models.AuditLog.entity_id == entity_id
        ).order_by(models.AuditLog.occurred_at.desc()).all()

def get_audit_engine(db: Session) -> AuditEngine:
    return AuditEngine(db)
