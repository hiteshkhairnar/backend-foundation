from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User

from app.services.like_service import (
    like_post,
    unlike_post,
)

router = APIRouter(
    prefix="/likes",
    tags=["Likes"],
)


@router.post("/{post_id}")
def like(post_id: int,
         db: Session = Depends(get_db),
         current_user: User = Depends(get_current_user)):

    result = like_post(db, post_id, current_user)

    if result is None:
        raise HTTPException(404, "Post not found")

    if result == "already_liked":
        raise HTTPException(400, "Already liked")

    return {
        "message": "Post liked successfully"
    }


@router.delete("/{post_id}")
def unlike(post_id: int,
           db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user)):

    result = unlike_post(db, post_id, current_user)

    if not result:
        raise HTTPException(404, "Like not found")

    return {
        "message": "Like removed successfully"
    }