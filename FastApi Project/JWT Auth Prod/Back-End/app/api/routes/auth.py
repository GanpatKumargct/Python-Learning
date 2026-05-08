from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, User
from app.crud.user import get_user_by_email, create_user
from app.core.security import verify_password, create_access_token
from app.utils.logger import logger

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user. External users can use this route.
    """
    logger.info(f"Attempting to register user with email: {user.email}")
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        logger.warning(f"Registration failed. Email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Actually, you might want to assign a default "External" role here,
    # but for simplicity, we'll leave it as None or handle it if "External" role exists.
    new_user = create_user(db=db, user=user)
    logger.info(f"Successfully registered user with email: {user.email}")
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Standard OAuth2 compatible token login, getting an access token for future requests.
    """
    logger.info(f"Login attempt for email: {form_data.username}")
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed for email: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.email)
    logger.info(f"Login successful for email: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
