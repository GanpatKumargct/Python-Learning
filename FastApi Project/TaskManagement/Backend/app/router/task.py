from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from app.Model import model
from app.Schema import schema
from app.database import database
from app.core import oauth2

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.get("/", response_model=List[schema.TaskOut])
def get_tasks(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    tasks = db.query(model.Task).filter(model.Task.owner_id == current_user.id).filter(model.Task.title.contains(search)).limit(limit).offset(skip).all()
    return tasks

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.TaskOut)
def create_task(task: schema.TaskCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_task = model.Task(owner_id=current_user.id, **task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{id}", response_model=schema.TaskOut)
def get_task(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(model.Task).filter(model.Task.id == id, model.Task.owner_id == current_user.id).first()
    
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} was not found")
        
    return task

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(model.Task).filter(model.Task.id == id, model.Task.owner_id == current_user.id)
    task = task_query.first()
    
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} does not exist")
        
    task_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.TaskOut)
def update_task(id: int, updated_task: schema.TaskCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(model.Task).filter(model.Task.id == id, model.Task.owner_id == current_user.id)
    task = task_query.first()
    
    if task == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id: {id} does not exist")
        
    task_query.update(updated_task.dict(), synchronize_session=False)
    db.commit()
    return task_query.first()
