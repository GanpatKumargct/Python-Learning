import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.Database.database import Base

def generate_uuid():
    return str(uuid.uuid4())

# ---------------------------------------------------------
# ACTORS (Users)
# ---------------------------------------------------------
class Actor(Base):
    __tablename__ = "actors"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------
# ENTITY BUILDER ENGINE
# ---------------------------------------------------------
class EntityDefinition(Base):
    __tablename__ = "entity_definitions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, index=True)
    label = Column(String)
    module_id = Column(String(36), nullable=True) # Could link to a modules table
    custom_fields = Column(JSON, default={})
    schema_version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(36), ForeignKey("actors.id"))

class EntitySchemaHistory(Base):
    __tablename__ = "entity_schema_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_id = Column(String(36), ForeignKey("entity_definitions.id"))
    schema_snapshot = Column(JSON)
    version = Column(Integer)
    changed_by = Column(String(36), ForeignKey("actors.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(Text)

class FieldDefinition(Base):
    __tablename__ = "field_definitions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_id = Column(String(36), ForeignKey("entity_definitions.id"))
    name = Column(String)
    label = Column(String)
    field_type = Column(String)
    is_required = Column(Boolean, default=False)
    is_system = Column(Boolean, default=False)
    enum_values = Column(JSON, nullable=True)
    fk_entity = Column(String(36), ForeignKey("entity_definitions.id"), nullable=True)
    constraints = Column(JSON, nullable=True)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------
# FORM ENGINE
# ---------------------------------------------------------
class FormDefinition(Base):
    __tablename__ = "form_definitions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_id = Column(String(36), ForeignKey("entity_definitions.id"))
    name = Column(String)
    layout = Column(JSON)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class FormSchemaHistory(Base):
    __tablename__ = "form_schema_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    form_id = Column(String(36), ForeignKey("form_definitions.id"))
    layout_snapshot = Column(JSON)
    version = Column(Integer)
    changed_by = Column(String(36), ForeignKey("actors.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(Text)

# ---------------------------------------------------------
# PERMISSION ENGINE
# ---------------------------------------------------------
class Role(Base):
    __tablename__ = "roles"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, unique=True)
    label = Column(String)
    module_id = Column(String(36), nullable=True)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    role_id = Column(String(36), ForeignKey("roles.id"))
    entity_name = Column(String)
    action = Column(String)
    field_name = Column(String, nullable=True)
    scope = Column(String)
    effect = Column(String)

class PermissionHistory(Base):
    __tablename__ = "permission_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    permission_id = Column(String(36), ForeignKey("permissions.id"))
    snapshot = Column(JSON)
    changed_by = Column(String(36), ForeignKey("actors.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(Text)

class ActorRole(Base):
    __tablename__ = "actor_roles"
    
    id = Column(String(36), primary_key=True, default=generate_uuid) # Added ID for convenience
    actor_id = Column(String(36), ForeignKey("actors.id"))
    role_id = Column(String(36), ForeignKey("roles.id"))
    assigned_by = Column(String(36), ForeignKey("actors.id"))
    assigned_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

# ---------------------------------------------------------
# WORKFLOW ENGINE
# ---------------------------------------------------------
class WorkflowDefinition(Base):
    __tablename__ = "workflow_definitions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_name = Column(String)
    name = Column(String)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowState(Base):
    __tablename__ = "workflow_states"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    definition_id = Column(String(36), ForeignKey("workflow_definitions.id"))
    name = Column(String)
    label = Column(String)
    is_initial = Column(Boolean, default=False)
    is_terminal = Column(Boolean, default=False)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowTransition(Base):
    __tablename__ = "workflow_transitions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    definition_id = Column(String(36), ForeignKey("workflow_definitions.id"))
    name = Column(String)
    from_state_id = Column(String(36), ForeignKey("workflow_states.id"))
    to_state_id = Column(String(36), ForeignKey("workflow_states.id"))
    validator_rules = Column(JSON, default=[])
    roles_required = Column(JSON, default=[])
    actions = Column(JSON, default=[])
    sla_hours = Column(Integer, nullable=True)

class WorkflowDefinitionHistory(Base):
    __tablename__ = "workflow_definition_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    definition_id = Column(String(36), ForeignKey("workflow_definitions.id"))
    states_snapshot = Column(JSON)
    transitions_snapshot = Column(JSON)
    version = Column(Integer)
    changed_by = Column(String(36), ForeignKey("actors.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(Text)

class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    definition_id = Column(String(36), ForeignKey("workflow_definitions.id"))
    record_id = Column(String(36)) # Points to the dynamic record table
    entity_name = Column(String)
    current_state_id = Column(String(36), ForeignKey("workflow_states.id"))
    context = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

class WorkflowEvent(Base):
    __tablename__ = "workflow_events"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    instance_id = Column(String(36), ForeignKey("workflow_instances.id"))
    idempotency_key = Column(String, unique=True, index=True)
    from_state = Column(String)
    to_state = Column(String)
    transition_name = Column(String)
    actor_id = Column(String(36), ForeignKey("actors.id"), nullable=True)
    payload = Column(JSON, default={})
    occurred_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------
# AUDIT ENGINE
# ---------------------------------------------------------
class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    entity_name = Column(String, nullable=False)
    entity_id = Column(String(36))
    actor_id = Column(String(36), ForeignKey("actors.id"), nullable=True)
    event_type = Column(String)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    metadata_col = Column("metadata", JSON, nullable=True) # Renamed to avoid conflicts
    occurred_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------
# NOTIFICATION ENGINE
# ---------------------------------------------------------
class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String, unique=True)
    channel = Column(String)
    subject = Column(String)
    body_text = Column(Text)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_by = Column(String(36), ForeignKey("actors.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

class NotificationTemplateHistory(Base):
    __tablename__ = "notification_template_history"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    template_id = Column(String(36), ForeignKey("notification_templates.id"))
    snapshot = Column(JSON)
    version = Column(Integer)
    changed_by = Column(String(36), ForeignKey("actors.id"))
    changed_at = Column(DateTime, default=datetime.utcnow)
    change_reason = Column(Text)

class NotificationLog(Base):
    __tablename__ = "notification_log"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    idempotency_key = Column(String, unique=True)
    template_name = Column(String)
    recipient_id = Column(String(36), ForeignKey("actors.id"))
    channel = Column(String)
    status = Column(String)
    retry_count = Column(Integer, default=0)
    sent_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------
# ATS BUSINESS ENTITIES (Phase 1)
# Using generic tables for dynamic entity records.
# In a fully dynamic ERP, these might just be rows in a generalized `records` table, 
# or specific tables managed by the Entity Builder via alembic dynamically.
# For Phase 1 hardcoding:
# ---------------------------------------------------------
class CandidateRecord(Base):
    __tablename__ = "candidate_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobRequisitionRecord(Base):
    __tablename__ = "job_requisition_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class InterviewRecord(Base):
    __tablename__ = "interview_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FeedbackRecord(Base):
    __tablename__ = "feedback_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OfferRecord(Base):
    __tablename__ = "offer_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RefereeRecord(Base):
    __tablename__ = "referee_records"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    data = Column(JSON, default={})
    created_by = Column(String(36), ForeignKey("actors.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
