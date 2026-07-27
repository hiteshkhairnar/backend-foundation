from sqlalchemy.orm import Session

from app.models.bookmark import Bookmark
from app.models.post import Post
from app.models.user import User


def bookmark_post(
    db: Session,
    post_id: int,
    current_user: User,
):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        return None

    existing = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id,
        )
        .first()
    )

    if existing:
        return "already_bookmarked"

    bookmark = Bookmark(
        user_id=current_user.id,
        post_id=post_id,
    )

    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)

    return bookmark


def remove_bookmark(
    db: Session,
    post_id: int,
    current_user: User,
):
    bookmark = (
        db.query(Bookmark)
        .filter(
            Bookmark.user_id == current_user.id,
            Bookmark.post_id == post_id,
        )
        .first()
    )

    if not bookmark:
        return None

    db.delete(bookmark)
    db.commit()

    return True


def get_my_bookmarks(
    db: Session,
    current_user: User,
):
    return (
        db.query(Bookmark)
        .filter(Bookmark.user_id == current_user.id)
        .all()
    )


def get_bookmark_count(
    db: Session,
    post_id: int,
):
    return (
        db.query(Bookmark)
        .filter(Bookmark.post_id == post_id)
        .count()
    )


def is_post_bookmarked(
    db: Session,
    post_id: int,
    current_user: User,
):
    bookmark = (
        db.query(Bookmark)
        .filter(
            Bookmark.post_id == post_id,
            Bookmark.user_id == current_user.id,
        )
        .first()
    )

    return bookmark is not None