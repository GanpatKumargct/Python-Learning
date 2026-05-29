from fastapi import  Depends, HTTPException, status, APIRouter
from .. import model, schema, util
from ..database import  get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=['Users'])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.userResponse)
def create_user(user: schema.user, db: Session = Depends(get_db)):

    hashed = util.hash_password(user.password)
    user.password = hashed


    new_user = model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/", response_model=schema.userResponse)
def get_user(id:int,db: Session = Depends(get_db) ):
    
    user= db.query(model.User).filter(model.User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user