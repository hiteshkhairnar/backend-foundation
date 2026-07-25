from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user

from app.models.user import User
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

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post("/{post_id}", response_model=CommentResponse)
def create_new_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_comment = create_comment(
        db,
        post_id,
        comment,
        current_user,
    )

    if not new_comment:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return new_comment


@router.get("/{post_id}", response_model=list[CommentWithOwner])
def read_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    return get_comments(db, post_id)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_existing_comment(
    comment_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated = update_comment(
        db,
        comment_id,
        comment,
        current_user,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if updated == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="You can update only your own comments.",
        )

    return updated


@router.delete("/{comment_id}")
def delete_existing_comment(
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
            detail="You can delete only your own comments.",
        )

    return {
        "message": "Comment deleted successfully"
    }