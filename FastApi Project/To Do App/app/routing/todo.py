
from fastapi import APIRouter
from app.model.todo import createTodo
router = APIRouter(prefix="/todo")

@router.get("/")
def index():
    return {
        "message ": "Hello From Router"
    }

@router.post("/")
def store(item:createTodo):
    return {"message ":"Created Todo item ","Item": item.model_dump()}