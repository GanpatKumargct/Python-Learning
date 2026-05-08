from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import User, UserUpdateRole
from app.crud.user import get_users, get_user, assign_role_to_user
from app.api.deps import get_admin_user, get_current_active_user
from app.utils.logger import logger

router = APIRouter()

@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current logged in user details. Any active user can hit this.
    """
    return current_user

# Admin only routes to manage users
@router.get("/", response_model=list[User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):
    """
    List all users. Admin only.
    """
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.put("/{user_id}/role", response_model=User)
def update_user_role(user_id: int, role_update: UserUpdateRole, db: Session = Depends(get_db), current_user = Depends(get_admin_user)):
    """
    Admin can assign a role to a user.
    """
    logger.info(f"Admin {current_user.email} updating role for user ID: {user_id} to role ID: {role_update.role_id}")
    db_user = get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = assign_role_to_user(db, user_id=user_id, role_id=role_update.role_id)
    return updated_user
