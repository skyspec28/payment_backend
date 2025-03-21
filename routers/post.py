
from typing import Optional
from .. import models ,oauth2
from .. database import get_db
from ..schemas import PostBase ,PostCreate ,Post
from sqlalchemy.orm import Session
from fastapi import status
from fastapi import HTTPException ,Depends ,APIRouter


router=APIRouter(
    tags=['Posts']
)

@router.get("/posts",response_model=list[Post])
def get_posts(db:Session = Depends(get_db),get_current_user:int= Depends(oauth2.get_current_user),limit:int=10,skip:int=0 ,search: Optional[str] = "" ):
   
   print(limit)
   posts =db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   return posts


@router.post("/posts",status_code=status.HTTP_201_CREATED) 
def create_post(post:PostCreate ,db:Session = Depends(get_db),  user_id:int =Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s , %s , %s) RETURNING * """ , (post.title , post.content , post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(user_id)
    new_post = models.Post(owner_id=user_id.id,**post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts/{id}",response_model=Post)
def get_post(id:int ,db:Session = Depends(get_db),user_id:int =Depends(oauth2.get_current_user)):
    # get_by_id=db.get(models.Post, id)
    get_by_id=db.query(models.Post).filter(models.Post.id == id).first()
    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} not found ")
    return get_by_id

# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int ,db:Session=Depends(get_db),current_user:int= Depends(oauth2.get_current_user)):
#     post_query=db.query(models.Post).filter(models.Post.id==id)
#     post=post_query.first()
#     print(current_user.id)
#     print(post.owner_id)
#     if post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
#     if post.owner_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cant delete not authorised")
#     post_query.delete(synchronize_session=False)
#     db.commit()
#     return {"message": "Post deleted successfully"}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user)  # Correct type
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    print(f"Current User ID: {current_user.id}, Post Owner ID: {post.owner_id}")


    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )
    if int(post.owner_id) != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to delete this post (User {current_user.id} vs Owner {post.owner_id})"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post deleted successfully"}


@router.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post:PostCreate,db:Session=Depends(get_db),get_current_user:int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title=%s , content=%s ,published=%s WHERE id = %s RETURNING *""", (post.title ,post.content , post.published ,id,))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query=db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first()

    updated_data=post.model_dump()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if post.id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="cant delete not authorised")
    
    post_query.update(updated_data ,synchronize_session=False)
    
    db.commit()
    db.refresh(existing_post)
    return  post

