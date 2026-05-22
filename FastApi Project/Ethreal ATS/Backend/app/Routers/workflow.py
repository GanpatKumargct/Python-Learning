from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict
from pydantic import BaseModel
from app.Database.database import get_db
from app.Model import models
from app.core.auth import verify_zoho_sso_token
from app.core.workflow_engine import get_workflow_engine

router = APIRouter(
    prefix="/workflow",
    tags=["workflow"]
)

class TransitionPayload(BaseModel):
    instance_id: str
    transition_name: str
    payload: Dict[str, Any]
    idempotency_key: str

@router.post("/transition")
def trigger_transition(payload: TransitionPayload, db: Session = Depends(get_db), actor: models.Actor = Depends(verify_zoho_sso_token)):
    we = get_workflow_engine(db)
    result = we.transition(
        instance_id=payload.instance_id,
        transition_name=payload.transition_name,
        actor_id=actor.id,
        payload=payload.payload,
        idempotency_key=payload.idempotency_key
    )
    if not result.ok:
        raise HTTPException(status_code=400, detail=result.errors)
        
    return {"status": "success", "new_state": result.new_state}
