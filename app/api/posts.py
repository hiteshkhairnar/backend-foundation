from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.post import (
    PostCreate,
    PostResponse,
    PostWithOwner,
)
from app.services.post_service import (
    create_post,
    get_posts,
    get_post,
    update_post,
    delete_post,
)
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


# ----------------------------------
# Create Post
# ----------------------------------

@router.post("/", response_model=PostResponse)
def create_new_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_post(
        db,
        post,
        current_user,
    )


# ----------------------------------
# Get All Posts
# ----------------------------------

@router.get("/", response_model=list[PostWithOwner])
def read_posts(
    db: Session = Depends(get_db),
):
    return get_posts(db)


# ----------------------------------
# Get Single Post
# ----------------------------------

@router.get("/{post_id}", response_model=PostWithOwner)
def read_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    post = get_post(db, post_id)

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


# ----------------------------------
# Update Post
# ----------------------------------

@router.put("/{post_id}", response_model=PostResponse)
def update_existing_post(
    post_id: int,
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_post = update_post(
        db,
        post_id,
        post,
        current_user,
    )

    if updated_post is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if updated_post == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="You can update only your own posts.",
        )

    return updated_post


# ----------------------------------
# Delete Post
# ----------------------------------

@router.delete("/{post_id}")
def delete_existing_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted = delete_post(
        db,
        post_id,
        current_user,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    if deleted == "forbidden":
        raise HTTPException(
            status_code=403,
            detail="You can delete only your own posts.",
        )

    return {
        "message": "Post deleted successfully"
    }