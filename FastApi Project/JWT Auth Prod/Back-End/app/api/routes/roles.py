from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.role import Role, RoleCreate
from app.crud.role import get_roles, create_role, get_role_by_name
from app.api.deps import get_admin_user
from app.utils.logger import logger

router = APIRouter()

# Only "Admin" role can access these endpoints
@router.post("/", response_model=Role)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):
    """
    Create new internal roles like HR, Process eng, Manager, Founder.
    Strictly for Admin users only.
    """
    logger.info(f"Admin {current_user.email} is creating a new role: {role.name}")
    db_role = get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    return create_role(db=db, role=role)

@router.get("/", response_model=list[Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):
    """
    Get all available roles. Only for Admins.
    """
    roles = get_roles(db, skip=skip, limit=limit)
    return roles
