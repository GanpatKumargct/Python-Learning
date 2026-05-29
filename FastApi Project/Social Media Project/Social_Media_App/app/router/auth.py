
from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from .. import schema, model, util, Oauth2
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Auth'])

@router.post("/login", response_model=schema.Token)
def login(user_data:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    user = db.query(model.User).filter(
        model.User.email == user_data.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Creditional!")
    
    if not util.verifyPassword(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Creditaional!")
    

    # Create a token 
    # return token  
    access_token = Oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token, "token_type":"bearer"}






