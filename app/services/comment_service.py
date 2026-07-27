from sqlalchemy.orm import Session, joinedload

from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.schemas.comment import CommentCreate


def create_comment(
    db: Session,
    post_id: int,
    comment: CommentCreate,
    current_user: User,
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    db_comment = Comment(
        content=comment.content,
        user_id=current_user.id,
        post_id=post_id,
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    return db_comment


def get_comments(db: Session, post_id: int):
    return (
        db.query(Comment)
        .options(joinedload(Comment.owner))
        .filter(Comment.post_id == post_id)
        .all()
    )

def update_comment(
    db: Session,
    comment_id: int,
    comment: CommentCreate,
    current_user: User,
):
    db_comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if not db_comment:
        return None

    if db_comment.user_id != current_user.id:
        return "forbidden"

    db_comment.content = comment.content

    db.commit()
    db.refresh(db_comment)

    return db_comment


def delete_comment(
    db: Session,
    comment_id: int,
    current_user: User,
):
    db_comment = (
        db.query(Comment)
        .filter(Comment.id == comment_id)
        .first()
    )

    if not db_comment:
        return None

    if db_comment.user_id != current_user.id:
        return "forbidden"

    db.delete(db_comment)
    db.commit()

    return True

def get_comment(
    db: Session,
    comment_id: int,
):
    return (
        db.query(Comment)
        .options(joinedload(Comment.owner))
        .filter(Comment.id == comment_id)
        .first()
    )