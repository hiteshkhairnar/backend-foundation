from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc

from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate


# ----------------------------
# Create Post
# ----------------------------

def create_post(
    db: Session,
    post: PostCreate,
    current_user: User,
):
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=current_user.id,
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post


# ----------------------------
# Get Posts (Search + Pagination + Sorting)
# ----------------------------

def get_posts(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str = "",
    sort: str = "latest",
):
    query = db.query(Post).options(
        joinedload(Post.owner)
    )

    if search:
        query = query.filter(
            or_(
                Post.title.ilike(f"%{search}%"),
                Post.content.ilike(f"%{search}%"),
            )
        )

    if sort == "title":
        query = query.order_by(Post.title)

    elif sort == "oldest":
        query = query.order_by(Post.id)

    else:
        query = query.order_by(desc(Post.id))

    total = query.count()

    posts = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "posts": posts,
    }


# ----------------------------
# Get Single Post
# ----------------------------

def get_post(
    db: Session,
    post_id: int,
):
    return (
        db.query(Post)
        .options(joinedload(Post.owner))
        .filter(Post.id == post_id)
        .first()
    )


# ----------------------------
# Update Post
# ----------------------------

def update_post(
    db: Session,
    post_id: int,
    post: PostCreate,
    current_user: User,
):
    db_post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not db_post:
        return None

    if db_post.user_id != current_user.id:
        return "forbidden"

    db_post.title = post.title
    db_post.content = post.content

    db.commit()
    db.refresh(db_post)

    return db_post


# ----------------------------
# Delete Post
# ----------------------------

def delete_post(
    db: Session,
    post_id: int,
    current_user: User,
):
    db_post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .first()
    )

    if not db_post:
        return None

    if db_post.user_id != current_user.id:
        return "forbidden"

    db.delete(db_post)
    db.commit()

    return True