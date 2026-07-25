from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.services.bookmark_service import (
    bookmark_post,
    remove_bookmark,
    get_my_bookmarks,
)

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


@router.post("/{post_id}")
def bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = bookmark_post(db, post_id, current_user)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if result == "already_bookmarked":
        raise HTTPException(
            status_code=400,
            detail="Already bookmarked",
        )

    return {
        "message": "Post bookmarked successfully"
    }


@router.delete("/{post_id}")
def delete_bookmark(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = remove_bookmark(db, post_id, current_user)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Bookmark not found",
        )

    return {
        "message": "Bookmark removed successfully"
    }


@router.get("/me")
def my_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_bookmarks(db, current_user)