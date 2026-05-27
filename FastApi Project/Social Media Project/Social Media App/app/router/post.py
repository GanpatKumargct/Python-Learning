from fastapi import  Depends, HTTPException, status, APIRouter
from .. import model, schema, Oauth2

from ..database import  get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List


router = APIRouter(
    prefix="/posts", tags=['Posts']
)

@router.post("/", status_code=201, response_model=schema.ResponseModel)
def create_Post(post:schema.PostCreate, db :Session = Depends(get_db) , current_user :int=Depends(Oauth2.get_current_user)):
    
    print(current_user.email)
    new_post = model.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"message":"Post Created Succefully.",
            # "data":post} 
    return new_post

# @router.get("/", response_model=List[schema.ResponseModel])
@router.get("/", response_model=List[schema.PostOut])
def get_posts(db :Session = Depends(get_db), current_user :int=Depends(Oauth2.get_current_user),
               lim:int =10, skip :int=0, search:str=""):

    # this will return all the post doesn't matter which user is created(all post public)
    # all_posts= db.query(model.Post).filter(model.Post.title.contains(search)).limit(lim).offset(skip).all()
   

    #Query with vote join 
    all_posts_vote = db.query(model.Post,func.count(model.Vote.post_id).label("votes")
    ).join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by( model.Post.id
    ).filter(model.Post.title.contains(search)).limit(lim).offset(skip).all()


    print(lim)
    print(search)
    return all_posts_vote

    # This will return which user is logged in
    # all_posts = db.query(model.Post).filter(model.Post.owner_id == current_user.id).all()

    # return {"Message":"Here is your All Posts", 
    #         "posts":all_posts}
    

# @router.get("/{id}", response_model=schema.ResponseModel)
# def get_post(id:int, db :Session = Depends(get_db), current_user :int=Depends(Oauth2.get_current_user)):

#     post= db.query(model.Post).filter(model.Post.id == id).first()

#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
#     return post
@router.get("/{id}", response_model=schema.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(Oauth2.get_current_user)
):

    post = db.query(
        model.Post,
        func.count(model.Vote.post_id).label("votes")
    ).join(
        model.Vote,
        model.Vote.post_id == model.Post.id,
        isouter=True
    ).group_by(
        model.Post.id
    ).filter(
        model.Post.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@router.put("/{id}", response_model=schema.ResponseModel)
def update_posts(id:int, post:schema.PostUpdate, db :Session = Depends(get_db),  current_user :int=Depends(Oauth2.get_current_user)):

    existing_post= db.query(model.Post).filter(model.Post.id == id).first()

    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized to perform this actions.")
    # existing_post.owner_id = current_user.id
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published

    db.commit()
    db.refresh(existing_post)

    return existing_post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user :int=Depends(Oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized to perform this actions.")
    
    db.delete(post)
    db.commit()


