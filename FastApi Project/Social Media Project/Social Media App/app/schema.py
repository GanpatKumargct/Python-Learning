from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class ResponseModel(PostBase):
    id:int

    class Config:
        orm_mode = True

class user(BaseModel):
    email : EmailStr
    password : str


class userResponse(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    
    model_config = ConfigDict(from_attributes=True)
