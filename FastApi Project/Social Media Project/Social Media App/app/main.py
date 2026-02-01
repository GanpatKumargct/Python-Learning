from fastapi import FastAPI, Depends
from . import model, schema
from .database import engine, get_db, Base
from sqlalchemy.orm import Session


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return "Welcome to Social Media Project"


@app.post("/posts")
def create_Post(post:schema.Post, db :Session = Depends(get_db) ):
    new_post = db.add(model.Post(**post.dict()))
    db.commit()
    
    return {"message":"Post Created Succefully.",
            "data":post} 

@app.get("/posts")
def get_posts(db :Session = Depends(get_db)):

    all_posts= db.query(model.Post).all()

    return {"Message":"Here is your All Posts", 
            "posts":all_posts}

@app.get("/posts/{id}")
def get_post(id:int, db :Session = Depends(get_db)):

    post= db.query(model.Post).filter(model.Post.id == id).first()

    if post:
        return {"Message":"Your Post is", 
            "posts":post}
    return "Post Not Found"


@app.put("/posts/{id}")
def update_posts(id:int, post:schema.Post, db :Session = Depends(get_db)):

    existing_post= db.query(model.Post).filter(model.Post.id == id).first()

    if existing_post:
        existing_post.title = post.title
        existing_post.content = post.content
        existing_post.published = post.published

        db.commit()

        return {"message ":"Post updated Successfully.",
                "post":post}
    else:
        return "Post Not Found"
    

@app.delete("/post/{id}")
def delete_posts(id:int, db :Session = Depends(get_db)):
    post= db.query(model.Post).filter(model.Post.id == id).first()

    if post:
        db.delete(post)
        db.commit()

        return "Post deleted.....!"
    return "Post Not Found"
    