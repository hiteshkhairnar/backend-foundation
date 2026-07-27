from sqlalchemy.orm import Session

from app.models.like import Like
from app.models.post import Post
from app.models.user import User


def like_post(
    db: Session,
    post_id: int,
    current_user: User,
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    existing = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.post_id == post_id,
        )
        .first()
    )

    if existing:
        return "already_liked"

    like = Like(
        user_id=current_user.id,
        post_id=post_id,
    )

    db.add(like)
    db.commit()
    db.refresh(like)

    return like


def unlike_post(
    db: Session,
    post_id: int,
    current_user: User,
):
    like = (
        db.query(Like)
        .filter(
            Like.user_id == current_user.id,
            Like.post_id == post_id,
        )
        .first()
    )

    if not like:
        return None

    db.delete(like)
    db.commit()

    return True


def get_like_count(
    db: Session,
    post_id: int,
):
    return (
        db.query(Like)
        .filter(Like.post_id == post_id)
        .count()
    )


def is_post_liked(
    db: Session,
    post_id: int,
    current_user: User,
):
    like = (
        db.query(Like)
        .filter(
            Like.post_id == post_id,
            Like.user_id == current_user.id,
        )
        .first()
    )

    return like is not None