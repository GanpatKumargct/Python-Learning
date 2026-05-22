from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Any, Dict, Optional
from app.Database.database import get_db
from app.Model import models
from app.core.auth import verify_zoho_sso_token, verify_zoho_sso_token_optional
from app.core.form_engine import get_form_engine
from app.core.permissions import get_permission_engine

router = APIRouter(
    prefix="/form",
    tags=["form"]
)

@router.get("/render/{entity_name}")
def render_form(entity_name: str, record_id: Optional[str] = None, db: Session = Depends(get_db), actor: Optional[models.Actor] = Depends(verify_zoho_sso_token_optional)):
    
    # Bypass for candidates applying publicly
    if entity_name != "candidate" and not actor:
        raise HTTPException(status_code=401, detail="Authentication required")
        
    actor_id = actor.id if actor else None
    
    # Get field permissions
    pe = get_permission_engine(db)
    field_permissions = pe.get_field_permissions(actor_id, entity_name) if actor_id else {}
    
    # If candidate bypass, we grant explicit write access to specific fields
    if not actor_id and entity_name == "candidate":
        field_permissions = {
            "name": {"read": True, "write": True},
            "email": {"read": True, "write": True},
            "phone": {"read": True, "write": True},
            "resumeLink": {"read": True, "write": True}
        }
    
    fe = get_form_engine(db)
    return fe.render_form(entity_name, record_id, actor_id, field_permissions)
