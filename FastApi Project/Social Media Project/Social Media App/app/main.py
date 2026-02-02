from fastapi import FastAPI, Depends, HTTPException, status
from . import model, schema
from .database import engine, get_db, Base
from sqlalchemy.orm import Session
from typing import List


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return "Welcome to Social Media Project"


@app.post("/posts", status_code=201, response_model=schema.ResponseModel)
def create_Post(post:schema.PostCreate, db :Session = Depends(get_db) ):
    new_post = model.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # return {"message":"Post Created Succefully.",
            # "data":post} 
    return new_post

@app.get("/posts", response_model=List[schema.ResponseModel])
def get_posts(db :Session = Depends(get_db)):

    all_posts= db.query(model.Post).all()

    # return {"Message":"Here is your All Posts", 
    #         "posts":all_posts}

    return all_posts

@app.get("/posts/{id}", response_model=schema.ResponseModel)
def get_post(id:int, db :Session = Depends(get_db)):

    post= db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.put("/posts/{id}", response_model=schema.ResponseModel)
def update_posts(id:int, post:schema.PostUpdate, db :Session = Depends(get_db)):

    existing_post= db.query(model.Post).filter(model.Post.id == id).first()

    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published

    db.commit()
    db.refresh(existing_post)

    return existing_post
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).filter(model.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    