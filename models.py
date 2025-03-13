from typing import Annotated
from sqlmodel import Field, Session, SQLModel
from .database import engine
from fastapi import Depends


class Post(SQLModel, table=True):
    id :int =Field(default=None ,primary_key=True ,nullable=False)
    title:str =Field(index=True ,nullable= False)
    content: str = Field(nullable=False) 
    is_published:bool=Field(default=True)



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
