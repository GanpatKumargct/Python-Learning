from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional
import uuid
from app.Database.database import get_db
from app.Model import models
from pydantic import BaseModel
from app.core.auth import verify_zoho_sso_token_optional, verify_zoho_sso_token
from app.core.permissions import get_permission_engine

router = APIRouter(
    prefix="/entity",
    tags=["entity"]
)

class RecordCreate(BaseModel):
    data: Dict[str, Any]

@router.post("/{entity_name}/records")
def create_record(entity_name: str, payload: RecordCreate, 
                  db: Session = Depends(get_db), 
                  actor: Optional[models.Actor] = Depends(verify_zoho_sso_token_optional)):
    
    # Permission bypass for candidates
    if entity_name != "candidate":
        if not actor:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        # Check permissions
        pe = get_permission_engine(db)
        decision = pe.evaluate(actor.id, "create", entity_name)
        if decision.effect == "deny":
            raise HTTPException(status_code=403, detail=decision.reason)

    # Phase 1: Hardcoded to our entities
    record = None
    if entity_name == "candidate":
        record = models.CandidateRecord(id=str(uuid.uuid4()), data=payload.data)
    elif entity_name == "job_requisition":
        record = models.JobRequisitionRecord(id=str(uuid.uuid4()), data=payload.data)
    elif entity_name == "interview":
        record = models.InterviewRecord(id=str(uuid.uuid4()), data=payload.data)
    elif entity_name == "feedback":
        record = models.FeedbackRecord(id=str(uuid.uuid4()), data=payload.data)
    elif entity_name == "offer":
        record = models.OfferRecord(id=str(uuid.uuid4()), data=payload.data)
    elif entity_name == "referee":
        record = models.RefereeRecord(id=str(uuid.uuid4()), data=payload.data)
    else:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    db.add(record)
    db.commit()
    db.refresh(record)
    
    # We should also spin up a workflow instance here
    wf_def = db.query(models.WorkflowDefinition).filter(models.WorkflowDefinition.entity_name == entity_name).first()
    if wf_def:
        # Find initial state
        init_state = db.query(models.WorkflowState).filter(
            models.WorkflowState.definition_id == wf_def.id,
            models.WorkflowState.is_initial == True
        ).first()
        
        if init_state:
            wf_inst = models.WorkflowInstance(
                id=str(uuid.uuid4()),
                definition_id=wf_def.id,
                record_id=record.id,
                entity_name=entity_name,
                current_state_id=init_state.id,
                context=payload.data
            )
            db.add(wf_inst)
            
            # Log event
            wf_event = models.WorkflowEvent(
                id=str(uuid.uuid4()),
                instance_id=wf_inst.id,
                idempotency_key=str(uuid.uuid4()),
                from_state="NONE",
                to_state=init_state.name,
                transition_name="system_init"
            )
            db.add(wf_event)
            db.commit()
            
    return {"record_id": record.id, "status": "created"}

@router.get("/{entity_name}/records")
def list_records(entity_name: str, db: Session = Depends(get_db), actor: models.Actor = Depends(verify_zoho_sso_token)):
    # Check permissions
    pe = get_permission_engine(db)
    decision = pe.evaluate(actor.id, "read", entity_name)
    if decision.effect == "deny":
        raise HTTPException(status_code=403, detail=decision.reason)

    if entity_name == "candidate":
        records = db.query(models.CandidateRecord).all()
    elif entity_name == "job_requisition":
        records = db.query(models.JobRequisitionRecord).all()
    elif entity_name == "interview":
        records = db.query(models.InterviewRecord).all()
    elif entity_name == "feedback":
        records = db.query(models.FeedbackRecord).all()
    elif entity_name == "offer":
        records = db.query(models.OfferRecord).all()
    elif entity_name == "referee":
        records = db.query(models.RefereeRecord).all()
    else:
        raise HTTPException(status_code=404, detail="Entity not found")
        
    return [{"id": r.id, "data": r.data, "created_at": r.created_at} for r in records]
