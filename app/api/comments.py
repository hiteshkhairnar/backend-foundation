from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.comment import (
    CommentCreate,
    CommentResponse,
    CommentWithOwner,
)
from app.services.comment_service import (
    create_comment,
    get_comments,
    update_comment,
    delete_comment,
)
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


# Create Comment
@router.post("/{post_id}", response_model=CommentResponse)
def add_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = create_comment(
        db,
        post_id,
        comment,
        current_user,
    )

    if not db_comment:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return db_comment


# Get Comments
@router.get("/{post_id}", response_model=list[CommentWithOwner])
def read_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    return get_comments(db, post_id)


# Update Comment
@router.put("/{comment_id}", response_model=CommentResponse)
def edit_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_comment = update_comment(
        db,
        comment_id,
        comment,
        current_user,
    )

    if updated_comment is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if updated_comment == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own comments",
        )

    return updated_comment


# Delete Comment
@router.delete("/{comment_id}")
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_comment(
        db,
        comment_id,
        current_user,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if deleted == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own comments",
        )

    return {
        "success": True,
        "message": "Comment deleted successfully",
    }