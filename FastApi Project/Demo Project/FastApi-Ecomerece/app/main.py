# from fastapi import FastAPI


# app = FastAPI()

# @app.get('/')
# def hello():
#     return "Hi, Welcome to TestNeo"

# @app.get("/hello")
# def greet():
#     return {"message":"Hey this is Ganpat",
#             "status":"High"}

# @app.get("/product/{id}")
# def product(id:int):
#     product = ['mouse','keyboard','charger', 'bomb']

#     return product[id] if product[id] else HTTPException(statuscode = 404, detail = "Product Nahi hai")

from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# ----- Model (DTO equivalent) -----
class User(BaseModel):
    id: int
    name: str
    email: str

# ----- In-memory DB (for demo) -----
db: Dict[int, User] = {}

# ----- CREATE -----
@app.post("/users")
def create_user(user: User):
    if user.id in db:
        raise HTTPException(status_code=400, detail="User already exists")
    db[user.id] = user
    return user

# ----- READ -----
@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    return db[user_id]

@app.get("/users")
def get_user():
    # if user_id not in db:
    #     raise HTTPException(status_code=404, detail="User not found")
    return db
# ----- UPDATE -----
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    db[user_id] = user
    return user

# ----- DELETE -----
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    if user_id not in db:
        raise HTTPException(status_code=404, detail="User not found")
    del db[user_id]
    return {"message": "User deleted"}

@app.post("/posts")
def create_post(payload : dict = Body(...)):
    print(payload)
    # return {"new post": payload}

    return {"new post": f"title : {payload['title']},\\n content : {payload['content']}"}
