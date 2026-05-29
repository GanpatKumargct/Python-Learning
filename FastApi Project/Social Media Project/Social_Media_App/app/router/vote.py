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
    
    # db post exisist or not via post id
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()

    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {vote.post_id} doesn't exist")
    
    vote_Query = db.query(model.Vote).filter(model.Vote.post_id == vote.post_id, model.Vote.user_id==current_user.id)

    found_vote = vote_Query.first()

    if (vote.dir==1):
        if found_vote: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already vote on post {vote.post_id}")
        new_vote = model.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message ": "Successfully added the vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        vote_Query.delete(synchronize_session=False)
        db.commit()

        return {"Message ": "Successfully deleted vote"}
    
    # --9:45
