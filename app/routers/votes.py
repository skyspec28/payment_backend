from fastapi import APIRouter ,Depends ,status ,HTTPException
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2

from app.database import get_db
router=APIRouter(tags=["Votes"])


router = APIRouter(tags=["Votes"])

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote_count(
    vote: schemas.Votes,
    db: Session = Depends(get_db),
    get_current_user: int = Depends(oauth2.get_current_user)
):
    # ✅ Check if the post exists first
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post doesn't exist or has been deleted."
        )

    # ✅ Check if the user already voted
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == get_current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User {get_current_user.id} already voted for post {vote.post_id}"
            )

        # ✅ Add the new vote
        new_vote = models.Vote(post_id=vote.post_id, user_id=get_current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote not found"
            )

        # ✅ Delete the vote
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote"}
