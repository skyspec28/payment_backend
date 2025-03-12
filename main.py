from fastapi import FastAPI ,HTTPException
from pydantic import BaseModel
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from fastapi import status

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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



def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
   cursor.execute("""SELECT * FROM posts """)
   posts=cursor.fetchall()
   return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s , %s , %s) RETURNING * """ , (post.title , post.content , post.published))
    new_post=cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id,)))
    get_by_id=cursor.fetchone()
    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id}not found ")
    return {"data":get_by_id}

app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """,(id))
    post=cursor.fetchone()
    conn.commit()
    return {"data":post}