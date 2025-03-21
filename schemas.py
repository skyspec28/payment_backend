from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    email:EmailStr
    id:int

    class Config:
        from_attributes = True
        
class Post(PostBase):
    id:int
    owner_id:int
    owner:UserResponse

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email:EmailStr
    password: str



class LoginUser(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]= None