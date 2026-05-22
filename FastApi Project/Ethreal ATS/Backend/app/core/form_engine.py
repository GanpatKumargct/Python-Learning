from sqlalchemy.orm import Session
from app.Model import models
from typing import Dict, Any, Optional

class FormEngine:
    def __init__(self, db: Session):
        self.db = db

    def render_form(self, entity_name: str, record_id: Optional[str], actor_id: str, field_permissions: Dict[str, Dict[str, bool]]) -> Dict[str, Any]:
        """
        Renders form schemas from entity definitions + RBAC masks.
        Produces a form config that the frontend renders.
        """
        # Fetch the entity definition
        entity = self.db.query(models.EntityDefinition).filter(models.EntityDefinition.name == entity_name).first()
        if not entity:
            return {"error": "Entity not found"}

        # Fetch form definition
        form_def = self.db.query(models.FormDefinition).filter(models.FormDefinition.entity_id == entity.id, models.FormDefinition.is_active == True).first()
        if not form_def:
            # Fallback if no specific layout exists
            return {"error": "Form layout not defined for this entity"}

        layout = form_def.layout
        rendered_sections = []
        
        # Assume layout is structured as {"sections": [{"label": "...", "fields": [...]}]}
        for section in layout.get("sections", []):
            rendered_fields = []
            for field in section.get("fields", []):
                field_name = field.get("field_name")
                
                # RBAC Masking
                perm = field_permissions.get(field_name, {"read": False, "write": False})
                if not perm.get("read", False):
                    continue # Skip field completely if no read access
                    
                rendered_field = dict(field)
                if not perm.get("write", False):
                    rendered_field["editable"] = False # Enforce read-only

                # If new record, maybe hide fields conditionally
                if not record_id and rendered_field.get("conditional"):
                    pass # conditional logic goes here
                    
                rendered_fields.append(rendered_field)
                
            if rendered_fields:
                rendered_sections.append({
                    "label": section.get("label"),
                    "fields": rendered_fields
                })
                
        return {"sections": rendered_sections}

    def validate_submission(self, entity_name: str, form_data: Dict[str, Any], actor_id: str, field_permissions: Dict[str, Dict[str, bool]]) -> Dict[str, Any]:
        """
        Validates a submitted form data payload.
        Ensures the user isn't modifying fields they don't have write access to.
        """
        errors = []
        for key, value in form_data.items():
            perm = field_permissions.get(key, {"read": False, "write": False})
            if not perm.get("write", False):
                errors.append({"field": key, "message": "You do not have permission to write to this field."})
                
        # In a full implementation, we'd also check against FieldDefinition for types, required, enums, etc.
        
        if errors:
            return {"ok": False, "errors": errors}
        return {"ok": True}

def get_form_engine(db: Session) -> FormEngine:
    return FormEngine(db)
