from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

from app.services.bookmark_service import (
    bookmark_post,
    remove_bookmark,
    get_my_bookmarks,
    get_bookmark_count,
    is_post_bookmarked,
)

router = APIRouter(
    prefix="/bookmarks",
    tags=["Bookmarks"],
)


# Bookmark a Post
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
        "success": True,
        "message": "Post bookmarked successfully",
    }


# Remove Bookmark
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
        "success": True,
        "message": "Bookmark removed successfully",
    }


# My Bookmarks
@router.get("/me")
def my_bookmarks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_my_bookmarks(db, current_user)


# Bookmark Count
@router.get("/{post_id}/count")
def bookmark_count(
    post_id: int,
    db: Session = Depends(get_db),
):
    return {
        "post_id": post_id,
        "bookmarks": get_bookmark_count(db, post_id),
    }


# Bookmark Status
@router.get("/{post_id}/status")
def bookmark_status(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return {
        "post_id": post_id,
        "bookmarked": is_post_bookmarked(
            db,
            post_id,
            current_user,
        ),
    }