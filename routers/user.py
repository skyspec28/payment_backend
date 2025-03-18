
from .. import models ,schemas ,utils
from sqlalchemy.orm import Session
from fastapi import FastAPI ,HTTPException ,Depends,status ,APIRouter
from ..database import get_db

router=APIRouter(
    tags=['User']
)

@router.post("/user",status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db) ):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump()) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user/{id}",response_model=schemas.UserResponse)
def get_user_id(id:int,db:Session=Depends(get_db)):
    user_id=db.query(models.User).filter(models.User.id == id ).first()

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"user with id :{id} not found ")
    
    return user_id