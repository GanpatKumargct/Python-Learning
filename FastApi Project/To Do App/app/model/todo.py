
from pydantic import BaseModel, Field


class createTodo(BaseModel):
    content:str=Field(..., min_length=4, max_length=60)
    isCompleted :bool = False