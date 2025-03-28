from sqlalchemy import TIMESTAMP, Column,String ,ForeignKey,Integer ,Boolean, text
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
   __tablename__ ="posts"
   id = Column(Integer ,primary_key=True ,nullable= False)
   title= Column(String , nullable=False)
   content= Column(String , nullable=False)
   published= Column(Boolean, nullable=False)
   owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
   created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   owner= relationship("User")

    
class User(Base):
   __tablename__ ="users"
   id = Column(Integer ,primary_key=True ,nullable= False)
   email=Column(String , nullable=False ,unique=True)
   password=Column(String ,nullable=False)
   created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
   
class Vote(Base):
   __tablename__ ="vote"
   user_id=Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
   post_id=Column(Integer, ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
