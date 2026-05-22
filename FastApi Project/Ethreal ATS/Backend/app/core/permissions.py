from sqlalchemy.orm import Session
from app.Model import models
from typing import Optional, Dict

class Decision:
    def __init__(self, effect: str, reason: str):
        self.effect = effect
        self.reason = reason

class PermissionEngine:
    def __init__(self, db: Session):
        self.db = db

    def evaluate(self, actor_id: str, action: str, entity_name: str, record_id: Optional[str] = None, field_name: Optional[str] = None) -> Decision:
        """
        Evaluates RBAC policies. Called by all other engines.
        Returns a decision (ALLOW/DENY) based on most specific rule.
        """
        # Fetch actor's roles
        actor_roles = self.db.query(models.ActorRole).filter(models.ActorRole.actor_id == actor_id).all()
        if not actor_roles:
            return Decision("deny", "Actor has no assigned roles.")

        role_ids = [ar.role_id for ar in actor_roles]
        
        # In a fully fleshed system, we check from most specific to least specific.
        # Check field level
        if field_name:
            field_perm = self.db.query(models.Permission).filter(
                models.Permission.role_id.in_(role_ids),
                models.Permission.entity_name == entity_name,
                models.Permission.action == action,
                models.Permission.field_name == field_name
            ).first()
            if field_perm:
                return Decision(field_perm.effect, f"Field level rule matched for {field_name}")

        # Check entity level
        entity_perm = self.db.query(models.Permission).filter(
            models.Permission.role_id.in_(role_ids),
            models.Permission.entity_name == entity_name,
            models.Permission.action == action,
            models.Permission.field_name.is_(None)
        ).first()

        if entity_perm:
            return Decision(entity_perm.effect, f"Entity level rule matched for {entity_name}")
            
        # Deny by default
        return Decision("deny", "No matching permission rule found.")

    def get_field_permissions(self, actor_id: str, entity_name: str) -> Dict[str, Dict[str, bool]]:
        """
        Returns a dictionary of field access masks.
        { "field_name": { "read": True, "write": False } }
        """
        actor_roles = self.db.query(models.ActorRole).filter(models.ActorRole.actor_id == actor_id).all()
        role_ids = [ar.role_id for ar in actor_roles]
        
        perms = self.db.query(models.Permission).filter(
            models.Permission.role_id.in_(role_ids),
            models.Permission.entity_name == entity_name,
            models.Permission.field_name.isnot(None)
        ).all()
        
        field_mask = {}
        for p in perms:
            if p.field_name not in field_mask:
                field_mask[p.field_name] = {"read": False, "write": False}
            if p.action == "read" and p.effect == "allow":
                field_mask[p.field_name]["read"] = True
            elif p.action == "write" and p.effect == "allow":
                field_mask[p.field_name]["write"] = True
                
        return field_mask

def get_permission_engine(db: Session) -> PermissionEngine:
    return PermissionEngine(db)
