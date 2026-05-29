from pydantic import BaseModel, EmailStr, ConfigDict

from datetime import datetime
from typing import Optional
from pydantic.types import conint


class userResponse(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime
    
    model_config = ConfigDict(from_attributes=True)

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
    created_at:datetime
    owner:userResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:ResponseModel
    votes:int
    class Config:
        orm_mode = True

class user(BaseModel):
    email : EmailStr
    password : str



class userLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id :int
    dir : conint(le =1)
    #le =1 means less than or equal to one