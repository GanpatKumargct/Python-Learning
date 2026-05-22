from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.Database.database import get_db
from app.Model import models
import jwt # Needs pyjwt in requirements

security = HTTPBearer(auto_error=False)

def verify_zoho_sso_token_optional(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    if not credentials:
        return None
        
    token = credentials.credentials
    try:
        # Mocking decoding JWT
        if token == "invalid":
            return None
            
        email = "admin@ethereal.com" # Mocked extraction
        actor = db.query(models.Actor).filter(models.Actor.email == email).first()
        return actor
    except Exception:
        return None

def verify_zoho_sso_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    actor = verify_zoho_sso_token_optional(credentials, db)
    if not actor:
        raise HTTPException(status_code=401, detail="Could not validate credentials or user not found")
    return actor
