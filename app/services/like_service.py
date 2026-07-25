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