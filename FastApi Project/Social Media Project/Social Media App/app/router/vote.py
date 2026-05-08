from fastapi import  Depends, HTTPException, status, APIRouter
from .. import model, schema, util, Oauth2
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote,db: Session = Depends(get_db), current_user :int=Depends(Oauth2.get_current_user)):
    pass

