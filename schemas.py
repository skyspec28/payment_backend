from pydantic import BaseModel,EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id:int

class UserCreate(BaseModel):
    email:EmailStr
    password: str

class UserResponse(BaseModel):
    email:EmailStr
    id:int

class LoginUser(BaseModel):
    email:EmailStr
    password: str