from fastapi import FastAPI ,HTTPException ,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from fastapi import status
from . import models 
from .schemas import PostBase ,PostCreate ,Post
from .database import engine ,SessionLocal



models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='SpectruM', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break

    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
   posts =db.query(models.Post).all()
   return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED ,response_model=Post)
def create_post(post:PostBase ,db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s , %s , %s) RETURNING * """ , (post.title , post.content , post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=Post)
def get_post(id:int ,db:Session = Depends(get_db)):
    # get_by_id=db.get(models.Post, id)
    get_by_id=db.query(models.Post).filter(models.Post.id == id).first()
    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found ")
    return get_by_id

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,db:Session=Depends(get_db)):
    post=db.get(models.Post,id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    db.delete(post)
    db.commit()
    return 

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post:PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title=%s , content=%s ,published=%s WHERE id = %s RETURNING *""", (post.title ,post.content , post.published ,id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    updated_data=post.model_dump()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post_query.update(updated_data ,synchronize_session=False)
    
    db.commit()
    db.refresh(existing_post)
    return  post
