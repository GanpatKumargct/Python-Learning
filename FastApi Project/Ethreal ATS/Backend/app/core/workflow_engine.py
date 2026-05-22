import uuid
from sqlalchemy.orm import Session
from app.Model import models
from typing import Any, Dict, List
from app.core.audit_engine import get_audit_engine
from app.core.permissions import get_permission_engine

class TransitionResult:
    def __init__(self, ok: bool, new_state: str = None, errors: List[str] = None):
        self.ok = ok
        self.new_state = new_state
        self.errors = errors or []

class WorkflowEngine:
    def __init__(self, db: Session):
        self.db = db
        self.audit = get_audit_engine(db)
        self.pe = get_permission_engine(db)

    def transition(self, instance_id: str, transition_name: str, actor_id: str, payload: Dict[str, Any], idempotency_key: str) -> TransitionResult:
        # Check idempotency
        existing_event = self.db.query(models.WorkflowEvent).filter(
            models.WorkflowEvent.idempotency_key == idempotency_key
        ).first()
        if existing_event:
            return TransitionResult(True, existing_event.to_state)

        # Load instance
        instance = self.db.query(models.WorkflowInstance).filter(models.WorkflowInstance.id == instance_id).first()
        if not instance:
            return TransitionResult(False, errors=["Workflow instance not found"])

        # Load definition and transition
        transition = self.db.query(models.WorkflowTransition).filter(
            models.WorkflowTransition.definition_id == instance.definition_id,
            models.WorkflowTransition.from_state_id == instance.current_state_id,
            models.WorkflowTransition.name == transition_name
        ).first()

        if not transition:
            return TransitionResult(False, errors=["Invalid transition from current state"])

        # Check permissions
        decision = self.pe.evaluate(actor_id, "transition", instance.entity_name, instance.record_id)
        if decision.effect == "deny":
            return TransitionResult(False, errors=[f"Permission denied: {decision.reason}"])

        # Run Validator Primitives
        errors = self._run_validators(transition.validator_rules, instance, payload, actor_id)
        if errors:
            return TransitionResult(False, errors=errors)

        # Update State
        old_state_id = instance.current_state_id
        instance.current_state_id = transition.to_state_id
        
        # Determine names for the log
        old_state_obj = self.db.query(models.WorkflowState).filter(models.WorkflowState.id == old_state_id).first()
        new_state_obj = self.db.query(models.WorkflowState).filter(models.WorkflowState.id == transition.to_state_id).first()
        old_state_name = old_state_obj.name if old_state_obj else "unknown"
        new_state_name = new_state_obj.name if new_state_obj else "unknown"

        # Log event
        event = models.WorkflowEvent(
            id=str(uuid.uuid4()),
            instance_id=instance.id,
            idempotency_key=idempotency_key,
            from_state=old_state_name,
            to_state=new_state_name,
            transition_name=transition_name,
            actor_id=actor_id,
            payload=payload
        )
        self.db.add(event)
        
        # Execute Action Handlers (in memory for now, normally would push to queue for async)
        self._execute_actions(transition.actions, instance, new_state_name, actor_id, payload)

        self.db.commit()
        return TransitionResult(True, new_state_name)

    def _run_validators(self, rules: List[Dict[str, Any]], instance, payload: Dict[str, Any], actor_id: str) -> List[str]:
        errors = []
        for rule in rules:
            rtype = rule.get("type")
            if rtype == "requires_field":
                field = rule.get("field")
                if not payload.get(field) and not instance.context.get(field):
                    errors.append(f"Required field missing: {field}")
            elif rtype == "role_check":
                roles_required = rule.get("roles", [])
                # simplistic check for phase 1
                actor_roles = self.db.query(models.ActorRole).filter(models.ActorRole.actor_id == actor_id).all()
                role_ids = [ar.role_id for ar in actor_roles]
                has_role = self.db.query(models.Role).filter(models.Role.id.in_(role_ids), models.Role.name.in_(roles_required)).first()
                if not has_role:
                    errors.append(f"Requires one of roles: {roles_required}")
            # Add more primitives here
        return errors

    def _execute_actions(self, actions: List[Dict[str, Any]], instance, new_state: str, actor_id: str, payload: Dict[str, Any]):
        for action in actions:
            atype = action.get("type")
            if atype == "update_field":
                field = action.get("field")
                val = action.get("value")
                # Need to write to the dynamic record table
                record_model = self._get_record_model(instance.entity_name)
                if record_model:
                    record = self.db.query(record_model).filter(record_model.id == instance.record_id).first()
                    if record:
                        # Because data is JSON, we can't easily partially update in sqlite. We read, mutate, write.
                        data = dict(record.data)
                        data[field] = val
                        record.data = data
            elif atype == "create_audit_log":
                self.audit.log(
                    entity_name=instance.entity_name,
                    entity_id=instance.record_id,
                    actor_id=actor_id,
                    event_type=action.get("event_type", "stage_transition"),
                    new_value={"state": new_state}
                )
            elif atype == "send_notification":
                from app.core.notification_engine import get_notification_engine
                ne = get_notification_engine(self.db)
                ne.dispatch(
                    template_name=action.get("template"),
                    recipients=action.get("to_roles", []), # Mocked for role translation to ids
                    context=payload,
                    idempotency_key=f"notify_{instance.id}_{new_state}"
                )

    def _get_record_model(self, entity_name: str):
        mapping = {
            "candidate": models.CandidateRecord,
            "job_requisition": models.JobRequisitionRecord,
            "interview": models.InterviewRecord,
            "feedback": models.FeedbackRecord,
            "offer": models.OfferRecord,
            "referee": models.RefereeRecord
        }
        return mapping.get(entity_name)

def get_workflow_engine(db: Session) -> WorkflowEngine:
    return WorkflowEngine(db)
