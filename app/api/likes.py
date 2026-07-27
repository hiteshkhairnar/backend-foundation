from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User

from app.services.like_service import (
    like_post,
    unlike_post,
    get_like_count,
    is_post_liked,
)

router = APIRouter(
    prefix="/likes",
    tags=["Likes"],
)


# Like a Post
@router.post("/{post_id}")
def like(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = like_post(db, post_id, current_user)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if result == "already_liked":
        raise HTTPException(
            status_code=400,
            detail="Already liked",
        )

    return {
        "success": True,
        "message": "Post liked successfully",
    }


# Unlike a Post
@router.delete("/{post_id}")
def unlike(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = unlike_post(db, post_id, current_user)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Like not found",
        )

    return {
        "success": True,
        "message": "Like removed successfully",
    }


# Total Likes
@router.get("/{post_id}/count")
def like_count(
    post_id: int,
    db: Session = Depends(get_db),
):
    return {
        "post_id": post_id,
        "likes": get_like_count(db, post_id),
    }


# Check if Current User Liked
@router.get("/{post_id}/status")
def like_status(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "post_id": post_id,
        "liked": is_post_liked(
            db,
            post_id,
            current_user,
        ),
    }