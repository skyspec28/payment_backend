from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel,EmailStr, Field


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: datetime

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

class PostOut(BaseModel):
    post:Post
    vote:int

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


class Votes(BaseModel):
    post_id:int
    dir: Annotated[int, Field(strict=True, le=1)]
    