from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.database import get_db
from app.schemas.token import TokenData
from app.crud.user import get_user_by_email
from app.db.models import User

# This acts as our token URL where users send username/password to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# RBAC Dependencies
def require_role(required_role_names: list[str]):
    """
    Dependency to check if the current user has one of the required roles.
    Industry standard practice for RBAC implementation.
    """
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role"
            )
        if current_user.role.name not in required_role_names:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker

# Predefined role checkers for common routes
get_admin_user = require_role(["Admin"])
