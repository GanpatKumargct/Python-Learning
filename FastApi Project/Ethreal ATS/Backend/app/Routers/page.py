from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Model import models
from app.core.auth import verify_zoho_sso_token

router = APIRouter(
    prefix="/page",
    tags=["page"]
)

@router.get("/resolve/{entity_name}/{entity_state}")
def resolve_page(entity_name: str, entity_state: str, db: Session = Depends(get_db), actor: models.Actor = Depends(verify_zoho_sso_token)):
    """
    Maps {role} + {entity_state} -> {page_component} config.
    """
    # Fetch roles for actor
    actor_roles = db.query(models.ActorRole).filter(models.ActorRole.actor_id == actor.id).all()
    role_ids = [ar.role_id for ar in actor_roles]
    roles = db.query(models.Role).filter(models.Role.id.in_(role_ids)).all()
    role_names = [r.name for r in roles]
    
    # Static config for Phase 1 (would normally live in DB JSON)
    route_config = {
        "candidate": {
            "applied": {
                "hiring_manager": {
                    "page_component": "CandidateReviewForm",
                    "available_actions": ["move_to_screening", "reject"]
                }
            },
            "offer": {
                "ptc": {
                    "page_component": "OfferLetterForm",
                    "available_actions": ["send_offer", "withdraw_offer"]
                }
            }
        }
    }
    
    # Simple resolution logic matching the first matching role config
    entity_config = route_config.get(entity_name, {})
    state_config = entity_config.get(entity_state, {})
    
    for rname in role_names:
        if rname in state_config:
            return state_config[rname]
            
    # Default fallback
    return {
        "page_component": "DefaultReadOnlyView",
        "available_actions": []
    }
